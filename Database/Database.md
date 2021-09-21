The database for the Helpdesk Application written in MySQL language.
To run the scripts in this folder, you need to create a database in a local database server on your pc:
1. Have any software that supports MySQL. One example is MySQL Workbench.
2. Set up a new local instance of database server from the software.
3. Run the scripts in Main.sql to create a database in your server.
To connect the database with the Python scripts, you need to:
1. pip install mysql-connector-python
2. run the Python scripts below to establish a connection:
import mysql.connector
(any name here) = mysql.connector.connect(
    host = (your database server's hostname),
    user = (the user you have created in your database server),
    password = (your password),
    database = "HelpdeskApplication"
    )
(here's what you want to do with the database)
(the name above).close()
