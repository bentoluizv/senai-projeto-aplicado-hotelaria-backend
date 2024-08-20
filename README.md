# Gestão Simplificada para Hotéis

Projeto Aplicado dos alunos da segunda fase de Análise e Desenvolvimento de Sistemas do SENAI em Florianópolis.

O projeto é baseado na demanda da indústria publicada na plataforma [SAGA](https://) do SENAI pela empresa Quinta do Ypuã com o objetivo de criar uma solução para o gerenciamento simplificado de hospedagens.

Este reposítório representa o backend do projeto escrito com Python utilizando Fastapi.

## Configurando o ambiente de desenvolvimento

### Instale Python 3.12.3

Você pode baixar python diretamente do site oficial mas é altamente recomendado usar um gerenciador de versão como o [pyenv](https://github.com/pyenv/pyenv) e o [pyenv-win](https://https://github.com/pyenv-win/pyenv-win).

Com o pyenv instalado você poderá instalar a versão do python adequada da seguinte forma:

```sh
pyenv install 3.12.3
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
Spawning shell within /home/bentoluizv/.cache/pypoetry/virtualenvs/app-kWK05R3W-py3.12
. /home/bentoluizv/.cache/pypoetry/virtualenvs/app-kWK05R3W-py3.12/bin/activate

bentoluizv@DESKTOPD5OD07S:~/$ ./home/bentoluizv/.cache/pypoetry/virtualenvs/app-kWK05R3W-py3.12/bin/activate


(app-py3.12) bentoluizv@DESKTOPD5OD07S:~/$
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
All checks passed!
============================================================================================== test session starts ==============================================================================================
platform linux -- Python 3.12.3, pytest-8.2.2, pluggy-1.5.0 -- /home/bentoluizv/.cache/pypoetry/virtualenvs/app-kWK05R3W-py3.12/bin/python
cachedir: .pytest_cache
rootdir: /home/bentoluizv/workspace/projetoaplicado1/teste/projeto-aplicado-backend
configfile: pyproject.toml
plugins: cov-5.0.0, anyio-4.4.0
collecting ...

tests/integration/test_api_accommodation.py::test_create_accommodation PASSED
tests/integration/test_api_accommodation.py::test_list_all_accommodation PASSED
tests/integration/test_api_accommodation.py::test_find_accommodation PASSED
tests/integration/test_api_accommodation.py::test_update_accommodation PASSED
tests/integration/test_api_accommodation.py::test_delete_guest PASSED
tests/integration/test_api_bookings.py::test_create_booking PASSED
tests/integration/test_api_bookings.py::test_list_all_bookings PASSED
tests/integration/test_api_bookings.py::test_find_booking PASSED
tests/integration/test_api_bookings.py::test_update_booking PASSED
tests/integration/test_api_bookings.py::test_delete_guest PASSED
tests/integration/test_api_bookings.py::test_not_found_on_delete_booking PASSED
tests/integration/test_api_guests.py::test_create_a_guest PASSED
tests/integration/test_api_guests.py::test_list_all_guests PASSED
tests/integration/test_api_guests.py::test_find_guest PASSED
tests/integration/test_api_guests.py::test_update_guest PASSED
tests/integration/test_api_guests.py::test_delete_guest PASSED
tests/integration/test_db_accommodation.py::test_create_accommodation PASSED
tests/integration/test_db_accommodation.py::test_select_all_accommodations PASSED
tests/integration/test_db_accommodation.py::test_find_accommodation_by_name PASSED
tests/integration/test_db_accommodation.py::test_update_accommodation PASSED
tests/integration/test_db_accommodation.py::test_delete_accommodation PASSED
tests/integration/test_db_booking.py::test_create_booking PASSED
tests/integration/test_db_booking.py::test_select_all_bookings PASSED
tests/integration/test_db_booking.py::test_find_booking_by_locator PASSED
tests/integration/test_db_booking.py::test_update_booking PASSED
tests/integration/test_db_booking.py::test_delete_accommodation PASSED
tests/integration/test_db_guest.py::test_create_guest PASSED
tests/integration/test_db_guest.py::test_select_all_guests PASSED
tests/integration/test_db_guest.py::test_find_guest_by_name PASSED
tests/integration/test_db_guest.py::test_update_guest PASSED
tests/integration/test_db_guest.py::test_delete_guest PASSED

---------- coverage: platform linux, python 3.12.3-final-0 -----------
Name                               Stmts   Miss  Cover
------------------------------------------------------
app/api/__init__.py                    0      0   100%
app/api/main.py                        9      0   100%
app/api/routers/accommodation.py      63      4    94%
app/api/routers/amenities.py          12      2    83%
app/api/routers/booking.py            67     11    84%
app/api/routers/guests.py             47      4    91%
app/database/db.py                    17      7    59%
app/database/db_init.py               31      0   100%
app/database/models.py                43      0   100%
app/domain/Accommodation.py           39      0   100%
app/domain/Amenitie.py                 9      0   100%
app/domain/Booking.py                 37      3    92%
app/domain/Guest.py                   13      0   100%
app/utils/generate_locator.py          7      0   100%
------------------------------------------------------
TOTAL                                394     31    92%


============================================================================================== 31 passed in 3.14s ===============================================================================================
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

Um dos principais motivos de Fastapi ter sido escolhido para este projeto é a criação automática de uma documentação seguindo a especificação do padrão openAPI que pode ser acessada (neste exemplo) em <http://127.0.0.1:8000/docs>.
