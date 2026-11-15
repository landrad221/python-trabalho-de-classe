
## import da biblioteca uuid para gerar identificadores únicos
from uuid import uuid4

# import da classe Tarefa do módulo modelos.tarefa
from modelos.tarefa import Tarefa

### definição da classe Projeto para representar um projeto com tarefas
class Projeto:
    def __init__(self, nome):
        if not nome or not nome.strip():
            raise ValueError("Nome do projeto obrigatório")

        self.id = str(uuid4())
        self.nome = nome
        self._tarefas = []

    def adicionar_tarefa(self, tarefa):
        if not isinstance(tarefa, Tarefa):
            raise TypeError("Objeto deve ser uma Tarefa")

        self._tarefas.append(tarefa)

    def listar_tarefas(self, status=None):
        if status is None:
            return list(self._tarefas)

        return [
            tarefa for tarefa in self._tarefas
            if tarefa.status == status
        ]

    def buscar_tarefa(self, tarefa_id):
        for tarefa in self._tarefas:
            if tarefa.id == tarefa_id:
                return tarefa

        raise ValueError("Tarefa não encontrada")
