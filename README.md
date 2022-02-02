# Matriz de eisenhower

API criada numa das tarefas do curso de Full Stack Web Developer da Kenzie Academy Brasil.
Se trata de um administrador de tarefas que se baseia na
[Matriz de Eisenhower](https://www.dropbox.com/pt_BR/business/resources/eisenhower-matrix)

## Objetivos

Praticar os conhecimentos em Flask (fazendo a criação de rotas), Flask-SQLAlchemy (fazendo criação de models e query com as mesmas), Flask-Migrate (fazendo a criação das tabelas no banco de dados e dando upgrade nelas), Blueprints e o design pattern Flask Factory.

## Como utilizar

Acesse o link abaixo para acessar a API:<br>
https://eisenhowerpy.herokuapp.com

Caso queria testar localmente:<br>
fork esse repositório e clone em seu computador em seguida instale o ambiente virtual

```
python -m venv venv --upgrade -deps
```

Entre no ambiene virtual:<br>

```
source venv/bin/activate
```

Instale o arquivo requirements.txt

```
pip install -r requirements.txt
```

configure seu arquivo .env com suas definições do seu banco local:<br>

`É PRECISO TER O POSTGRE INSTALADO`
<br>

Depois disso tudo pronto rode o comando abaixo para criar as tabelas no banco de dados:<br>

```
flask db upgrade
```

Adicione os seguintes dados diretamente no seu banco:<br>

```
insert into eisenhowers
    (type)
values
    ('Do It First'),
    ('Schedule It'),
    ('Delegate It'),
    ('Delete It');

```

## Endpoints disponíveis

<br>
Se estiver usando a aplicação no heroku:<br>

**_base_url_ = https://eisenhowerpy.herokuapp.com**<br>
Se for local:<br>
**_base_url_ = http://localhost:5000**<br>
Método|Prefixo|Descrição<br>
--- |--- |---
GET|/category|Retorna todos os registros da tabela
GET|/category/{id}|Retorna um registro específico da tabela
POST|/category|Cria um novo registro na tabela
PATCH|/category/{id}|Atualiza um registro específico da tabela
DELETE|/category/{id}|Deleta um registro específico da tabela
GET|/task|Retorna todas as tarefas registradas
GET|/task/{id}|Retorna uma tarefa específica
POST|/task|Cria uma nova tarefa
PATCH|/task/{id}|Atualiza uma tarefa específica
DELETE|/task/{id}|Deleta uma tarefa específica

![Warning](https://img.shields.io/badge/EC-Em%20constru%C3%A7%C3%A3o-yellowgreen)
