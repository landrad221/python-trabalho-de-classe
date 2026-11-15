
from modelos.projeto import Projeto

class GerenciadorProjetos:
    def __init__(self):
        self._projetos = {}

    def criar_projeto(self, nome):
        projeto = Projeto(nome)
        self._projetos[projeto.id] = projeto
        return projeto

    def buscar_projeto(self, projeto_id):
        if projeto_id not in self._projetos:
            raise ValueError("Projeto não encontrado")

        return self._projetos[projeto_id]

    def listar_projetos(self):
        return list(self._projetos.values())

    def consultar_tarefas(self, projeto_id, status=None):
        projeto = self.buscar_projeto(projeto_id)
        return projeto.listar_tarefas(status)
