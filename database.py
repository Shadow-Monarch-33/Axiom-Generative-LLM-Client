import os
import mysql.connector

from dotenv import load_dotenv

# Load variables from .env
load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

# Connect to MySQL server
def connect_to_mysql_server():

    return mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD
    )

# Create database if not exists
def create_database():

    mysql_connection = connect_to_mysql_server()
    mysql_cursor = mysql_connection.cursor()

    mysql_cursor.execute(
        f"CREATE DATABASE IF NOT EXISTS {DB_NAME}"
    )

    mysql_cursor.close()
    mysql_connection.close()

# Create the users table if it does not exist
def create_users_table():

    mysql_connection = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )

    mysql_cursor = mysql_connection.cursor()

    mysql_cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            email VARCHAR(255) UNIQUE NOT NULL,
            password VARCHAR(255) NOT NULL
        )
    """)

    mysql_connection.commit()

    mysql_cursor.close()
    mysql_connection.close()

# Set up everything needed by the application
def setup_database():

    create_database()
    create_users_table()

# Get a connection to the AURA database
def get_database_connection():

    return mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )