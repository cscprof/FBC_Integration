# from dotenv import load_dotenv
#import os
import pymysql
from flask import current_app
from flask_sqlalchemy import SQLAlchemy


# db = SQLAlchemy()

# GSM Temporary until all DB is converted
def get_db_connection():

        return pymysql.connect(
            host=current_app.config['MYSQL_HOST'],
            user=current_app.config['MYSQL_USER'],
            password=current_app.config['MYSQL_PASSWORD'],
            database=current_app.config['MYSQL_DATABASE'],
            cursorclass=pymysql.cursors.DictCursor
        )



class db_class():

    def connect(self):

        return pymysql.connect(
            host=current_app.config['MYSQL_HOST'],
            user=current_app.config['MYSQL_USER'],
            password=current_app.config['MYSQL_PASSWORD'],
            database=current_app.config['MYSQL_DATABASE'],
            cursorclass=pymysql.cursors.DictCursor
        )


    def query(self, sql, one_record=False):

        # Connect to database
        conn = self.connect()

        # Execute query
        with conn.cursor() as cursor:
            cursor.execute(sql)

            if one_record == True:
                # Get first/only result
                rows = cursor.fetchone() 
            else: 
                # Get all results
                rows = cursor.fetchall()

        # Close the connection
        conn.close()

        return rows
    

    def insert(self, sql):
        # Add a record to the database

        print(sql)

        # Connect to database
        conn = self.connect()

        # Execute query
        with conn.cursor() as cursor:
            cursor.execute(sql)
            new_id = cursor.lastrowid            

        # Commit change and get insert id
        conn.commit()

        # Close the connection
        conn.close()

        return new_id