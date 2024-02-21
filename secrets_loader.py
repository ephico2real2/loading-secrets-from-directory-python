# secrets_loader.py
import os
import logging
from typing import List

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class SecretsLoader:
    def __init__(self, secrets_dirs: List[str], expected_keys: List[str] = []):
        self.secrets_dirs = secrets_dirs
        self.expected_keys = expected_keys
        self.credentials = {}
        self.load_secrets()
        self.validate_secrets()

    def load_secrets(self):
        logging.info("Loading secrets...")
        self.credentials.clear()
        for dir_path in self.secrets_dirs:
            if not os.path.isdir(dir_path):
                logging.warning(f"Directory {dir_path} does not exist or is not accessible.")
                continue
            for filename in os.listdir(dir_path):
                secret_path = os.path.join(dir_path, filename)
                try:
                    with open(secret_path, 'r') as file:
                        self.credentials[filename] = file.read().strip()
                        logging.info(f"Loaded secret from {secret_path}")
                except Exception as e:
                    logging.error(f"Failed to read secret from {secret_path}: {e}")

    def validate_secrets(self):
        missing_keys = [key for key in self.expected_keys if key not in self.credentials]
        if missing_keys:
            logging.warning(f"Missing expected secrets: {', '.join(missing_keys)}")
        else:
            logging.info("All expected secrets loaded successfully.")

    def get_credential(self, key: str) -> str:
        return self.credentials.get(key)

# Example usage:
if __name__ == "__main__":
    secrets_dirs = ['/path/to/db-secrets', '/path/to/token-secrets']  # Update these paths as needed
    expected_keys = ['MYSQL_HOSTNAME', 'MYSQL_USERNAME', 'MYSQL_PASSWORD', 'MYSQL_DB', 'MYSQL_PORT']
    loader = SecretsLoader(secrets_dirs=secrets_dirs, expected_keys=expected_keys)
    
    # Demonstrate retrieving a non-sensitive credential for testing purposes
    hostname = loader.get_credential('MYSQL_HOSTNAME')
    print(f"MYSQL_HOSTNAME: {hostname}")
    # Note: Be cautious about printing sensitive information like passwords in a real environment.

