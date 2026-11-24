"""Interface web Flask, isolada da interface desktop."""
from flask import Flask, redirect, render_template, request, url_for
from interfaces.base import Interface
from modelos.tarefa import Prioridade, Status, Tarefa
from servicos.gerenciador import GerenciadorProjetos

HOST, PORTA = "127.0.0.1", 8000


class InterfaceWeb(Interface):
    def criar_app(self, gerenciador=None):
        aplicacao = Flask(__name__, template_folder="templates")
        aplicacao.config["MAX_CONTENT_LENGTH"] = 1024 * 1024
        servico = gerenciador or GerenciadorProjetos()

        @aplicacao.get("/")
        def index():
            projetos = servico.listar_projetos()
            projeto_id = request.args.get("projeto", "")
            projeto = projetos[0] if projetos and not projeto_id else None
            erro = request.args.get("erro") or None
            status_code = 200
            if projeto_id:
                try: projeto = servico.buscar_projeto(projeto_id)
                except ValueError:
                    erro, projeto, status_code = "Projeto não encontrado.", (projetos[0] if projetos else None), 400
            filtro_status = None
            if request.args.get("status"):
                try: filtro_status = Status[request.args["status"]]
                except KeyError: erro, status_code = "Filtro de status inválido.", 400
            todas = servico.consultar_tarefas(projeto.id) if projeto else []
            tarefas = [t for t in todas if t.status == filtro_status] if filtro_status else todas
            total = len(todas)
            concluidas = sum(t.status == Status.CONCLUIDA for t in todas)
            andamento = sum(t.status == Status.ANDAMENTO for t in todas)
            progresso = round(concluidas / total * 100) if total else 0
            pagina = render_template("index.html", projetos=projetos, projeto_selecionado=projeto, tarefas=tarefas,
                filtro_status=filtro_status, status_opcoes=Status, prioridades=Prioridade,
                filtros=[(None, "Todas")] + [(s, s.value) for s in Status], total=total,
                andamento=andamento, concluidas=concluidas, progresso=progresso, erro=erro)
            return pagina, status_code

        @aplicacao.post("/projetos")
        def criar_projeto():
            try: projeto = servico.criar_projeto(request.form.get("nome", "").strip())
            except ValueError as erro: return redirect(url_for("index", erro=str(erro)), code=303)
            return redirect(url_for("index", projeto=projeto.id), code=303)

        @aplicacao.post("/tarefas")
        def criar_tarefa():
            projeto_id = request.form.get("projeto_id", "").strip()
            try: projeto = servico.buscar_projeto(projeto_id)
            except ValueError as erro: return redirect(url_for("index", erro=str(erro)), code=303)
            try: prioridade = Prioridade[request.form.get("prioridade", "")]
            except KeyError: return redirect(url_for("index", projeto=projeto_id, erro="Prioridade inválida."), code=303)
            try:
                tarefa = Tarefa(request.form.get("descricao", "").strip(), request.form.get("responsavel", "").strip(), prioridade)
                projeto.adicionar_tarefa(tarefa)
            except (TypeError, ValueError) as erro: return redirect(url_for("index", projeto=projeto_id, erro=str(erro)), code=303)
            return redirect(url_for("index", projeto=projeto_id), code=303)

        @aplicacao.post("/tarefas/status")
        def atualizar_status():
            projeto_id = request.form.get("projeto_id", "").strip()
            try: projeto = servico.buscar_projeto(projeto_id)
            except ValueError as erro: return redirect(url_for("index", erro=str(erro)), code=303)
            try: status = Status[request.form.get("status", "")]
            except KeyError: return redirect(url_for("index", projeto=projeto_id, erro="Status inválido."), code=303)
            try:
                tarefa = projeto.buscar_tarefa(request.form.get("tarefa_id", "").strip())
                tarefa.alterar_status(status)
            except ValueError as erro: return redirect(url_for("index", projeto=projeto_id, erro=str(erro)), code=303)
            return redirect(url_for("index", projeto=projeto_id), code=303)
        return aplicacao

    def executar(self, gerenciador):
        print(f"Interface disponível em http://{HOST}:{PORTA}")
        self.criar_app(gerenciador).run(host=HOST, port=PORTA, debug=False, threaded=True)


def criar_app(gerenciador=None):
    return InterfaceWeb().criar_app(gerenciador)


app = criar_app()
