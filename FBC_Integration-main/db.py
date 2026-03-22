# from dotenv import load_dotenv
#import os
import pymysql
from flask import current_app
from flask_sqlalchemy import SQLAlchemy

#load_dotenv()

# DB_CONFIG = {
#     "host": os.getenv("DB_HOST"),
#     "user": os.getenv("DB_USER"),
#     "password": os.getenv("DB_PASSWORD"),
#     "database": os.getenv("DB_NAME")
# }

# def get_db_connection():
#     return pymysql.connect(
#         host=DB_CONFIG["host"],
#         user=DB_CONFIG["user"],
#         password=DB_CONFIG["password"],
#         database=DB_CONFIG["database"],
#         cursorclass=pymysql.cursors.DictCursor
#     )

db = SQLAlchemy() #Added by resource team for SQLAlchemy integration

def get_db_connection():

    print(f"-------- {current_app.config['MYSQL_DATABASE']} ----------")
    print(f"-------- {current_app.config['MYSQL_USER']} ----------")
    print(f"-------- {current_app.config['MYSQL_PASSWORD']} ----------")

    return pymysql.connect(
        host=current_app.config['MYSQL_HOST'],
        user=current_app.config['MYSQL_USER'],
        password=current_app.config['MYSQL_PASSWORD'],
        database=current_app.config['MYSQL_DATABASE'],
        cursorclass=pymysql.cursors.DictCursor
    )
