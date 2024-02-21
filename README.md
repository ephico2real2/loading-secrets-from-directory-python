# Loading-secrets-from-directory-python

### Dynamic Database Connection Management with `db_connect-watchdog.py`

#### Objective

Learn to automatically manage database connections in your Python applications by dynamically reloading secrets upon modification, using the `db_connect-watchdog.py` script.

#### Pre-requisites

- Python 3.x and MySQL installed on your system.
- Access to a MySQL database.
- `mysql-connector-python` and `watchdog` libraries installed. Install them using `pip3` if you haven't already:

    ```bash
    pip3 install mysql-connector-python watchdog
    ```

#### Step 1: Prepare Your Secrets

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

#### Step 2: Script Overview

`db_connect-watchdog.py` uses the `watchdog` library to monitor the secrets directories for any changes, automatically reloading the database credentials and reconnecting to the MySQL database without manual intervention or restarting the application.

#### Step 3: Running `db_connect-watchdog.py`

1. **Execute the Script**:

    In the terminal, run:

    ```bash
    python3 db_connect-watchdog.py
    ```

    This starts the monitoring of the `./local_secrets` and `./local_watch/token-secrets` directories.

2. **Test by Modifying a Secret**:

    Edit the password file to simulate an update:

    ```bash
    echo "newpassword123" > ./local_secrets/MYSQL_PASSWORD
    ```

3. **Watch for Script Response**:

    The script detects the change, reloads the credentials, and attempts to reconnect to the database. Look for log messages indicating these actions.

#### Step 4: Application Integration

- Tailor `db_connect-watchdog.py` to fit specific application requirements, like supporting various database types or incorporating additional secret types.
- Ensure thorough testing in a controlled environment before deploying to production.

#### Conclusion

`db_connect-watchdog.py` provides an effective method for applications to maintain up-to-date database connections by reacting to changes in configuration secrets in real-time. This tutorial walks you through setting up, executing, and leveraging this script for dynamic secrets management in your Python applications.

```
### Step 5: Adding a Token Secret

Create a token secret within the `./local_watch/token-secrets` directory. This token might represent an API key, authentication token, or any other type of secret your application needs alongside database credentials:

```bash
echo "s3cr3tT0k3nValue" > ./local_watch/token-secrets/API_TOKEN
```

This command creates a file named `API_TOKEN` containing the mock token value `s3cr3tT0k3nValue` in the `./local_watch/token-secrets` directory.

### Step 6: Adjusting `db_connect-watchdog.py` to Acknowledge Token Secrets

Even though `db_connect-watchdog.py` primarily focuses on establishing database connections using MySQL secrets, it's designed to load and be aware of all secrets in the specified directories. To demonstrate that `db_connect-watchdog.py` also loads the token secret, you might want to add a simple log message or print statement to confirm the API token is accessible after secrets are loaded:

```python
# Inside multi_db_connect.py, after initializing SecretsLoader and loading secrets
api_token = secrets_loader.get_credential('API_TOKEN')
print(f"API_TOKEN: {api_token}")
```

This change doesn't alter the database connection logic but confirms that secrets beyond those required for the database can also be loaded and accessed, showcasing the script's flexibility.

### Step 7: Running and Testing

After adding the token secret and adjusting `multi_db_connect.py`:

1. **Run `db_connect-watchdog.py`** in your terminal:

    ```bash
    python3 db_connect-watchdog.py
    ```

2. **Observe the Output**: Look for the printout of the API token value among the startup logs. This confirms that `db_connect-watchdog.py` is correctly loading not just the database secrets but also other secrets like the API token.

