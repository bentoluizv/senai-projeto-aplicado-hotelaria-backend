# Sobre

Projeto Aplicado dos alunos da segunda fase de Análise e Desenvolvimento de Sistemas do SENAI em Florianópolis.

O projeto é baseado na demanda da indústria publicada na plataforma SAGA do SENAI pela empresa Quinta do Ypuã com o objetivo de criar uma solução para o gerenciamento simplificado de hospedagens.

link: https://plataforma.gpinovacao.senai.br/plataforma/demandas-da-industria/interna/9790

## Instalando pela primeira vez

Se você estiver rodando pela primeira vez o projeto não se esqueça de ativar o ambiente virtual rodando o seguinte comando dentro da pasta do projeto:

```bash
  python3 -m venv .venv

  . .venv/bin/activate
```

com o ambiente virtual iniciado instale o Flask.

```bash
  pip install Flask
```

## Inicializando o Banco de Dados

Para inicializar rode o seguinde comando paraa aplicação criar um banco de dados sqlite rodando o arquivo sql com o schema das tabelas:

```bash
  flask --app app init-db
```

## Inicializando o Servidor de Desenvolvimento

Para inicializar um servidor de desenvolvimento flask rode:

```bash
  flask --app app run --debug
```

## Stack utilizada

Python, Flask
