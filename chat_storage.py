from database import get_database_connection

# Save a message to the database
def save_message(user_id, message_text, is_user_message):

    mysql_connection = get_database_connection()
    mysql_cursor = mysql_connection.cursor()

    mysql_cursor.execute(
        """
        INSERT INTO messages (user_id, message_text, is_user_message)
        VALUES (%s, %s, %s)
        """,
        (user_id, message_text, is_user_message)
    )
    mysql_connection.commit()

    mysql_cursor.close()
    mysql_connection.close()

# Load all messages for a specific user
def load_user_messages(user_id):

    mysql_connection = get_database_connection()
    mysql_cursor = mysql_connection.cursor()

    mysql_cursor.execute(
        """
        SELECT message_text, is_user_message
        FROM messages
        WHERE user_id = %s
        ORDER BY created_at ASC
        """,
        (user_id,)
    )

    messages = mysql_cursor.fetchall()

    mysql_cursor.close()
    mysql_connection.close()

    return messages
