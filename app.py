#!/usr/bin/env python3
"""Interface Flask para gerenciar projetos e tarefas."""

from flask import Flask, redirect, render_template, request, url_for

from modelos.tarefa import Prioridade, Status, Tarefa
from servicos.gerenciador import GerenciadorProjetos


HOST = "127.0.0.1"
PORTA = 8000
TAMANHO_MAXIMO_FORMULARIO = 1024 * 1024


def criar_app(gerenciador=None):
    aplicacao = Flask(__name__)
    aplicacao.config["MAX_CONTENT_LENGTH"] = TAMANHO_MAXIMO_FORMULARIO
    servico = gerenciador or GerenciadorProjetos()

    @aplicacao.get("/")
    def index():
        projetos = servico.listar_projetos()
        projeto_id = request.args.get("projeto", "")
        projeto = projetos[0] if projetos and not projeto_id else None
        erro = request.args.get("erro") or None
        status_code = 200

        if projeto_id:
            try:
                projeto = servico.buscar_projeto(projeto_id)
            except ValueError:
                erro = "Projeto não encontrado."
                projeto = projetos[0] if projetos else None
                status_code = 400

        filtro_status = None
        status_nome = request.args.get("status", "")
        if status_nome:
            try:
                filtro_status = Status[status_nome]
            except KeyError:
                erro = "Filtro de status inválido."
                status_code = 400

        todas_tarefas = (
            servico.consultar_tarefas(projeto.id)
            if projeto
            else []
        )
        tarefas = (
            [tarefa for tarefa in todas_tarefas if tarefa.status == filtro_status]
            if filtro_status
            else todas_tarefas
        )
        total = len(todas_tarefas)
        concluidas = sum(
            tarefa.status == Status.CONCLUIDA for tarefa in todas_tarefas
        )
        andamento = sum(
            tarefa.status == Status.ANDAMENTO for tarefa in todas_tarefas
        )
        progresso = round(concluidas / total * 100) if total else 0
        filtros = [(None, "Todas")] + [
            (status, status.value) for status in Status
        ]

        pagina = render_template(
            "index.html",
            projetos=projetos,
            projeto_selecionado=projeto,
            tarefas=tarefas,
            filtro_status=filtro_status,
            status_opcoes=Status,
            prioridades=Prioridade,
            filtros=filtros,
            total=total,
            andamento=andamento,
            concluidas=concluidas,
            progresso=progresso,
            erro=erro,
        )
        return pagina, status_code

    @aplicacao.post("/projetos")
    def criar_projeto():
        try:
            projeto = servico.criar_projeto(request.form.get("nome", "").strip())
        except ValueError as erro:
            return redirect(url_for("index", erro=str(erro)), code=303)
        return redirect(url_for("index", projeto=projeto.id), code=303)

    @aplicacao.post("/tarefas")
    def criar_tarefa():
        projeto_id = request.form.get("projeto_id", "").strip()
        try:
            projeto = servico.buscar_projeto(projeto_id)
        except ValueError as erro:
            return redirect(url_for("index", erro=str(erro)), code=303)

        try:
            prioridade = Prioridade[request.form.get("prioridade", "")]
        except KeyError:
            return redirect(
                url_for("index", projeto=projeto_id, erro="Prioridade inválida."),
                code=303,
            )

        try:
            tarefa = Tarefa(
                request.form.get("descricao", "").strip(),
                request.form.get("responsavel", "").strip(),
                prioridade,
            )
            projeto.adicionar_tarefa(tarefa)
        except (TypeError, ValueError) as erro:
            return redirect(
                url_for("index", projeto=projeto_id, erro=str(erro)),
                code=303,
            )
        return redirect(url_for("index", projeto=projeto_id), code=303)

    @aplicacao.post("/tarefas/status")
    def atualizar_status():
        projeto_id = request.form.get("projeto_id", "").strip()
        try:
            projeto = servico.buscar_projeto(projeto_id)
        except ValueError as erro:
            return redirect(url_for("index", erro=str(erro)), code=303)

        try:
            novo_status = Status[request.form.get("status", "")]
        except KeyError:
            return redirect(
                url_for("index", projeto=projeto_id, erro="Status inválido."),
                code=303,
            )

        try:
            tarefa = projeto.buscar_tarefa(
                request.form.get("tarefa_id", "").strip()
            )
            tarefa.alterar_status(novo_status)
        except ValueError as erro:
            return redirect(
                url_for("index", projeto=projeto_id, erro=str(erro)),
                code=303,
            )
        return redirect(url_for("index", projeto=projeto_id), code=303)

    return aplicacao


app = criar_app()


def main():
    print(f"Interface disponível em http://{HOST}:{PORTA}")
    app.run(host=HOST, port=PORTA, debug=False, threaded=True)


if __name__ == "__main__":
    main()
