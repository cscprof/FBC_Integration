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


    def query(self, sql):

        # Connect to database
        conn = self.connect()

        # Execute query
        with conn.cursor() as cursor:
            cursor.execute(sql)
            rows = cursor.fetchall()

        # Close the connection
        conn.close()

        return rows