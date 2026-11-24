#!/usr/bin/env python3
"""Ponto de entrada: Tkinter por padrão, Flask sob demanda."""
import argparse
from interfaces.tkinter import InterfaceTkinter
from interfaces.web import criar_app
from servicos.gerenciador import GerenciadorProjetos


def main():
    parser = argparse.ArgumentParser(description="Painel de projetos e tarefas")
    parser.add_argument("--web", action="store_true", help="inicia a interface web Flask")
    args = parser.parse_args()
    gerenciador = GerenciadorProjetos()
    if args.web:
        print("Interface disponível em http://127.0.0.1:8000")
        criar_app(gerenciador).run(host="127.0.0.1", port=8000, debug=False, threaded=True)
    else:
        InterfaceTkinter().executar(gerenciador)


# Compatibilidade com consumidores que importam app para usar test_client().
app = criar_app()

if __name__ == "__main__":
    main()
