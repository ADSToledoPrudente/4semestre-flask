# Projeto Flask - 4º Semestre

Este projeto faz parte do 4º semestre do curso de Análise e Desenvolvimento de Sistemas da Toledo Presidente Prudente, na disciplina de **Frameworks para Desenvolvimento de Software**.

## Professor

**Prof. Dr. Diogo Branquinho Ramos**

## Descrição

O objetivo deste projeto é desenvolver uma aplicação web utilizando o framework Flask, aplicando os conceitos aprendidos na disciplina. A aplicação envolve a criação de um sistema básico com rotas, templates e utilização de um ambiente virtual para gerenciar as dependências.

## Estrutura do Projeto

```bash
4semestre_flask/
│
├── app.py             # Arquivo principal do Flask
├── templates/         # Diretório para arquivos HTML
│   └── index.html     # Template principal
├── static/            # Diretório para arquivos estáticos (CSS, JS, imagens, etc.)
└── routes/            # Diretório para as rotas
```

## Configuração e Execução

```bash
    #Ambiente Windows
Criação
    ├── python -m venv venv
Ativação
    ├── venv\Scripts\Activate
Instalação
    ├── pip install flask wheel mysql-connector mysqlclient SQLAlchemy flask-login Flask-SQLAlchemy
Execução
    ├── flask run
Acesso
    ├── http://127.0.0.1:5000/
```

## Requisitos

├── Python 3.7+
├── Pacotes da seção ```bash Instalação```