#!/usr/bin/env python3
from modelos.tarefa import Tarefa, Prioridade, Status
from servicos.gerenciador import GerenciadorProjetos


def exibir_tarefas(tarefas):
    if not tarefas:
        print("Nenhuma tarefa encontrada")
        return

    for tarefa in tarefas:
        print(tarefa)


def main():
    gerenciador = GerenciadorProjetos()

    projeto = gerenciador.criar_projeto("Sistema Web")

    tarefa1 = Tarefa(
        "Criar interface",
        "Ana",
        Prioridade.ALTA
    )

    tarefa2 = Tarefa(
        "Implementar banco de dados",
        "Carlos",
        Prioridade.MEDIA
    )

    projeto.adicionar_tarefa(tarefa1)
    projeto.adicionar_tarefa(tarefa2)

    print("=== TAREFAS DO PROJETO ===")
    exibir_tarefas(
        gerenciador.consultar_tarefas(projeto.id)
    )

    tarefa1.alterar_status(Status.ANDAMENTO)

    print("\n=== TAREFAS EM ANDAMENTO ===")
    exibir_tarefas(
        gerenciador.consultar_tarefas(
            projeto.id, Status.ANDAMENTO
        )
    )


if __name__ == "__main__":
    main()
