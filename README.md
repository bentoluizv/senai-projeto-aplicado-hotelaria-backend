# Sobre

Projeto Aplicado dos alunos da segunda fase de Análise e Desenvolvimento de Sistemas do SENAI em Florianópolis.

O projeto é baseado na demanda da indústria publicada na plataforma SAGA do SENAI pela empresa Quinta do Ypuã com o objetivo de criar uma solução para o gerenciamento simplificado de hospedagens.

link: https://plataforma.gpinovacao.senai.br/plataforma/demandas-da-industria/interna/9790

## Dependências:
| Dependência  | Versão |
| ------------- | ------------- |
| python  | 3.12.3  |
| pydantic  | 2.7.4  |
| fastapi  | 0.111.0  |
| sqlalchemy  | 2.0.31  |
| pytest  | 8.2.2  |
| taskipy  |1.13.0  |
| ruff  | 0.4.9 |


## Configurando o ambiente de desenvolvimento:

Instale o Poetry para a gestão de dependências.

```powershell
# Windowns (powershell)
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | py -
# If you have installed Python through the Microsoft Store, replace py with python in the command above.


# Linux
curl -sSL https://install.python-poetry.org | python3 -
```

Clone o projeto e entre no diretorio

```bash
  git clone https://github.com/bentoluizv/projeto-aplicado-backend
  cd ./projeto-aplicado-backend
```


Inicie o *.venv* e instale as dependências:
```bash
poetry shell
poetry install
```
### Usando o taskipy para  automatização de tarefas:

```bash
[tool.taskipy.tasks]
lint = 'ruff check . && ruff check . --diff'
# Roda o lint do ruff

format = 'ruff check . --fix && ruff format .'
# Roda o format do ruff

dev = 'fastapi dev app/api/main.py'
# Roda o servidor de desenvolvimento

pre_test = 'task lint'
# Roda o lint antes de rodar os testes

test = 'pytest -s -x --cov=app -vv'
# Roda a suite de testes com pystest

post_test = 'coverage html'
# Roda o test coverage

run = 'fastapi run app/api/main.py'
# Roda o servidor de produçãp

------------------
Para rodar apenas digite 'task <command>'

```
### Inicializando o Servidor de Desenvolvimento

Para inicializar um servidor de desenvolvimento flask rode:

```bash
  task dev
```
Com o servidor de desenvolvimento em funcionamento você pode acessar a documentação da API em http://127.0.0.1:8000/docs ou http://127.0.0.1:8000/redoc.

## Estrutura de Pastas

```bash
.
├── README.md
├── app
│   ├── api
│   │   ├── __init__.py
│   │   ├── main.py
│   │   └── routers
│   │       ├── accommodation.py
│   │       ├── amenities.py
│   │       ├── booking.py
│   │       └── guests.py
│   ├── database
│   │   ├── db.py
│   │   ├── db_init.py
│   │   ├── json
│   │   │   ├── accommodations.json
│   │   │   ├── amenities.json
│   │   │   ├── bookings.json
│   │   │   └── guests.json
│   │   └── models.py
│   ├── domain
│   │   ├── Accommodation.py
│   │   ├── Amenitie.py
│   │   ├── Booking.py
│   │   └── Guest.py
│   └── utils
│       ├── generate_locator.py
│       └── is_valid_cpf.py
├── database.db
├── poetry.lock
├── pyproject.toml
└── tests
    └── integration
        ├── conftest.py
        ├── test_api_accommodation.py
        ├── test_api_bookings.py
        ├── test_api_guests.py
        ├── test_db_accommodation.py
        ├── test_db_booking.py
        └── test_db_guest.py
```