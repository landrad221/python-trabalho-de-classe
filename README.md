# Painel de Projetos e Tarefas

Aplicação web desenvolvida com Flask para organizar projetos e acompanhar suas tarefas. O sistema permite criar projetos, cadastrar tarefas com descrição e responsável, definir prioridades e atualizar o status de cada tarefa.

## Funcionalidades

- Criação de projetos
- Cadastro de tarefas com responsável e prioridade
- Prioridades: baixa, média e alta
- Status: pendente, em andamento e concluída
- Filtro de tarefas por status
- Resumo de quantidade e progresso do projeto
- Interface responsiva para computador e celular

## Tecnologias

- Python 3.10
- Flask 3
- HTML e CSS
- Testes com `unittest`

## Pré-requisitos

- Python 3.10 instalado
- Git, opcional, para clonar o repositório

No Windows, confira a versão do Python com:

```powershell
python --version
```

## Configuração no Windows

Abra o PowerShell na pasta do repositório e execute:

```powershell
cd "C:\caminho\python-trabalho-de-classe-main"

python -m venv .venv
.\.venv\Scripts\Activate.ps1

python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Se o PowerShell bloquear a ativação do ambiente virtual, habilite a execução apenas para a sessão atual:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

Também é possível iniciar o servidor de duas maneiras:

```powershell
python app.py
```

ou:

```powershell
flask --app app run --host 127.0.0.1 --port 8000
```

## Acesso no navegador

Com o servidor em execução, abra:

[http://127.0.0.1:8000](http://127.0.0.1:8000)

Para encerrar o servidor, pressione `Ctrl+C` no terminal.

## Executar os testes

Na pasta do projeto e com o ambiente virtual ativo:

```powershell
python -m unittest discover -s testes -p "test_*.py"
```

## Estrutura do projeto

```text
.
├── app.py                 # Aplicação Flask e rotas
├── requirements.txt       # Dependências Python
├── modelos/
│   ├── projeto.py         # Classe Projeto
│   └── tarefa.py          # Classes Tarefa, Prioridade e Status
├── servicos/
│   └── gerenciador.py     # Gerenciamento dos projetos em memória
├── templates/
│   └── index.html         # Interface web
└── testes/
    ├── test_app.py        # Teste da página web
    └── test_sistema.py    # Testes das regras do sistema
```

## Observações

Os projetos e tarefas são armazenados em memória. Os dados ficam disponíveis enquanto o servidor está aberto e são apagados ao reiniciar ou encerrar a aplicação. A aplicação não utiliza banco de dados ou armazenamento persistente neste momento.