import unittest

from app import app


class TestAplicacaoWeb(unittest.TestCase):
    def test_pagina_inicial(self):
        resposta = app.test_client().get("/")

        self.assertEqual(resposta.status_code, 200)


if __name__ == "__main__":
    unittest.main()
