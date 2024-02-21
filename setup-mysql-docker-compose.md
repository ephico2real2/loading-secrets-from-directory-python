# Creating MYSQL using docker compose

Creating a MySQL application using Docker Compose involves several steps, including setting up a Docker Compose file for MySQL, preparing an initialization SQL script, configuring secrets for database access, and writing a Python application to interact with the database. Below is a step-by-step tutorial that incorporates using `secrets_loader.py` and `db_connect.py` scripts for managing database secrets dynamically in a local development environment.

### Step 1: Install MYSQL client on your macbook and Prepare Docker Compose File

Create a file named `docker-compose.yml` in your project directory with the following content. This defines a MySQL service with initial environment variables and mounts volumes for data persistence and initialization:

```bash

brew install mysql-client

>>>> Add the mysql client to the shell PATH <<<<

```

```yaml
version: '3.8'
services:
  db:
    image: mysql:8.0
    cap_add:
      - SYS_NICE
    restart: always
    environment:
      - MYSQL_DATABASE=quotes
      - MYSQL_ROOT_PASSWORD=london123
    ports:
      - '3306:3306'
    volumes:
      - db:/var/lib/mysql
      - ./db/init.sql:/docker-entrypoint-initdb.d/init.sql
volumes:
  db:
    driver: local
```

### Step 2: Create the MySQL Initialization Script

Create a directory named `db` in your project directory, and inside it, create a file named `init.sql`. This file can contain SQL commands to initialize your database, such as creating tables or inserting initial data.

Example `init.sql`:

```sql

CREATE DATABASE IF NOT EXISTS quotes;
USE quotes;

CREATE TABLE IF NOT EXISTS quotes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    quote TEXT NOT NULL,
    author VARCHAR(255) NOT NULL
);

INSERT INTO quotes (quote, author)
VALUES ('Life is 10% what happens to us and 90% how we react to it.', 'Charles R. Swindoll');

```

### Step 3: Prepare Secrets for Database Connection

Following the instructions, create a `local_secrets` directory and populate it with your MySQL connection details. Note the correction from "qoutes" to "quotes" for the `MYSQL_DB` file to match the database name defined in your Docker Compose file:

```bash
mkdir -p ./local_secrets ./local_watch/token-secrets

echo "127.0.0.1" > ./local_secrets/MYSQL_HOSTNAME
echo "root" > ./local_secrets/MYSQL_USERNAME
echo "london123" > ./local_secrets/MYSQL_PASSWORD
echo "quotes" > ./local_secrets/MYSQL_DB
echo "3306" > ./local_secrets/MYSQL_PORT

```

### Step 4: Install MySQL Connector for python and watchdog 

Ensure you have the MySQL connector installed in your environment to allow Python to communicate with MySQL:

```bash
 pip3 install mysql-connector-python watchdog
```

### Step 5: Write Your Python Application (`db_connect.py`)

Refer to the previously provided `db_connect.py` script, ensuring it's configured to use the secrets from `./local_secrets`. This script will connect to the MySQL database and can be extended to perform database operations such as querying or updating data.

### Step 6: Run Docker Compose

Navigate to your project directory where `docker-compose.yml` is located and start your MySQL container:

```bash
docker-compose up -d
```

This command starts the MySQL service in detached mode. Your database will be initialized according to the `init.sql` script.


