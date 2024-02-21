import os
import mysql.connector
from secrets_loader import SecretsLoader
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import logging
import time

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class SecretsChangeHandler(FileSystemEventHandler):
    def __init__(self, callback):
        self.callback = callback

    def on_modified(self, event):
        if not event.is_directory:
            logging.info(f"Detected modification in: {event.src_path}")
            self.callback()

    def on_deleted(self, event):
        if not event.is_directory:
            logging.info(f"Detected deletion of: {event.src_path}")
            self.callback()

class DatabaseConnector:
    def __init__(self, secrets_dirs):
        # Initialize SecretsLoader with directories provided
        self.db_secrets_loader = SecretsLoader(secrets_dirs=secrets_dirs)
        self.token_secrets_loader = SecretsLoader(secrets_dirs=secrets_dirs)
        self.connection = None
        self.load_db_config()
        self.connect_to_database()

    def load_db_config(self):
        # Load or reload database configuration from secrets
        self.db_config = {
            'host': self.db_secrets_loader.get_credential('MYSQL_HOSTNAME'),
            'user': self.db_secrets_loader.get_credential('MYSQL_USERNAME'),
            'password': self.db_secrets_loader.get_credential('MYSQL_PASSWORD'),
            'database': self.db_secrets_loader.get_credential('MYSQL_DB'),
            'port': self.db_secrets_loader.get_credential('MYSQL_PORT'),
        }

    def connect_to_database(self):
        # Connect to the database using the loaded configuration
        if self.connection is not None:
            self.connection.close()
        try:
            self.connection = mysql.connector.connect(**self.db_config)
            logging.info("Successfully connected to the database.")
        except mysql.connector.Error as err:
            logging.error(f"Database connection failed: {err}")

    def load_and_log_additional_secrets(self):
        # Reload and log additional secrets
        api_token = self.token_secrets_loader.get_credential('API_TOKEN')
        aws_sns_topic = self.token_secrets_loader.get_credential('AWS_SNS_TOPIC')
        kafka_url = self.token_secrets_loader.get_credential('KAFKA_URL')
        logging.info(f"Reloaded API_TOKEN: {api_token}")
        logging.info(f"Reloaded AWS_SNS_TOPIC: {aws_sns_topic}")
        logging.info(f"Reloaded KAFKA_URL: {kafka_url}")

    def on_secrets_changed(self):
        # Handle secrets changes: reload secrets and update configurations
        logging.info("Secrets changed. Waiting for file changes to settle...")
        time.sleep(3)  # Delay to ensure file changes are completed
        self.db_secrets_loader.load_secrets()
        self.token_secrets_loader.load_secrets()
        self.load_db_config()
        self.connect_to_database()
        self.load_and_log_additional_secrets()

    def run(self):
        # Set up and start the watchdog observer for secrets directories
        event_handler = SecretsChangeHandler(self.on_secrets_changed)
        observer = Observer()
        for directory in self.db_secrets_loader.secrets_dirs:
            observer.schedule(event_handler, directory, recursive=False)
        observer.start()
        logging.info("Starting enhanced DB and secrets connector...")
        try:
            while True:
                time.sleep(10)
        except KeyboardInterrupt:
            observer.stop()
            logging.info("Stopping enhanced DB and secrets connector...")
        observer.join()
        if self.connection:
            self.connection.close()  # Ensure database connection is closed gracefully

if __name__ == "__main__":
    # Fetch secrets directories from an environment variable, split by commas, and strip spaces
    secrets_dirs_env = os.getenv('SECRETS_DIRS', './default/path/to/secrets').split(',')
    secrets_dirs = [dir.strip() for dir in secrets_dirs_env]

    # Announcement that SECRETS_DIRS was detected and is being used
    logging.info(f"SECRETS_DIRS detected: {', '.join(secrets_dirs)}")

    db_connector = DatabaseConnector(secrets_dirs)
    db_connector.run()