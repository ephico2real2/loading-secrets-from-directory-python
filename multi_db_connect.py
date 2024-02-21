import mysql.connector
import time
from secrets_loader import SecretsLoader

class DatabaseConnector:
    def __init__(self, secrets_dirs):
        self.secrets_loader = SecretsLoader(secrets_dirs=secrets_dirs)
        self.db_config = None
        self.load_db_config()

    def load_db_config(self):
        """Load or reload the database configuration from secrets."""
        self.db_config = {
            'host': self.secrets_loader.get_credential('MYSQL_HOSTNAME'),
            'user': self.secrets_loader.get_credential('MYSQL_USERNAME'),
            'password': self.secrets_loader.get_credential('MYSQL_PASSWORD'),
            'database': self.secrets_loader.get_credential('MYSQL_DB'),
            'port': int(self.secrets_loader.get_credential('MYSQL_PORT')),
        }

        # After loading the secrets, access and print the API token
        api_token = self.secrets_loader.get_credential('API_TOKEN')
        print(f"API_TOKEN: {api_token}")  # Demonstrate that the token is loaded

    def connect_to_database(self):
        """Establish a database connection using the loaded configuration."""
        try:
            connection = mysql.connector.connect(**self.db_config)
            print("Successfully connected to the database.")
            # Use the connection for database operations
            # ...
            connection.close()
        except mysql.connector.Error as err:
            print(f"Database connection failed: {err}")

    def run(self, reload_interval=300):
        """Run the connector, periodically reloading secrets."""
        try:
            while True:
                self.load_db_config()  # Reload configuration in case of updates
                self.connect_to_database()
                time.sleep(reload_interval)  # Wait for the next reload interval
        except KeyboardInterrupt:
            print("Stopping the database connector.")

if __name__ == "__main__":
    #secrets_dirs = ['./local_watch/db-secrets', './local_watch/token-secrets']  # Example directories
    secrets_dirs = ['./local_secrets', './local_watch/token-secrets']  # Example directories
    connector = DatabaseConnector(secrets_dirs=secrets_dirs)
    connector.run(reload_interval=5)  # Reload secrets every 5 minutes

