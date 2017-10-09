# Image Analysis 2.0

Hello World!


## Server Dependencies

> `pip3 install mysql-connector==2.1.4 flask flask_sqlalchemy Flask-MySQL sqlalchemy werkzeug pyyaml`


## Server Migrations
---
When setting up the server for the first time on a new system you will need to run migrations to setup the database. These commands will create the tables required for the server to run. The 5th step is if you need to drop all of the tables for some reason and should only be used in rare cases as this deletes all of the data stored.

1. From the root of the project 
>`cd server`

2. Start python 
> `python3`

3. Import the migrations file 
> `from migrations import db`

4. Run the migration 
> `db.create_all()`

5. To drop all the tables run 
> `db.drop_all()`