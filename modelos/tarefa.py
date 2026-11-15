
from enum import Enum
from uuid import uuid4
# uso de Enum para definir prioridades e status das tarefas
# uso de uuid para gerar identificadores únicos para cada tarefa


class Prioridade(Enum):
    BAIXA = "Baixa"
    MEDIA = "Média"
    ALTA = "Alta"


class Status(Enum):
    PENDENTE = "Pendente"
    ANDAMENTO = "Em andamento"
    CONCLUIDA = "Concluída"


### cada tarefa possui uma descrição, responsável, prioridade e status
## descrição: string, responsável: string, prioridade: Prioridade, status: Status
class Tarefa:
    def __init__(self, descricao, responsavel, prioridade):
        if not descricao or not descricao.strip():
            raise ValueError("Descrição obrigatória")

        if not responsavel or not responsavel.strip():
            raise ValueError("Responsável obrigatório")

        if not isinstance(prioridade, Prioridade):
            raise ValueError("Prioridade inválida")

        self.id = str(uuid4())
        self.descricao = descricao
        self.responsavel = responsavel
        self.prioridade = prioridade
        self.status = Status.PENDENTE

    def alterar_status(self, novo_status):
        if not isinstance(novo_status, Status):
            raise ValueError("Status inválido")

        self.status = novo_status

    def __str__(self):
        return (
            f"{self.descricao} | "
            f"Responsável: {self.responsavel} | "
            f"Prioridade: {self.prioridade.value} | "
            f"Status: {self.status.value}"
        )
