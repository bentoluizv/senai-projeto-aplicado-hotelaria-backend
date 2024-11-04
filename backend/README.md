# Gestão Simplificada para Hotéis

Projeto Aplicado dos alunos da segunda fase de Análise e Desenvolvimento de Sistemas do SENAI em Florianópolis.

O projeto é baseado na demanda da indústria publicada na plataforma [SAGA](https://) do SENAI pela empresa Quinta do Ypuã com o objetivo de criar uma solução para o gerenciamento simplificado de hospedagens.

Este reposítório representa o backend do projeto escrito com Python utilizando Fastapi.

## Configurando o ambiente de desenvolvimento

### Instale Python 3.12.3

Você pode baixar python diretamente do site oficial mas é altamente recomendado usar um gerenciador de versão como o [pyenv](https://github.com/pyenv/pyenv) e o [pyenv-win](https://https://github.com/pyenv-win/pyenv-win).

Com o pyenv instalado você poderá instalar a versão do python adequada da seguinte forma:

```sh
pyenv install 3.12.5
Downloading Python-3.12.5.tar.xz...
-> https://www.python.org/ftp/python/3.12.5/Python-3.12.5.tar.xz
Installing Python-3.12.5...
```

### Clone o projeto diretamente do Github

```bash
  git clone https://github.com/bentoluizv/projeto-aplicado-backend
  cd ./projeto-aplicado-backend
```

### Ambiente virtual e gerenciamento de dependências

O projeto utiliza o [Poetry](https://python-poetry.org/) para criar um ambiente virtual e fazer a gestão de dependencias do projeto. Com o poetry utilize o comando `shell` para ativar o ambiente virutal e `install` para instalar as dependencias localizadas no arquivo `pyproject.toml`

```sh
poetry shell
The currently activated Python version 3.10.12 is not supported by the project (3.12.3).
Trying to find and use a compatible version.
Using python3 (3.12.3)
Spawning shell within /.cache/pypoetry/virtualenvs/app-kWK05R3W-py3.12
. /.cache/pypoetry/virtualenvs/app-kWK05R3W-py3.12/bin/activate

:~/$ ./.cache/pypoetry/virtualenvs/app-kWK05R3W-py3.12/bin/activate


(app-py3.12) :~/$
```

```sh
poetry install
Installing dependencies from lock file

Package operations: 0 installs, 8 updates, 0 removals

  - Updating pyyaml (6.0.1 -> 6.0.2)
  - Updating uvloop (0.19.0 -> 0.20.0)
  - Updating watchfiles (0.22.0 -> 0.23.0)
  - Updating typer (0.12.3 -> 0.12.4)
  - Updating uvicorn (0.30.1 -> 0.30.6)
  - Updating coverage (7.5.4 -> 7.6.1)
  - Updating fastapi-cli (0.0.4 -> 0.0.5)
  - Updating orjson (3.10.6 -> 3.10.7)

Installing the current project: app (0.1.0)
```

### O arquivo pyproject.toml

#### Info e dependências

```bash
[tool.poetry]
name = "app"
version = "0.1.0"
description = "Hotel booking system"
authors = ["bentoluizv <bentoluizv@gmail.com>"]
readme = "README.md"

[tool.poetry.dependencies]
python = "3.12.3"
pydantic = "2.7.4"
fastapi = "0.111.0"
sqlalchemy = "2.0.31"


[tool.poetry.group.dev.dependencies]
pytest = "8.2.2"
pytest-cov = "5.0.0"
taskipy = "1.13.0"
ruff = "0.4.9"
httpx = "0.27.0"
```

#### Boas práticas na escrita do código com ruff

```sh
[tool.ruff]
line-length = 79
extend-exclude = ['migrations']

[tool.ruff.lint]
preview = true
select = ['I', 'F', 'E', 'W', 'PL', 'PT']

[tool.ruff.format]
preview = true
quote-style = 'single'
```

#### Automatizando comandos com taskipy

```sh
[tool.taskipy.tasks]
lint = 'ruff check . && ruff check . --diff'
format = 'ruff check . --fix && ruff format .'
dev = 'fastapi dev app/api/main.py'
pre_test = 'task lint'
test = 'pytest -s -x --cov=app -vv'
post_test = 'coverage html'
run = 'fastapi run app/api/main.py'
```

Para rodar qualquer comando não esqueça de ativar o ambiente virutal e apenas digite `task <command>`.

### Testes com pytest

O projeto utiliza pytest para rodar testes de integração que cobrem operações com o banco de dado e endpoints da api.

Os testes podem ser executados de forma automatizada gerando coverage report e também checando o linter através do comando `task test`

```sh
configfile: pyproject.toml
plugins: cov-5.0.0, anyio-4.4.0
collected 18 items

tests/integration/test_api_accommodation.py sssss
tests/integration/test_api_bookings.py ssssss
tests/integration/test_api_guests.py sssss
tests/integration/test_db.py ..

---------- coverage: platform linux, python 3.12.3-final-0 -----------
Name                            Stmts   Miss  Cover
---------------------------------------------------
app/__init__.py                     0      0   100%
app/app.py                          9      0   100%
app/infra/database/db.py            8      2    75%
app/infra/database/models.py       52      0   100%
app/routers/__init__.py             0      0   100%
app/routers/accommodation.py       17      0   100%
app/routers/amenities.py            8      0   100%
app/routers/booking.py             17      0   100%
app/routers/guests.py              22      0   100%
app/schemas/Accommodation.py       17      0   100%
app/schemas/Booking.py             20      0   100%
app/schemas/Guest.py               13      0   100%
app/utils/generate_locator.py       7      0   100%
---------------------------------------------------
TOTAL                             190      2    99%


================================================== 2 passed, 16 skipped in 2.21s ==================================================
Wrote HTML report to htmlcov/index.html
```

## Rodando o projeto

Com o projeto configurado e testes passando digite o comando `task dev` para executar o servidor no modo desenvolvimento e `task run` para o modo de produção.

```sh
task dev
INFO     Using path app/api/main.py
INFO     Resolved absolute path /home/bentoluizv/workspace/projetoaplicado1/teste/projeto-aplicado-backend/app/api/main.py
INFO     Searching for package file structure from directories with __init__.py files
INFO     Importing from /home/bentoluizv/workspace/projetoaplicado1/teste/projeto-aplicado-backend/app

 ╭─ Python package file structure ─╮
 │                                 │
 │  📁 api                         │
 │  ├── 🐍 __init__.py             │
 │  └── 🐍 main.py                 │
 │                                 │
 ╰─────────────────────────────────╯

INFO     Importing module api.main
INFO     Found importable FastAPI app

 ╭── Importable FastAPI app ──╮
 │                            │
 │  from api.main import app  │
 │                            │
 ╰────────────────────────────╯

INFO     Using import string api.main:app

 ╭────────── FastAPI CLI - Development mode ───────────╮
 │                                                     │
 │  Serving at: http://127.0.0.1:8000                  │
 │                                                     │
 │  API docs: http://127.0.0.1:8000/docs               │
 │                                                     │
 │  Running in development mode, for production use:   │
 │                                                     │
 │  fastapi run                                        │
 │                                                     │
 ╰─────────────────────────────────────────────────────╯

INFO:     Will watch for changes in these directories: ['/home/bentoluizv/workspace/projetoaplicado1/teste/projeto-aplicado-backend']
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [126321] using WatchFiles
INFO:     Started server process [126394]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```
