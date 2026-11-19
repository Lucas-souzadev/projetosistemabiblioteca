"""Interface web da biblioteca.

Servidor HTTP usando apenas a biblioteca padrao. Expoe uma API JSON
sobre os modulos existentes e serve os arquivos estaticos de `static/`.

Uso:
    python web.py            # http://localhost:8000
    python web.py 8080       # porta personalizada
"""
import json
import os
import re
import sys
from datetime import date
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlparse

import emprestimos
import livros
import relatorios
import storage
import usuarios

PASTA_STATIC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static")
TIPOS = {
    ".html": "text/html; charset=utf-8",
    ".css": "text/css; charset=utf-8",
    ".js": "application/javascript; charset=utf-8",
}


class ErroApi(Exception):
    def __init__(self, status, mensagem):
        super().__init__(mensagem)
        self.status = status
        self.mensagem = mensagem


def _serializar(obj):
    if isinstance(obj, date):
        return obj.isoformat()
    raise TypeError(f"Tipo nao serializavel: {type(obj)}")


def _emprestimo_detalhado(e):
    livro = livros.buscar_por_id(e["livro_id"])
    usuario = usuarios.buscar_por_id(e["usuario_id"])
    return {
        **e,
        "livro_titulo": livro["titulo"] if livro else None,
        "usuario_nome": usuario["nome"] if usuario else None,
    }


def _resumo():
    exemplares = sum(l["copias"] for l in livros.LIVROS)
    disponiveis = sum(l["disponiveis"] for l in livros.LIVROS)
    ativos = sum(1 for e in emprestimos.EMPRESTIMOS if e["devolvido_em"] is None)
    encerrados = len(emprestimos.EMPRESTIMOS) - ativos

    try:
        ocupacao = relatorios.taxa_ocupacao()
    except ZeroDivisionError:
        ocupacao = None

    try:
        mais = [{"titulo": t, "quantidade": q}
                for t, q in relatorios.livros_mais_emprestados()]
    except (TypeError, KeyError):
        # livro emprestado que foi removido do acervo
        mais = None

    return {
        "exemplares": exemplares,
        "disponiveis": disponiveis,
        "emprestimos_ativos": ativos,
        "emprestimos_encerrados": encerrados,
        "atrasados": [_emprestimo_detalhado(e) for e in relatorios.livros_atrasados()],
        "mais_emprestados": mais,
        "ocupacao": ocupacao,
    }


def _int(valor, campo):
    try:
        return int(valor)
    except (TypeError, ValueError):
        raise ErroApi(400, f"Campo '{campo}' deve ser um numero inteiro")


def _texto(dados, campo):
    valor = dados.get(campo)
    if not isinstance(valor, str):
        raise ErroApi(400, f"Campo '{campo}' obrigatorio")
    return valor


