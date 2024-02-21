import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from secrets_loader import SecretsLoader
import mysql.connector
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class SecretsChangeHandler(FileSystemEventHandler):
    def __init__(self, callback):
        self.callback = callback

    def on_modified(self, event):
        if not event.is_directory:
            logging.info(f"Detected change in: {event.src_path}")
            self.callback()

class DatabaseConnector:
    def __init__(self, secrets_dirs):
        self.secrets_loader = SecretsLoader(secrets_dirs=secrets_dirs)
        self.db_config = None
        self.connection = None
        self.load_db_config()
        self.connect_to_database()

    def load_db_config(self):
        self.db_config = {
            'host': self.secrets_loader.get_credential('MYSQL_HOSTNAME'),
            'user': self.secrets_loader.get_credential('MYSQL_USERNAME'),
            'password': self.secrets_loader.get_credential('MYSQL_PASSWORD'),
            'database': self.secrets_loader.get_credential('MYSQL_DB'),
            'port': int(self.secrets_loader.get_credential('MYSQL_PORT')),
        }

    def connect_to_database(self):
        if self.connection is not None:
            self.connection.close()
        try:
            self.connection = mysql.connector.connect(**self.db_config)
            logging.info("Successfully connected to the database.")
        except mysql.connector.Error as err:
            logging.error(f"Database connection failed: {err}")

    def run(self, secrets_dirs):
        # Set up watchdog
        event_handler = SecretsChangeHandler(self.on_secrets_changed)
        observer = Observer()
        for directory in secrets_dirs:
            observer.schedule(event_handler, directory, recursive=False)
        observer.start()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()
        observer.join()

    def on_secrets_changed(self):
        logging.info("Secrets changed. Reloading and reconnecting...")
        self.secrets_loader.load_secrets()
        self.load_db_config()
        self.connect_to_database()

if __name__ == "__main__":
    secrets_dirs = ['./local_secrets', './local_watch/token-secrets']
    db_connector = DatabaseConnector(secrets_dirs)
    db_connector.run(secrets_dirs)

