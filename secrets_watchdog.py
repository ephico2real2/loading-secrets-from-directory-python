import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from secrets_loader import SecretsLoader  # Ensure secrets_loader is accessible

class SecretsUpdateHandler(FileSystemEventHandler):
    def __init__(self, secrets_loader):
        self.secrets_loader = secrets_loader

    def on_any_event(self, event):
        # Check if the event is for a file (not a directory)
        if not event.is_directory:
            # Reload secrets on any file change event (create, modify, etc.)
            print(f"Change detected: {event.src_path}. Reloading secrets...")
            self.secrets_loader.load_secrets()
            self.secrets_loader.validate_secrets()

class SecretsWatchdog:
    def __init__(self, secrets_dirs, expected_keys):
        self.secrets_loader = SecretsLoader(secrets_dirs=secrets_dirs, expected_keys=expected_keys)
        self.observer = Observer()

    def run(self):
        event_handler = SecretsUpdateHandler(self.secrets_loader)
        for dir_path in self.secrets_loader.secrets_dirs:
            self.observer.schedule(event_handler, dir_path, recursive=True)
        print("Starting observer to watch for secret changes...")
        self.observer.start()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.observer.stop()
            print("Observer stopped.")
        self.observer.join()

if __name__ == '__main__':
    #secrets_dirs = ['/path/to/db-secrets', '/path/to/token-secrets']  # Update with your directories
    secrets_dirs = ['/Users/olasumbo/local_secrets/db-secrets', '/Users/olasumbo/local_secrets/token-secrets']  # Update with your directories
    expected_keys = ['MYSQL_HOSTNAME', 'MYSQL_USERNAME', 'MYSQL_PASSWORD', 'MYSQL_DB', 'MYSQL_PORT']
    watchdog = SecretsWatchdog(secrets_dirs=secrets_dirs, expected_keys=expected_keys)
    watchdog.run()

