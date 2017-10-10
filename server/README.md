# Image Analysis 2.0


## Server
### Server Dependencies
---
When setting up the server for the first time on a new system you will need to install these dependencies with pip3 in order for the application to run.

> `pip3 install mysql-connector==2.1.4 flask flask_sqlalchemy Flask-MySQL sqlalchemy werkzeug pyyaml`


### Server Migrations
---
When setting up the server for the first time on a new system you will need to run migrations to setup the database. The following commands will create tables and drop tables (You won't need to drop tables unless you need to delete the data in the database. 

1. From the root of the project copy the example config to the production config file.
>`cp example.config.yml config.yml`

2. After you've copied the config file you will need to fill in the information that pertains to your MySQL server information.

2. Next, run this command to create the tables
>`python3 pie migrate create`

3. Finally, run the application 
> `python3 app.py`

### Pie
---
Pie is a command line tool to help you manage the server. Pie is built to help both developers and devops handle everyday tasks. Below you'll find a couple examples of what Pie can do and what can be added to it.

Currently pie supports database migrations. Below are the commands it has.

1. Creates all tables in the database
>`python3 pie migrate create`

2. Drops all tables in the database
>`python3 pie migrate drop`


### Project Structure
---
The server is designed in a modular way to make additions easy. In the server folder you will find a few different folders and files. Some of the important ones you may need are listed below with a brief explanation.

#### Folders
 *Models* - These are your object models. These are built with Flask-SQLAlchemy to be used for both migrations in creating database tables as well as in your controllers to manipulate data. For more information see [this](http://flask-sqlalchemy.pocoo.org/2.3/models/).
 
 *Controllers* - This is the main logic of the application. Any data manipulation you need to do goes here. Your routes will call controller methods and they will return a response to be returned to the user.

 *Database* - This is where your migrations file is. The migration file is where you will import your models to create tables in the database.

#### Root Files

*Routes* - This is where you handle the your HTTP routing logic. You'll map routes to controllers here.

### Run the Server
---
To run the server locally to testing run the following command
>`python3 app.py`

To run the server in production you should follow this guide [here](https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-uwsgi-and-nginx-on-ubuntu-16-04). However if you're in a hurry and need to get something up you can open up `app.py` and modify the following code.

1. Change this
>`app.run()`
2. To this
>`app.run(host='0.0.0.0')`