# Sobre

Projeto Aplicado dos alunos da segunda fase de Análise e Desenvolvimento de Sistemas do SENAI em Florianópolis.

O projeto é baseado na demanda da indústria publicada na plataforma SAGA do SENAI pela empresa Quinta do Ypuã com o objetivo de criar uma solução para o gerenciamento simplificado de hospedagens.

link: https://plataforma.gpinovacao.senai.br/plataforma/demandas-da-industria/interna/9790

## Rodando localmente

Clone o projeto

```bash
  git clone https://github.com/bentoluizv/senai_projeto_aplicado_quintadoypua.git
```

Entre no diretório do projeto

```bash
  cd ./senai_projeto_aplicado_quintadoypua
```

Inicie o .venv

```bash
# LINUX

  python3 -m venv .venv

  . .venv/bin/activate

# WIN

  py -m venv .venv

  . .venv/Script/activate
```

Atualize o pip e instale as dependências

```bash
  pip install --upgrade pip
  pip install -e .
```

## Inicializando o Banco de Dados

Para inicializar rode o seguinde comando paraa aplicação criar um banco de dados sqlite rodando o arquivo sql com o schema das tabelas:

```bash
  flask --app app init-db
  flask --app app seed-db
```

"init-db" irá inicialiar o banco de dados executando o script SQL com o schema e "seed-db" irá carregar as tabelas com algum dado inicial.

## Inicializando o Servidor de Desenvolvimento

Para inicializar um servidor de desenvolvimento flask rode:

```bash
  flask --app app run --debug
```

## Documentação

### Tipos

```bash
  guest = {
    'document': str,
    'created_at': datetime,
    'name': str,
    'surname': str,
    'country': str,
    'phones': List[str]
  }

  accommodation = {
    'uuid': str
    'created_at': datetime
    'name': str,
    'status': str,
    'name': str,
    'total_guests': int,
    'single_beds': int,
    'double_beds': int,
    'min_nights': int,
    'price': int
    'amenities': List[str]
  }

    booking = {
    'uuid': str,
    'created_at': datetime,
    'guest': Guest,
    'accommodation': Accommodation,
    'status': str,
    'check_in': datetime,
    'check_out': datetime,
  }


```

### Abrindo uma conexão com o banco de dados

```bash
  db = get_db() # SQLite3 Database Connection
  result = db.cursor().execute(SELECT * FROM guests;) # Lista

```

## Camada de Dados

Camada responsável pelo acesso ao banco de dados (através do módulo database.py), organização da queries de consulta e mutações utilizando DAOs (Data Access Objects) para cada entidade e Repositórios para centralizar a criação das classes especificas de cada entidade.

```bash
# Como instanciar o repositório.
db = get_db() # Importada do modulo database.py
dao = GuestDAO(db) #  DAO referente a tabela de Hóspedes
repository = GuestRepository(dao)

# O repositório expõe as seguintes operações:

count(): int # Retorna a quantidade de registros em uma tabela
insert(Entidade): None # Cria um novo registro
find(id): <Entidade>   # Procura um registro de acordo com uma identificação
find_many(): List[Entidade]  # Lista todos os registros
update(Entidade): None  # Atualiza um registro já existente
delete(document): None  # Deleta um registro a partir da uma identificação


```

## Documentação da API (Em construção)

#### > Retorna todos os hóspedes

```http
  GET /api/hospedes/
```

#### > Retorna um hóspede

```http
  GET /api/hospedes/${document}/
```

| Parâmetro  | Tipo     | Descrição                                                |
| :--------- | :------- | :------------------------------------------------------- |
| `document` | `string` | **Obrigatório**. O documento de identificação do hóspede |

#### > Cadastra um novo hóspedee

```http
  POST /api/hospedes/cadastro/
```

#### body da requisição

| Parâmetro  | Tipo     | Descrição                            |
| :--------- | :------- | :----------------------------------- |
| `document` | `string` | Documento de Identificação. Ex.: CPF |
| `name`     | `string` |                                      |
| `surname`  | `string` |                                      |
| `country`  | `string` |                                      |
| `phone`    | `string` |                                      |

#### > Deleta um hóspede

```http
  DELETE /api/hospedes/${document}/
```

| Parâmetro  | Tipo     | Descrição                                                |
| :--------- | :------- | :------------------------------------------------------- |
| `document` | `string` | **Obrigatório**. O documento de identificação do hóspede |

#### > Atualiza um hóspede

```http
  PUT /api/hospedes/
```

| Parâmetro  | Tipo     | Descrição                            |
| :--------- | :------- | :----------------------------------- |
| `document` | `string` | Documento de Identificação. Ex.: CPF |
| `name`     | `string` |                                      |
| `surname`  | `string` |                                      |
| `country`  | `string` |                                      |
| `phone`    | `string` |                                      |
