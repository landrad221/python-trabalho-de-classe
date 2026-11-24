import unittest
from interfaces.web import criar_app


class TestAplicacaoWeb(unittest.TestCase):
    def test_pagina_inicial(self):
        resposta = criar_app().test_client().get("/")
        self.assertEqual(resposta.status_code, 200)


if __name__ == "__main__":
    unittest.main()
