"use strict";

// ---------- utilitarios ----------

const $ = (sel) => document.querySelector(sel);

async function api(caminho, opcoes = {}) {
  const resp = await fetch("/api" + caminho, {
    headers: { "Content-Type": "application/json" },
    ...opcoes,
    body: opcoes.body ? JSON.stringify(opcoes.body) : undefined,
  });
  const dados = await resp.json().catch(() => ({}));
  if (!resp.ok) throw new Error(dados.erro || `Erro ${resp.status}`);
  return dados;
}

let timerAviso;
function avisar(msg, tipo = "ok") {
  const el = $("#aviso");
  el.textContent = msg;
  el.className = `aviso visivel ${tipo}`;
  clearTimeout(timerAviso);
  timerAviso = setTimeout(() => el.classList.remove("visivel"), 3500);
}

function esc(v) {
  return String(v ?? "").replace(/[&<>"']/g, (c) => ({
    "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;",
  })[c]);
}

function dataBR(iso) {
  if (!iso) return "—";
  const [a, m, d] = iso.split("-");
  return `${d}/${m}/${a}`;
}

function hojeISO() {
  const h = new Date();
  return new Date(h.getTime() - h.getTimezoneOffset() * 60000).toISOString().slice(0, 10);
}

function linhaVazia(colunas, texto) {
  return `<tr class="vazio"><td colspan="${colunas}">${texto}</td></tr>`;
}

function dadosForm(form) {
  return Object.fromEntries(new FormData(form).entries());
}

// ---------- abas ----------

document.querySelectorAll(".aba").forEach((botao) => {
  botao.addEventListener("click", () => {
    document.querySelectorAll(".aba").forEach((b) => b.classList.toggle("ativa", b === botao));
    document.querySelectorAll(".painel").forEach((p) =>
      p.classList.toggle("ativo", p.id === `aba-${botao.dataset.aba}`));
    carregarAba(botao.dataset.aba);
  });
});

function carregarAba(aba) {
  const acoes = {
    livros: carregarLivros,
    usuarios: carregarUsuarios,
    emprestimos: carregarEmprestimos,
    resumo: carregarResumo,
  };
  acoes[aba]().catch((e) => avisar(e.message, "erro"));
}

// ---------- livros ----------

async function carregarLivros() {
  const termo = $("#busca-livro").value.trim();
  const lista = await api("/livros" + (termo ? `?q=${encodeURIComponent(termo)}` : ""));
  $("#tabela-livros").innerHTML = lista.length
    ? lista.map((l) => `
      <tr>
        <td>${l.id}</td>
        <td class="titulo">${esc(l.titulo)}</td>
        <td>${esc(l.autor)}</td>
        <td>${esc(l.ano)}</td>
        <td><span class="selo ${l.disponiveis > 0 ? "ok" : "neutro"}">${l.disponiveis} / ${l.copias}</span></td>
        <td><button class="secundario perigo" data-remover="${l.id}">Remover</button></td>
      </tr>`).join("")
    : linhaVazia(6, termo ? "Nenhum livro encontrado" : "Nenhum livro cadastrado");
}

let timerBusca;
$("#busca-livro").addEventListener("input", () => {
  clearTimeout(timerBusca);
  timerBusca = setTimeout(() => carregarLivros().catch((e) => avisar(e.message, "erro")), 200);
});

$("#tabela-livros").addEventListener("click", async (ev) => {
  const id = ev.target.dataset.remover;
  if (!id || !confirm("Remover este livro do acervo?")) return;
  try {
    await api(`/livros/${id}`, { method: "DELETE" });
    avisar("Livro removido");
    carregarLivros();
  } catch (e) { avisar(e.message, "erro"); }
});

$("#form-livro").addEventListener("submit", async (ev) => {
  ev.preventDefault();
  const d = dadosForm(ev.target);
  try {
    const l = await api("/livros", {
      method: "POST",
      body: { ...d, ano: Number(d.ano), copias: Number(d.copias) },
    });
    avisar(`Livro cadastrado com id ${l.id}`);
    ev.target.reset();
    carregarLivros();
  } catch (e) { avisar(e.message, "erro"); }
});

// ---------- usuarios ----------

async function carregarUsuarios() {
  const [lista, emps] = await Promise.all([api("/usuarios"), api("/emprestimos")]);
  const ativos = {};
  emps.filter((e) => !e.devolvido_em).forEach((e) => {
    ativos[e.usuario_id] = (ativos[e.usuario_id] || 0) + 1;
  });
  $("#tabela-usuarios").innerHTML = lista.length
    ? lista.map((u) => `
      <tr>
        <td>${u.id}</td>
        <td class="titulo">${esc(u.nome)}</td>
        <td>${esc(u.email)}</td>
        <td>${ativos[u.id] || 0}</td>
      </tr>`).join("")
    : linhaVazia(4, "Nenhum usuário cadastrado");
}

$("#form-usuario").addEventListener("submit", async (ev) => {
  ev.preventDefault();
  try {
    const u = await api("/usuarios", { method: "POST", body: dadosForm(ev.target) });
    avisar(`Usuário cadastrado com id ${u.id}`);
    ev.target.reset();
    carregarUsuarios();
  } catch (e) { avisar(e.message, "erro"); }
});

