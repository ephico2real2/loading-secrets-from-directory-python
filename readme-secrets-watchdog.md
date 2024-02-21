
### Objective

The goal is to demonstrate how `secrets_watchdog.py` dynamically responds to changes in secret files by reloading them automatically. This capability is crucial for applications that need to update their configurations or secrets without restarting.

### Pre-requisites

- Python installed on your system.
- `watchdog` Python package installed. If not, install it using `pip install watchdog`.
- `secrets_loader.py` and `secrets_watchdog.py` scripts are prepared as per the instructions, with the latter set to monitor changes in the `./local_watch` directory.

### Tutorial: Testing `secrets_watchdog.py` Locally

#### Step 1: Prepare Your Secrets Directory

Create the `./local_watch/db-secrets` and `./local_watch/token-secrets` directories within your project's root directory and populate them with initial secret files:

```bash
mkdir -p ./local_watch/db-secrets ./local_watch/token-secrets
echo "localhost" > ./local_watch/db-secrets/MYSQL_HOSTNAME
echo "user" > ./local_watch/db-secrets/MYSQL_USERNAME
echo "password" > ./local_watch/db-secrets/MYSQL_PASSWORD
echo "database_name" > ./local_watch/db-secrets/MYSQL_DB
echo "3306" > ./local_watch/db-secrets/MYSQL_PORT
```

#### Step 2: Run `secrets_watchdog.py`

Open a terminal and navigate to your project's root directory. Start `secrets_watchdog.py` by running:

```bash
python secrets_watchdog.py
```

This command initiates the monitoring of the `./local_watch` directory for any file changes.

#### Step 3: Simulate Secret Changes

While `secrets_watchdog.py` is running, open another terminal window to modify the secrets to trigger the reload mechanism. For example, update the `MYSQL_HOSTNAME` secret:

```bash
echo "newhost.example.com" > ./local_watch/db-secrets/MYSQL_HOSTNAME
```

#### Step 4: Observe the Output

Switch back to the terminal where `secrets_watchdog.py` is running. You should see output indicating that a modification event was detected and the secrets are being reloaded:

```
Detected modified event - ./local_watch/db-secrets/MYSQL_HOSTNAME. Reloading secrets...
```

#### Step 5: Verify Secret Reload

To verify that `secrets_watchdog.py` successfully reloaded the secrets, you can either:

- Integrate a logging statement or a simple print command within `secrets_loader.py` to output the newly loaded secret values (ensure to do this securely to avoid exposing sensitive information).
- Use a connected application or script that utilizes these secrets to confirm it accesses the updated values.

### Tips for Effective Testing

- **Monitor Output**: Keep an eye on the terminal running `secrets_watchdog.py` for real-time logs as you modify, add, or delete secret files.
- **Test Various Changes**: Try creating new secret files, modifying existing ones, or even deleting them to see how the script responds.
- **Use Realistic Secret Values**: For a more authentic test, use placeholder values that mimic real secret data (without using actual sensitive information).

### Conclusion

By following this tutorial, you've learned how to set up and test `secrets_watchdog.py` locally, enabling your applications to dynamically reload configurations or secrets as they change. This approach enhances application flexibility and security, ensuring that updates to configurations or secrets can be seamlessly adopted without service interruption.