class Handler(BaseHTTPRequestHandler):
    server_version = "BibliotecaWeb/1.0"

    # ---- utilitarios ---------------------------------------------------

    def _responder(self, status, corpo):
        dados = json.dumps(corpo, default=_serializar, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(dados)))
        self.end_headers()
        self.wfile.write(dados)

    def _ler_json(self):
        tamanho = int(self.headers.get("Content-Length") or 0)
        if tamanho == 0:
            return {}
        try:
            dados = json.loads(self.rfile.read(tamanho).decode("utf-8"))
        except (ValueError, UnicodeDecodeError):
            raise ErroApi(400, "JSON invalido")
        if not isinstance(dados, dict):
            raise ErroApi(400, "Corpo deve ser um objeto JSON")
        return dados

    def _servir_estatico(self, caminho):
        if caminho in ("", "/"):
            caminho = "/index.html"
        nome = os.path.normpath(caminho.lstrip("/"))
        if nome.startswith("..") or os.path.isabs(nome):
            self.send_error(404)
            return
        arquivo = os.path.join(PASTA_STATIC, nome)
        tipo = TIPOS.get(os.path.splitext(arquivo)[1])
        if tipo is None or not os.path.isfile(arquivo):
            self.send_error(404)
            return
        with open(arquivo, "rb") as f:
            dados = f.read()
        self.send_response(200)
        self.send_header("Content-Type", tipo)
        self.send_header("Content-Length", str(len(dados)))
        self.end_headers()
        self.wfile.write(dados)

    def _despachar(self, metodo):
        url = urlparse(self.path)
        caminho = url.path.rstrip("/") or "/"
        if not caminho.startswith("/api/"):
            if metodo == "GET":
                self._servir_estatico(url.path)
            else:
                self.send_error(405)
            return
        try:
            status, corpo = self._rota_api(metodo, caminho, parse_qs(url.query))
            self._responder(status, corpo)
        except ErroApi as erro:
            self._responder(erro.status, {"erro": erro.mensagem})
        except ValueError as erro:
            # regras de negocio dos modulos legados sinalizam com ValueError
            self._responder(400, {"erro": str(erro)})
        except Exception as erro:  # noqa: BLE001
            self._responder(500, {"erro": f"Erro interno: {erro}"})

    # ---- rotas ---------------------------------------------------------

    def _rota_api(self, metodo, caminho, query):
        if caminho == "/api/livros":
            if metodo == "GET":
                termo = query.get("q", [""])[0]
                lista = livros.buscar_por_titulo(termo) if termo else livros.listar_livros()
                return 200, lista
            if metodo == "POST":
                d = self._ler_json()
                titulo = _texto(d, "titulo").strip()
                if not titulo:
                    raise ErroApi(400, "Titulo obrigatorio")
                livro = livros.cadastrar_livro(
                    titulo,
                    _texto(d, "autor").strip(),
                    _int(d.get("ano"), "ano"),
                    _int(d.get("copias", 1), "copias"),
                )
                storage.salvar()
                return 201, livro

        m = re.fullmatch(r"/api/livros/(\d+)", caminho)
        if m and metodo == "DELETE":
            livros.remover_livro(int(m.group(1)))
            storage.salvar()
            return 200, {"ok": True}

        if caminho == "/api/usuarios":
            if metodo == "GET":
                return 200, usuarios.listar_usuarios()
            if metodo == "POST":
                d = self._ler_json()
                u = usuarios.cadastrar_usuario(_texto(d, "nome"), _texto(d, "email"))
                storage.salvar()
                return 201, u

        if caminho == "/api/emprestimos":
            if metodo == "GET":
                return 200, [_emprestimo_detalhado(e) for e in emprestimos.EMPRESTIMOS]
            if metodo == "POST":
                d = self._ler_json()
                e = emprestimos.emprestar(
                    _int(d.get("usuario_id"), "usuario_id"),
                    _int(d.get("livro_id"), "livro_id"),
                )
                storage.salvar()
                return 201, _emprestimo_detalhado(e)

        m = re.fullmatch(r"/api/emprestimos/(\d+)/devolucao", caminho)
        if m and metodo == "POST":
            multa = emprestimos.devolver(int(m.group(1)))
            storage.salvar()
            return 200, {"multa": multa}

        if caminho == "/api/resumo" and metodo == "GET":
            return 200, _resumo()

        raise ErroApi(404, "Rota nao encontrada")

    def do_GET(self):
        self._despachar("GET")

    def do_POST(self):
        self._despachar("POST")

    def do_DELETE(self):
        self._despachar("DELETE")


def main():
    porta = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
    os.makedirs("dados", exist_ok=True)
    storage.carregar()
    # HTTPServer (sem threads) atende uma requisicao por vez, o que evita
    # condicoes de corrida sobre as listas globais dos modulos.
    servidor = HTTPServer(("127.0.0.1", porta), Handler)
    print(f"Biblioteca disponivel em http://localhost:{porta}  (Ctrl+C para sair)")
    try:
        servidor.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        storage.salvar()
        servidor.server_close()


if __name__ == "__main__":
    main()