// ---------- emprestimos ----------

async function carregarEmprestimos() {
  const [emps, users, books] = await Promise.all([
    api("/emprestimos"), api("/usuarios"), api("/livros"),
  ]);

  const selU = $("#form-emprestimo [name=usuario_id]");
  const selL = $("#form-emprestimo [name=livro_id]");
  selU.innerHTML = `<option value="">Selecione…</option>` +
    users.map((u) => `<option value="${u.id}">${u.id} — ${esc(u.nome)}</option>`).join("");
  selL.innerHTML = `<option value="">Selecione…</option>` +
    books.map((l) => `<option value="${l.id}">${l.id} — ${esc(l.titulo)} (${l.disponiveis}/${l.copias})</option>`).join("");

  const hoje = hojeISO();
  const soAtivos = $("#so-ativos").checked;
  const lista = emps.filter((e) => !soAtivos || !e.devolvido_em).reverse();

  $("#tabela-emprestimos").innerHTML = lista.length
    ? lista.map((e) => {
      let selo;
      if (e.devolvido_em) selo = `<span class="selo neutro">Devolvido ${dataBR(e.devolvido_em)}</span>`;
      else if (e.data_prevista < hoje) selo = `<span class="selo atraso">Atrasado</span>`;
      else selo = `<span class="selo ok">No prazo</span>`;
      return `
      <tr>
        <td>${e.id}</td>
        <td class="titulo">${esc(e.livro_titulo ?? `#${e.livro_id} (removido)`)}</td>
        <td>${esc(e.usuario_nome ?? `#${e.usuario_id}`)}</td>
        <td>${dataBR(e.data_emprestimo)}</td>
        <td>${dataBR(e.data_prevista)}</td>
        <td>${selo}</td>
        <td>${e.devolvido_em ? "" : `<button class="secundario" data-devolver="${e.id}">Devolver</button>`}</td>
      </tr>`;
    }).join("")
    : linhaVazia(7, soAtivos ? "Nenhum empréstimo ativo" : "Nenhum empréstimo registrado");
}

$("#so-ativos").addEventListener("change", () =>
  carregarEmprestimos().catch((e) => avisar(e.message, "erro")));

$("#form-emprestimo").addEventListener("submit", async (ev) => {
  ev.preventDefault();
  const d = dadosForm(ev.target);
  try {
    const e = await api("/emprestimos", {
      method: "POST",
      body: { usuario_id: Number(d.usuario_id), livro_id: Number(d.livro_id) },
    });
    avisar(`Empréstimo ${e.id} — devolver até ${dataBR(e.data_prevista)}`);
    carregarEmprestimos();
  } catch (e) { avisar(e.message, "erro"); }
});

$("#tabela-emprestimos").addEventListener("click", async (ev) => {
  const id = ev.target.dataset.devolver;
  if (!id) return;
  try {
    const { multa } = await api(`/emprestimos/${id}/devolucao`, { method: "POST" });
    if (multa > 0) avisar(`Devolvido com multa de R$ ${multa.toFixed(2).replace(".", ",")}`, "alerta");
    else avisar("Devolvido sem multa");
    carregarEmprestimos();
  } catch (e) { avisar(e.message, "erro"); }
});

// ---------- resumo ----------

async function carregarResumo() {
  const r = await api("/resumo");
  const ocup = r.ocupacao == null ? "—" : `${r.ocupacao.toFixed(1).replace(".", ",")}%`;
  const cards = [
    ["Exemplares", r.exemplares],
    ["Disponíveis", r.disponiveis],
    ["Empréstimos ativos", r.emprestimos_ativos],
    ["Encerrados", r.emprestimos_encerrados],
    ["Atrasados", r.atrasados.length],
    ["Ocupação", ocup],
  ];
  $("#numeros").innerHTML = cards.map(([rot, val]) =>
    `<div class="numero"><div class="valor">${val}</div><div class="rotulo">${rot}</div></div>`).join("");

  const mais = r.mais_emprestados;
  $("#mais-emprestados").innerHTML = mais == null
    ? `<li class="qtd">Não foi possível calcular (livro emprestado foi removido)</li>`
    : mais.length
      ? mais.map((m) => `<li>${esc(m.titulo)} <span class="qtd">— ${m.quantidade}×</span></li>`).join("")
      : `<li class="qtd">Nenhum empréstimo ainda</li>`;

  $("#tabela-atrasados").innerHTML = r.atrasados.length
    ? r.atrasados.map((e) => `
      <tr>
        <td class="titulo">${esc(e.livro_titulo ?? `#${e.livro_id}`)}</td>
        <td>${esc(e.usuario_nome ?? `#${e.usuario_id}`)}</td>
        <td>${dataBR(e.data_prevista)}</td>
      </tr>`).join("")
    : linhaVazia(3, "Nenhum empréstimo atrasado");
}

// ---------- inicio ----------

carregarAba("livros");
