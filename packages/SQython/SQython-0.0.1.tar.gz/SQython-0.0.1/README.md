# SQython
 A wrapper for SQL and python.

 # requirments
 - psycopg2
 - os
 - numpy
 - io / StringIO
 - pandas


# This was made to create an easier access to SQL through python

# instalation

```
pip install sqython
```

# example use cases

```
# creating a connection to my DB and creating a new database

conn = sq.create_connection("postgres", "postgres", "3301", 'localhost', 5432)
sq.execute_query(conn,create_database('maxtest'))

# after creating we need to connect to our new database

conn = sq.create_connection("maxtest", "postgres", "3301", 'localhost', 5432)


# creating a table based on column names and datatypes to each of their respective columns

sq.execute_query(conn,make_table('testtable',['test1','test2','test3'],['serial','char(50)','char(50)'],'test1'))


# sample DataFrame that we will insert

data = {'test1':[1,2,3],
       'test2':['max','luke','aids'],
       'test3':['a','B','c']}
data = pd.DataFrame(data)

# pushing the data to DB
sq.execute_many(conn,data,'testtable')


# example of deleting new table

sq.execute_query(conn,delete_table('testtable'))

# if we want to delete the current database we must connect to a different one before deletion

conn = sq.create_connection("postgres", "postgres", "3301", 'localhost', 5432)
sq.execute_query(conn,sq.delete_database('maxtest'))


# example of altering a column name
sq.execute_query(conn,sq.alter_column_name(testtable,'test2','names'))

# example of changing an existing columns datatype
# changing column 'names' to varchar
sq.execute_query(conn,sq.alter_datatype(testtable,'names','VARCHAR'))

# to write your own query!

query = 'select * from table'

sq.execute_query(conn,query)

# Currently working on a more efficient and easy querying method

```