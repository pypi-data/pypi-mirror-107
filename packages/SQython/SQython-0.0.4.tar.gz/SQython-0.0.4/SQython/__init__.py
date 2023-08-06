# written and maintained by Max Paul
# Founder and owner of O2 Analytics

# add me in linkedin https://www.linkedin.com/in/max-k-paul/
# add me on github https://github.com/XamNalpak
# add me on twitter https://twitter.com/max_paul23


# This package is intended to create an easier user experience when working with data in a pgadmin database


# importing packages

import psycopg2
from psycopg2 import OperationalError
import numpy as np
import psycopg2.extras as extras
from io import StringIO
import pandas as pd

# creating initial connection to the database

# allows us to enter our connection parameters to the initial database, or a new one createed after initializing
def create_connection(db_name, db_user, db_password, db_host, db_port):
    connection = None
    try:
        connection = psycopg2.connect(
            database=db_name,
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port,
        )
        print("Connection to PostgreSQL DB successful")
    except OperationalError as e:
        print(f"The error '{e}' occurred")
    return connection



#  example use connection=create_connection(1,2,3,4,5)

# reusable function that sends queries over to your db server

def execute_query(connection, query):
    connection.autocommit = True
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        print("Query executed successfully")
    except OperationalError as e:
        print(f"The error '{e}' occurred")

# Creating a database 

def create_database(connection, query):
    connection.autocommit = True
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        print("Query executed successfully")
    except OperationalError as e:
        print(f"The error '{e}' occurred")


# initializing first table in database ( meant for use with tables THAT DONT CONTAIN A FOREIGN KEY)

def make_table(tablename: str,columns: list,datatypes: list, primary_key: str, *args):
    # this function will take in only strings
    # takes arguments inside a list for columns and datatype
    # also takes in parameter for primary and foreign key
    res = ",".join([i +' ' + j for i, j in zip(columns, datatypes)]) + ','
    query = f'CREATE TABLE {tablename}({res} PRIMARY KEY({primary_key}));'
    return query

# creating a table with a foriegn key (can be used any time after initializing a first table)
# you cannot reference a foriegn key that has yet to be created, so we need a starting table first

def make_table_fkey(tablename: str,columns: list,datatypes: list, primary_key: str, foreign_key:list):
    # this function will take in only strings
    # takes arguments inside a list for columns and datatype
    # also takes in parameter for primary and foreign key
    res = ",".join([i +' ' + j for i, j in zip(columns, datatypes)]) + ','
    
    foreign_key = f"constraint fk_{foreign_key[0]} FOREIGN KEY ({foreign_key[0]}) references {foreign_key[1]}({foreign_key[2]})"
    query = f'CREATE TABLE {tablename}({res} PRIMARY KEY({primary_key}));'
    return query

# creating an entirly new database
def create_database(dbname: str):
    query = f'CREATE DATABASE {dbname}'
    return query

# deleting a database
def delete_database(dbname: str):
    query = f'DROP DATABASE {dbname}'
    return query

# deleting a table from the database
def delete_table(table: str):
    query = f'DROP TABLE if exists {table}'
    return query

# function that writes a pandas dataframe to your specified database table
# makes using python to update databases super easy and functional

def execute_many(conn, df, table):
    """
    Using cursor.executemany() to insert the dataframe
    """
    # Create a list of tupples from the dataframe values
    tuples = [tuple(x) for x in df.to_numpy()]
    # Comma-separated dataframe columns
    cols = ','.join(list(df.columns))
    # SQL quert to execute
    query = "INSERT INTO %s(%s) VALUES(%%s,%%s,%%s)" % (table, cols)
    cursor = conn.cursor()
    try:
        cursor.executemany(query, tuples)
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error: %s" % error)
        conn.rollback()
        cursor.close()
        return 1
    print("execute_many() done")
    cursor.close()

# function to alter a column name
def alter_column_name(table,old_name,new_name):
    query = f'ALTER {table} RENAME COLUMN {old_name} TO {new_name}'
    return query

# function to alter a columnar datatype
def alter_datatype(table,column_name,new_datatype):
    query = f'ALTER TABLE {table} ALTER COLUMN {column_name} TYPE {new_datatype}'
    return query

# function to drop a column in existing table
def drop_column(table,column_name):
    query = f'ALTER TABLE {table} DROP COLUMN {column_name}'
    return query




