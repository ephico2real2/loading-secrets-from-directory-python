This script, designed for dynamic secrets management and database connection handling in Python, utilizes the `mysql-connector-python` library for MySQL database interactions, the `watchdog` library for monitoring filesystem changes, and a custom `SecretsLoader` class for managing secrets. Here's a breakdown of its components and functionality:

### Script Overview

- **Logging Configuration**: Sets up logging to report info-level and above messages with a specific format including the timestamp, logging level, and message.

### `SecretsChangeHandler` Class
- Inherits from `watchdog.events.FileSystemEventHandler`.
- **Purpose**: To handle filesystem events (modification and deletion of files) for specified directories.
- **Methods**:
  - `on_modified`: Called when a file in the watched directory is modified. Logs the event and triggers a callback function.
  - `on_deleted`: Similar to `on_modified`, but triggered when a file is deleted.

### `DatabaseConnector` Class
- **Purpose**: Manages database connections using secrets loaded from specified directories and reacts to changes in these secrets.
- **Initialization**:
  - Accepts two directories: `db_secrets_dir` for database-related secrets and `token_secrets_dir` for other tokens or secrets.
  - Initializes `SecretsLoader` instances for both directories.
  - Loads database configuration and connects to the database upon initialization.
- **Methods**:
  - `load_db_config`: Loads or reloads the database configuration from secrets.
  - `connect_to_database`: Establishes or re-establishes a connection to the database using the loaded configuration. It closes any existing connection before attempting to reconnect.
  - `load_and_log_additional_secrets`: Loads additional secrets (like `API_TOKEN`, `AWS_SNS_TOPIC`, `KAFKA_URL`) and logs their values. This demonstrates how to handle non-database secrets.
  - `on_secrets_changed`: Called when a secrets file is modified or deleted. It waits briefly to ensure all filesystem changes are complete, then reloads secrets and re-establishes the database connection.
  - `run`: Sets up the `watchdog` observer to monitor the secrets directories for changes and starts the monitoring process. It ensures a graceful shutdown upon receiving a keyboard interrupt.

### Main Execution Flow
- Specifies the secrets directories to monitor.
- Initializes the `DatabaseConnector` with these directories.
- Starts the monitoring and handling process, allowing the application to dynamically respond to changes in secrets files.

### Key Features
- **Dynamic Secrets Management**: Automatically reloads secrets and updates database connections in response to changes, enhancing security and flexibility.
- **Separation of Concerns**: Manages database and other secrets separately, allowing for modular handling of different types of configuration data.
- **Robust Error Handling and Logging**: Provides clear feedback on the status of database connections and secret management operations, aiding in troubleshooting and monitoring.

### Usage Scenario
This script is particularly useful in environments where secrets may change frequently, such as cloud environments with rotating credentials or development environments where configurations are frequently tweaked. It ensures that applications can continue to operate with the latest configurations without manual intervention or restarts.

###

1. **Create Secrets Directories**: Set up directories to store your database secrets.

    ```bash
    mkdir -p ./local_secrets ./local_watch/token-secrets
    ```

2. **Populate Secrets Files**: Add your database connection details to the `./local_secrets` directory:

```bash
    echo "127.0.0.1" > ./local_secrets/MYSQL_HOSTNAME
    echo "root" > ./local_secrets/MYSQL_USERNAME
    echo "london123" > ./local_secrets/MYSQL_PASSWORD
    echo "quotes" > ./local_secrets/MYSQL_DB
    echo "3306" > ./local_secrets/MYSQL_PORT
```

```bash
    echo "s3cr3tT0k3nValue" > ./local_watch/token-secrets/API_TOKEN
    echo "arn:aws:sns:us-east-1:123456789012:myTopic" > ./local_watch/token-secrets/AWS_SNS_TOPIC
    echo "kafka://mykafkaurl:9092" > ./local_watch/token-secrets/KAFKA_URL
```

`` python3 enhance_db_connect_secret_loader.py ``


3. ***Populate Secrets Files as Environmental variable SECRETS_DIRS***: set the value of "SECRETS_DIRS" as show below

`` e.g export SECRETS_DIRS='/path/to/db_secrets, /path/to/other_secrets, /path/etc' ``

`` export SECRETS_DIRS='./local_secrets,./local_watch' ``

```bash
    echo "127.0.0.1" > ./local_secrets/MYSQL_HOSTNAME
    echo "root" > ./local_secrets/MYSQL_USERNAME
    echo "london123" > ./local_secrets/MYSQL_PASSWORD
    echo "quotes" > ./local_secrets/MYSQL_DB
    echo "3306" > ./local_secrets/MYSQL_PORT
```

***Execute the scripts with updated logic to read secrets path from ENV SECRETS_DIRS***
`` python3 env_enhance_db_connect_secret_loader.py`` 

***In another terminal add more variables as shown below and monitor the scripts progress**

```bash
    echo "s3cr3tT0k3nValue" > ./local_watch/API_TOKEN
    echo "arn:aws:sns:us-east-1:123456789012:myTopic" > ./local_watch/AWS_SNS_TOPIC
    echo "kafka://mykafkaurl:9092" > ./local_watch/KAFKA_URL
```