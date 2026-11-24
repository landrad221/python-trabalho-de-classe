# Painel de Projetos e Tarefas

Aplicação Python para organizar projetos e acompanhar tarefas. A interface gráfica Tkinter é a opção padrão; a interface web original, construída com Flask, continua disponível como alternativa.

## Funcionalidades

- Criação e seleção de projetos
- Cadastro de tarefas com descrição, responsável e prioridade
- Prioridades: baixa, média e alta
- Status: pendente, em andamento e concluída
- Atualização do status das tarefas
- Interface desktop Tkinter e interface web Flask

## Requisitos

- Python 3.10 ou superior
- Tkinter (normalmente incluído no Python; em distribuições Linux pode exigir instalação do pacote do sistema, como python-tk ou tk)
- Flask 3 para executar a interface web

## Instalação

```bash
python -m venv .venv
# Linux/macOS: source .venv/bin/activate
# Windows PowerShell: .venv\\Scripts\\Activate.ps1
python -m pip install -r requirements.txt
```

## Executar

A interface Tkinter inicia por padrão:

```bash
python app.py
```

Para iniciar a interface web Flask:

```bash
python app.py --web
```

Acesse http://127.0.0.1:8000. As duas interfaces utilizam o mesmo serviço de gerenciamento e não dependem uma da outra.

## Testes

```bash
python -m unittest discover -s testes -p "test_*.py"
```

## Estrutura

```text
.
├── app.py
├── interfaces/
│   ├── base.py
│   ├── tkinter.py
│   ├── web.py
│   └── templates/index.html
├── modelos/
├── servicos/
└── testes/
```

## Armazenamento

Projetos e tarefas são mantidos em memória. Os dados são perdidos ao encerrar a aplicação; não há persistência nesta versão.
