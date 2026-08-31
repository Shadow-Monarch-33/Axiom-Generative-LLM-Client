from database import get_database_connection

# Create a new user account
def create_user(name, email, password):

    mysql_connection = get_database_connection()
    mysql_cursor = mysql_connection.cursor()

    mysql_cursor.execute(
        """
        INSERT INTO users (name, email, password_hash)
        VALUES (%s, %s, %s)
        """,
        (name, email, password)
    )
    mysql_connection.commit()

    mysql_cursor.close()
    mysql_connection.close()

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
        SELECT password_hash
        FROM users
        WHERE email = %s
        """,
        (email,)
    )

    user = mysql_cursor.fetchone()

    mysql_cursor.close()
    mysql_connection.close()

    if not user:
        return False

    return user[0] == password