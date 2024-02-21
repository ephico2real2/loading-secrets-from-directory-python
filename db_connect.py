import mysql.connector
from secrets_loader import SecretsLoader

def connect_to_database(secrets_dir):
    # Initialize the SecretsLoader
    secrets_loader = SecretsLoader(secrets_dirs=[secrets_dir])

    # Retrieve database credentials
    db_config = {
        'host': secrets_loader.get_credential('MYSQL_HOSTNAME'),
        'user': secrets_loader.get_credential('MYSQL_USERNAME'),
        'password': secrets_loader.get_credential('MYSQL_PASSWORD'),
        'database': secrets_loader.get_credential('MYSQL_DB'),
        'port': secrets_loader.get_credential('MYSQL_PORT'),
    }

    # Establish a database connection
    try:
        connection = mysql.connector.connect(**db_config)
        print("Successfully connected to the database.")
        return connection
    except mysql.connector.Error as err:
        print(f"Database connection failed: {err}")
        return None

if __name__ == "__main__":
    secrets_dir = './local_secrets'  # Or use os.path.expanduser('~/local_secrets') if needed
    connection = connect_to_database(secrets_dir)
    # Don't forget to close the connection when done
    if connection:
        connection.close()

