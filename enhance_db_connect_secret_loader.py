import mysql.connector
from secrets_loader import SecretsLoader
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import logging
import time

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
    def __init__(self, db_secrets_dir, token_secrets_dir):
        self.db_secrets_loader = SecretsLoader(secrets_dirs=[db_secrets_dir])
        self.token_secrets_loader = SecretsLoader(secrets_dirs=[token_secrets_dir])
        self.connection = None
        self.load_db_config()
        self.connect_to_database()

    def load_db_config(self):
        self.db_config = {
            'host': self.db_secrets_loader.get_credential('MYSQL_HOSTNAME'),
            'user': self.db_secrets_loader.get_credential('MYSQL_USERNAME'),
            'password': self.db_secrets_loader.get_credential('MYSQL_PASSWORD'),
            'database': self.db_secrets_loader.get_credential('MYSQL_DB'),
            'port': int(self.db_secrets_loader.get_credential('MYSQL_PORT')),
        }

    def connect_to_database(self):
        if self.connection is not None:
            self.connection.close()
        try:
            self.connection = mysql.connector.connect(**self.db_config)
            logging.info("Successfully connected to the database.")
        except mysql.connector.Error as err:
            logging.error(f"Database connection failed: {err}")

    def load_and_log_additional_secrets(self):
        # Reload and log additional secrets including API_TOKEN
        api_token = self.token_secrets_loader.get_credential('API_TOKEN')
        aws_sns_topic = self.token_secrets_loader.get_credential('AWS_SNS_TOPIC')
        kafka_url = self.token_secrets_loader.get_credential('KAFKA_URL')
        logging.info(f"Reloaded API_TOKEN: {api_token}")
        logging.info(f"Reloaded AWS_SNS_TOPIC: {aws_sns_topic}")
        logging.info(f"Reloaded KAFKA_URL: {kafka_url}")

    def on_secrets_changed(self):
        logging.info("Secrets changed. Waiting for file changes to settle...")
        time.sleep(3)  # Delay to ensure file changes are completed
        logging.info("Reloading and reconnecting with new secrets...")
        self.db_secrets_loader.load_secrets()
        self.token_secrets_loader.load_secrets()
        self.load_db_config()
        self.connect_to_database()
        self.load_and_log_additional_secrets()

    def run(self, secrets_dirs):
        event_handler = SecretsChangeHandler(self.on_secrets_changed)
        observer = Observer()
        for directory in secrets_dirs:
            observer.schedule(event_handler, directory, recursive=False)
        observer.start()
        try:
            while True:
                time.sleep(10)  # Adjusted sleep time for efficiency
        except KeyboardInterrupt:
            observer.stop()
            observer.join()
            if self.connection:
                self.connection.close()  # Ensure the database connection is closed gracefully

if __name__ == "__main__":
    secrets_dirs = ['./local_secrets', './local_watch/token-secrets']
    db_connector = DatabaseConnector(*secrets_dirs)
    db_connector.run(secrets_dirs)
