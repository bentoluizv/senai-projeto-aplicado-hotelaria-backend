# Sobre

Projeto Aplicado dos alunos da segunda fase de Análise e Desenvolvimento de Sistemas do SENAI em Florianópolis.

O projeto é baseado na demanda da indústria publicada na plataforma SAGA do SENAI pela empresa Quinta do Ypuã com o objetivo de criar uma solução para o gerenciamento simplificado de hospedagens.

link: https://plataforma.gpinovacao.senai.br/plataforma/demandas-da-industria/interna/9790

## Inicializando o Banco de Dados

Para inicializar rode o seguinde comando para a aplicação criar um banco de dados sqlite rodando o arquivo sql com o schema das tabelas:

```bash
  flask --app app init-db
```

## Inicializando o Servidor de Desenvolvimento

Para inicializar um servidor de desenvolvimento flask rode:

```bash
  flask --app app run --debug
```
