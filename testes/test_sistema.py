
import unittest

from modelos.tarefa import Tarefa, Prioridade, Status
from modelos.projeto import Projeto
from servicos.gerenciador import GerenciadorProjetos


class TestSistema(unittest.TestCase):

    def test_cenario_valido(self):
        gerenciador = GerenciadorProjetos()
        projeto = gerenciador.criar_projeto("Projeto Teste")

        tarefa = Tarefa(
            "Criar login",
            "Maria",
            Prioridade.ALTA
        )

        projeto.adicionar_tarefa(tarefa)
        tarefa.alterar_status(Status.CONCLUIDA)

        resultado = gerenciador.consultar_tarefas(
            projeto.id, Status.CONCLUIDA
        )

        self.assertEqual(len(resultado), 1)
        self.assertEqual(resultado[0], tarefa)

    def test_descricao_invalida(self):
        with self.assertRaises(ValueError):
            Tarefa("", "João", Prioridade.ALTA)

    def test_status_invalido(self):
        tarefa = Tarefa(
            "Criar tela",
            "Ana",
            Prioridade.BAIXA
        )

        with self.assertRaises(ValueError):
            tarefa.alterar_status("Finalizada")

    def test_projeto_inexistente(self):
        gerenciador = GerenciadorProjetos()

        with self.assertRaises(ValueError):
            gerenciador.buscar_projeto("id-invalido")


if __name__ == "__main__":
    unittest.main()
