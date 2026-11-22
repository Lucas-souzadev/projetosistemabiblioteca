import livros
import usuarios
import emprestimos
import relatorios
import storage
from datetime import datetime


def menu():
    print()
    print("1 - Cadastrar livro")
    print("2 - Buscar livro por titulo")
    print("3 - Cadastrar usuario")
    print("4 - Emprestar livro")
    print("5 - Devolver livro")
    print("6 - Resumo")
    print("7 - Buscar emprestimos por periodo")
    print("0 - Sair")
    return input("Opcao: ")


def main():
    storage.carregar()
    while True:
        op = menu()
        if op == "1":
            titulo = input("Titulo: ")
            autor = input("Autor: ")
            ano = int(input("Ano: "))
            copias = int(input("Copias: "))
            l = livros.cadastrar_livro(titulo, autor, ano, copias)
            print("Livro cadastrado com id", l["id"])
        elif op == "2":
            termo = input("Titulo (ou parte): ")
            achados = livros.buscar_por_titulo(termo)
            if len(achados) == 0:
                print("Nenhum livro encontrado")
            for l in achados:
                print(l["id"], l["titulo"], "-", l["autor"], "(", l["disponiveis"], "/", l["copias"], ")")
        elif op == "3":
            nome = input("Nome: ")
            email = input("Email: ")
            try:
                u = usuarios.cadastrar_usuario(nome, email)
                print("Usuario cadastrado com id", u["id"])
            except ValueError as erro:
                print("Erro:", erro)
        elif op == "4":
            uid = int(input("Id do usuario: "))
            lid = int(input("Id do livro: "))
            try:
                e = emprestimos.emprestar(uid, lid)
                print("Emprestimo", e["id"], "devolver ate", e["data_prevista"].strftime("%d/%m/%Y"))
            except ValueError as erro:
                print("Erro:", erro)
        elif op == "5":
            eid = int(input("Id do emprestimo: "))
            try:
                multa = emprestimos.devolver(eid)
                if multa > 0:
                    print("Multa: R$ %.2f" % multa)
                else:
                    print("Devolvido sem multa")
            except ValueError as erro:
                print("Erro:", erro)
        elif op == "6":
            relatorios.imprimir_resumo()
        elif op == "7":
            try:
                data_inicio = datetime.strptime(
                    input("Data inicial (dd/mm/aaaa): "), "%d/%m/%Y"
                ).date()

                data_fim = datetime.strptime(
                    input("Data final (dd/mm/aaaa): "), "%d/%m/%Y"
                ).date()

                resultado = emprestimos.buscar_emprestimos_por_periodo(
                    data_inicio, data_fim
                )

                if not resultado:
                    print("Nenhum emprestimo encontrado nesse periodo")

                for e in resultado:
                    u = usuarios.buscar_por_id(e["usuario_id"])
                    l = livros.buscar_por_id(e["livro_id"])

                    print("ID:", e["id"])
                    print("Usuario:", u["nome"])
                    print("Livro:", l["titulo"])
                    print("Data do emprestimo:", e["data_emprestimo"].strftime("%d/%m/%Y"))
                    print("Devolver ate:", e["data_prevista"].strftime("%d/%m/%Y"))

            except ValueError as erro:
                print("Erro:", erro)
        elif op == "0":
            storage.salvar()
            break
        else:
            print("Opcao invalida")


if __name__ == "__main__":
    main()
