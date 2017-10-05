# Image Analysis 2.0

Hello World!


## Server Dependencies

> `pip3 install mysql-connector==2.1.4 flask flask_sqlalchemy`



## Server Migrations
---

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