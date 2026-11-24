"""Interface desktop baseada em Tkinter."""
import tkinter as tk
from tkinter import messagebox, ttk

from interfaces.base import Interface
from modelos.tarefa import Prioridade, Status, Tarefa


class InterfaceTkinter(Interface):
    def executar(self, gerenciador):
        self.gerenciador = gerenciador
        self.root = tk.Tk()
        self.root.title("Painel de Projetos e Tarefas")
        self.root.geometry("980x640")
        self.root.minsize(760, 500)
        self._montar_tela()
        self._atualizar_projetos()
        self.root.mainloop()

    def _montar_tela(self):
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        principal = ttk.Frame(self.root, padding=16)
        principal.grid(sticky="nsew")
        principal.columnconfigure(0, weight=1)
        principal.columnconfigure(1, weight=2)
        principal.rowconfigure(1, weight=1)
        ttk.Label(principal, text="Painel de projetos e tarefas", font=("TkDefaultFont", 18, "bold")).grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 16))

        esquerda = ttk.LabelFrame(principal, text="Projetos", padding=12)
        esquerda.grid(row=1, column=0, sticky="nsew", padx=(0, 10))
        esquerda.columnconfigure(0, weight=1)
        esquerda.rowconfigure(1, weight=1)
        self.nome_projeto = tk.StringVar()
        ttk.Entry(esquerda, textvariable=self.nome_projeto).grid(row=0, column=0, sticky="ew")
        ttk.Button(esquerda, text="Criar projeto", command=self._criar_projeto).grid(row=0, column=1, padx=(6, 0))
        self.lista_projetos = tk.Listbox(esquerda, exportselection=False)
        self.lista_projetos.grid(row=1, column=0, columnspan=2, sticky="nsew", pady=(10, 0))
        self.lista_projetos.bind("<<ListboxSelect>>", self._selecionar_projeto)

        direita = ttk.Frame(principal)
        direita.grid(row=1, column=1, sticky="nsew")
        direita.columnconfigure(0, weight=1)
        direita.rowconfigure(0, weight=1)
        quadro = ttk.LabelFrame(direita, text="Tarefas do projeto", padding=12)
        quadro.grid(row=0, column=0, sticky="nsew")
        quadro.columnconfigure(0, weight=1)
        quadro.rowconfigure(0, weight=1)
        colunas = ("descricao", "responsavel", "prioridade", "status")
        self.tabela = ttk.Treeview(quadro, columns=colunas, show="headings")
        for col, titulo, largura in [("descricao", "Descrição", 230), ("responsavel", "Responsável", 120), ("prioridade", "Prioridade", 90), ("status", "Status", 110)]:
            self.tabela.heading(col, text=titulo)
            self.tabela.column(col, width=largura, anchor="w")
        self.tabela.grid(row=0, column=0, sticky="nsew")
        scroll = ttk.Scrollbar(quadro, orient="vertical", command=self.tabela.yview)
        scroll.grid(row=0, column=1, sticky="ns")
        self.tabela.configure(yscrollcommand=scroll.set)

        form = ttk.LabelFrame(direita, text="Nova tarefa / status", padding=12)
        form.grid(row=1, column=0, sticky="ew", pady=(12, 0))
        for i in range(3): form.columnconfigure(i, weight=1)
        self.descricao = tk.StringVar()
        self.responsavel = tk.StringVar()
        self.prioridade = tk.StringVar(value=Prioridade.MEDIA.name)
        self.status = tk.StringVar(value=Status.PENDENTE.name)
        ttk.Label(form, text="Descrição").grid(row=0, column=0, sticky="w")
        ttk.Entry(form, textvariable=self.descricao).grid(row=1, column=0, sticky="ew", padx=(0, 6))
        ttk.Label(form, text="Responsável").grid(row=0, column=1, sticky="w")
        ttk.Entry(form, textvariable=self.responsavel).grid(row=1, column=1, sticky="ew", padx=(0, 6))
        ttk.Label(form, text="Prioridade").grid(row=0, column=2, sticky="w")
        ttk.Combobox(form, textvariable=self.prioridade, values=[p.name for p in Prioridade], state="readonly").grid(row=1, column=2, sticky="ew")
        ttk.Button(form, text="Adicionar tarefa", command=self._criar_tarefa).grid(row=2, column=0, sticky="ew", pady=(10, 0))
        ttk.Label(form, text="Novo status").grid(row=2, column=1, sticky="w", padx=(6, 0), pady=(10, 0))
        ttk.Combobox(form, textvariable=self.status, values=[s.name for s in Status], state="readonly").grid(row=3, column=1, sticky="ew", padx=(6, 0))
        ttk.Button(form, text="Atualizar tarefa selecionada", command=self._atualizar_status).grid(row=3, column=2, sticky="ew", pady=(4, 0))
        self.projeto_atual = None
        self.tarefas_por_id = {}

    def _projeto_selecionado(self):
        selecionados = self.lista_projetos.curselection()
        projetos = self.gerenciador.listar_projetos()
        return projetos[selecionados[0]] if selecionados and selecionados[0] < len(projetos) else None

    def _atualizar_projetos(self, projeto_id=None):
        projetos = self.gerenciador.listar_projetos()
        self.lista_projetos.delete(0, tk.END)
        indice = 0
        for i, projeto in enumerate(projetos):
            self.lista_projetos.insert(tk.END, projeto.nome)
            if projeto.id == projeto_id: indice = i
        if projetos:
            self.lista_projetos.selection_set(indice)
            self.lista_projetos.event_generate("<<ListboxSelect>>")
        else:
            self.projeto_atual = None
            self._mostrar_tarefas([])

    def _selecionar_projeto(self, _evento=None):
        self.projeto_atual = self._projeto_selecionado()
        self._mostrar_tarefas(self.projeto_atual.listar_tarefas() if self.projeto_atual else [])

    def _mostrar_tarefas(self, tarefas):
        for item in self.tabela.get_children(): self.tabela.delete(item)
        self.tarefas_por_id = {}
        for tarefa in tarefas:
            self.tabela.insert("", "end", iid=tarefa.id, values=(tarefa.descricao, tarefa.responsavel, tarefa.prioridade.value, tarefa.status.value))
            self.tarefas_por_id[tarefa.id] = tarefa

    def _criar_projeto(self):
        try: projeto = self.gerenciador.criar_projeto(self.nome_projeto.get().strip())
        except ValueError as erro:
            messagebox.showerror("Projeto inválido", str(erro), parent=self.root)
            return
        self.nome_projeto.set("")
        self._atualizar_projetos(projeto.id)

    def _criar_tarefa(self):
        if not self.projeto_atual:
            messagebox.showwarning("Selecione um projeto", "Crie ou selecione um projeto primeiro.", parent=self.root)
            return
        try:
            tarefa = Tarefa(self.descricao.get().strip(), self.responsavel.get().strip(), Prioridade[self.prioridade.get()])
            self.projeto_atual.adicionar_tarefa(tarefa)
        except (KeyError, TypeError, ValueError) as erro:
            messagebox.showerror("Tarefa inválida", str(erro), parent=self.root)
            return
        self.descricao.set("")
        self.responsavel.set("")
        self._selecionar_projeto()

    def _atualizar_status(self):
        selecionados = self.tabela.selection()
        if not selecionados:
            messagebox.showwarning("Selecione uma tarefa", "Escolha uma tarefa na lista.", parent=self.root)
            return
        try: self.tarefas_por_id[selecionados[0]].alterar_status(Status[self.status.get()])
        except (KeyError, ValueError) as erro:
            messagebox.showerror("Status inválido", str(erro), parent=self.root)
            return
        self._selecionar_projeto()
