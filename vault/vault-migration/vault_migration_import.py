import hvac  # Install with `pip install hvac`
import json

# Connect to the new Vault instance
new_client = hvac.Client(url='https://vault-prod.ingotbrokers.app', token='')

# Define the mount point for the secrets engine on the new Vault instance
mount_point = 'kv'  # Update if the path is different

# Load secrets from the backup JSON file
with open('secrets_backup.json', 'r') as f:
    secrets_to_import = json.load(f)

def import_secrets(path, secrets):
    """
    Recursively import all secrets from a dictionary to the specified path in the KV v2 engine.
    """
    for key, value in secrets.items():
        if isinstance(value, dict) and any(k.endswith('/') for k in value.keys()):
            # If the value is a nested dictionary with subdirectories, recurse into it
            import_secrets(f"{path}/{key}".strip('/'), value)
        else:
            # Write each secret at the correct path
            new_client.secrets.kv.v2.create_or_update_secret(
                path=f"{path}/{key}".strip('/'),
                secret=value,
                mount_point=mount_point
            )

# Start importing at the root of the 'kv/' path
import_secrets('', secrets_to_import)

print("Secrets import complete.")
