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

### Abrindo uma conexão com o banco de dados

```bash
  db = get_db() # SQLite3 Database Connection
  result = db.cursor().execute(SELECT * FROM guests;) # Lista

```

### Data Access Objects

Guest DAO

```bash
  from app.data.dao.guest_dao import GuestDAO
  from app.data.database.db import get_db


  db = get_db()
  guest_dao = GuestDAO(db)

  guest_dao.count()
  # Retorna a quantidade de registros

  guest_dao.select(document)
  # Retorna um Dict com o resultado

  guest_dao.select_many()
  # Retorna uma List com os resultados.

  guest_dao.insert(guest)
  # Insere um registro

  guest_dao.update(guest)
  # Atualiza um registro já existente ou Error.

  guest_dao.delete(document)
  # Deleta um registro passando o numero do documto de identificação


```

Accommodation DAO

```bash
  from app.data.dao.accommodation_dao import AccommodationDAO
  from app.data.database.db import get_db


  db = get_db()
  accommodation_dao = AccommodationDAO(db)

  accommodation_dao.count()
  # Retorna a quantidade de registros

  accommodation_dao.select(uuid)
  # Retorna um Dict com o resultado

  accommodation_dao.select_many()
  # Retorna uma List com os resultados.

  accommodation_dao.insert(accommodation)
  # Insere um registro

  accommodation_dao.update(accommodation)
  # Atualiza um registro já existente ou Error.

  accommodation_dao.delete(uuid)
  # Deleta um registro passando o numero do documto de identificação


```

Booking DAO

```bash
  from app.data.dao.booking_dao import BookingDAO
  from app.data.database.db import get_db


  db = get_db()
  booking_dao = BookingDAO(db)

  booking_dao.count()
  # Retorna a quantidade de registros

  booking_dao.select(uuid)
  # Retorna um Dict com o resultado

  booking_dao.select_many()
  # Retorna uma List com os resultados.

  booking_dao.insert(booking)
  # Insere um registro

  booking_dao.update(booking)
  # Atualiza um registro já existente ou Error.

  booking_dao.delete(uuid)
  # Deleta um registro passando o numero do documto de identificação


```

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

## Documentação da API (Em construção)

#### > Retorna todos os hóspedes

```http
  GET /api/guests
```

#### > Retorna um hóspede

```http
  GET /api/guests/${document}
```

| Parâmetro  | Tipo     | Descrição                                                |
| :--------- | :------- | :------------------------------------------------------- |
| `document` | `string` | **Obrigatório**. O documento de identificação do hóspede |

#### > Retorna todas as acomodações

```http
  GET /api/accommodations
```

#### > Retorna uma acomodação

```http
  GET /api/accommodations/${uuid}
```

| Parâmetro | Tipo     | Descrição                             |
| :-------- | :------- | :------------------------------------ |
| `uuid`    | `string` | **Obrigatório**. O uuid da acomodação |

#### > Retorna todas as reservas

```http
  GET /api/bookings
```

#### > Retorna uma reserva

```http
  GET /api/bookings/${uuid}
```

| Parâmetro | Tipo     | Descrição                          |
| :-------- | :------- | :--------------------------------- |
| `uuid`    | `string` | **Obrigatório**. O uuid da reserva |
