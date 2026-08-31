import mysql.connector
from database import get_database_connection

# Create a new user account
def create_user(name, email, password):

    mysql_connection = get_database_connection()
    mysql_cursor = mysql_connection.cursor()

    try:
        mysql_cursor.execute(
            """
            INSERT INTO users (name, email, password)
            VALUES (%s, %s, %s)
            """,
            (name, email, password)
        )
        mysql_connection.commit()
        user_id = mysql_cursor.lastrowid
    except mysql.connector.IntegrityError:
        mysql_cursor.close()
        mysql_connection.close()
        return None

    mysql_cursor.close()
    mysql_connection.close()
    return user_id

# Check whether an email already exists
def user_exists(email):

    mysql_connection = get_database_connection()
    mysql_cursor = mysql_connection.cursor()

    mysql_cursor.execute(
        "SELECT id FROM users WHERE email = %s",
        (email,)
    )

    user = mysql_cursor.fetchone()

    mysql_cursor.close()
    mysql_connection.close()

    return user is not None

# Check login details
def login_user(email, password):

    mysql_connection = get_database_connection()
    mysql_cursor = mysql_connection.cursor()

    mysql_cursor.execute(
        """
        SELECT id, password
        FROM users
        WHERE email = %s
        """,
        (email,)
    )

    user = mysql_cursor.fetchone()

    mysql_cursor.close()
    mysql_connection.close()

    if not user:
        return None

    if user[1] == password:
        return user[0]

    return None