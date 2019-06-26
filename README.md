# SQL Alchemy Hack-a-thon

*  Hack-a-thon code: https://www.github.com/rydevops/sqlalchemyhat
*  SQLite browser: https://sqlitebrowser.org/

## <u>Topics</u>

*  What is SQL Alchemy and why should we use it? 
*  What is ORM (Object Relational Mapper)
*  ORM vs SQL
*  Establishing a connection to a database engine
   *  Understanding lazy sessions
   *  SQLite (in-memory)
   *  SQLite (to file)
   *  Postgres
*  Working domain models
   *  Creating a model (table mapper)
   *  Create new records
   *  Commiting data
   *  Querying for records
   *  Deleting records
*  Creating relationships
   *  One-to-One
   *  One-to-Many
   *  Many-to-Many (time permitting)
   *  Interacting with models  with  relationships


## <u>Requirements</u>

The following hack-a-thon will use an SQL Lite database for demonstration. 
Additional detail on how to interact with other databases (e.g. postgres)
can be found in the documentation.

This demonstration was created using Python 3.6 and requires the following python package:
*  sqlalchemy

`python3.6 -m venv venv`

`source venv/bin/activate`

`python3.6 -m pip install sqlalchemy`

## <u>FAQ</u>
**Q:** Can I use SQL for more advanced scenarios?<br>
**A:** Yes, SQL Alchemy has a few ways of allowing you to execute SQL if required. For example **sqlalchemy.text** allows you to specify queries as part of the query. 

**Q:** Can I perform operations such as SQL Joins (querying multiple tables at one time)?<br>
**A:** Yes. The **query** function  also provides a **join** function that will pre-populate multiple domain models. 

**Q:** Is SQL Alchemy the only ORM  for Python?<br>
**A:** No. Python offers a few frameworks such a s django which implement their own ORM patterns often looking very similar to SQL Alchemy. 

**Q:** Can I change the model/table through SQL Alchemy (also known as a migration)?<br>
**A:** The default configuration of SQL Alchemy does not provide a migration facility out of the box however a seperate package ([SQL Alchemy Migrate](https://sqlalchemy-migrate.readthedocs.io/en/latest/)) has been created to enable this functionality. Other ORMs such as django do include the migration facilities. 

## <u>Challenge #1 - Create some simple models</u>

**Timebox:** 30 minutes

As a group perform the following actions on a single computer:

1.  Create a new virtual environment and install sqlalchemy
2.  Setup a new session and engine
3.  Create the models for 2 to 3 tables from the sample ERD (ignore foreign keys)
4.  Insert a couple of rows of data into each table. 
5.  Run your code and validate it works

## <u>Challenge #2 - Create some relationships</u>

**Timebox:** 30 minutes

As a group perform the following actions on a single computer:

1.  Using the tables from the previous challenge setup the foreign key constraints
2.  Configure relationship variables between the models
3.  Delete your db.sqlite3 file
4.  Create some new records that insert data using the new constraints
5.  Run your code and validate it works

## <u>Documentation</u>:
*  [ORM Documentation](https://docs.sqlalchemy.org/en/13/)
*  [Column Reference](https://docs.sqlalchemy.org/en/13/core/metadata.html#sqlalchemy.schema.Column)
*  [Basic Column Types](https://docs.sqlalchemy.org/en/13/core/type_basics.html)
*  [Querying results](https://docs.sqlalchemy.org/en/13/orm/tutorial.html#returning-lists-and-scalars)
*  [Common filter operations](https://docs.sqlalchemy.org/en/13/orm/tutorial.html#common-filter-operators)
*  [Basic Relationship Patterns](https://docs.sqlalchemy.org/en/13/orm/basic_relationships.html)
*  [Defining constraints](https://docs.sqlalchemy.org/en/13/core/constraints.html)


   

