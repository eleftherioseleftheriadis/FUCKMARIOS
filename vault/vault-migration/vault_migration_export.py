
import hvac  # Install with `pip install hvac`
import json

# Connect to the old Vault instance
old_client = hvac.Client(url='https://vault.ingotbrokers.app', token='')

# Define the mount point based on your Vault configuration
mount_point = 'kv'  # Update if the path is different

def export_secrets(path):
    """
    Recursively export all secrets from a given path in the KV v2 engine.
    """
    secrets = {}
    try:
        # List all secrets in the current path
        secret_keys = old_client.secrets.kv.v2.list_secrets(path=path, mount_point=mount_point)
        
        for key in secret_keys['data']['keys']:
            if key.endswith('/'):
                # Recursively handle subdirectories (folders)
                secrets[key] = export_secrets(path=f"{path}/{key}".strip('/'))
            else:
                # Read the actual secret data for each key
                secret = old_client.secrets.kv.v2.read_secret_version(path=f"{path}/{key}", mount_point=mount_point)
                secrets[key] = secret['data']['data']
    except hvac.exceptions.InvalidPath:
        print(f"Invalid path: {path}. Ensure this is a valid path under the '{mount_point}/' mount.")
    return secrets

# Start exporting from the root of the 'kv/' path
all_secrets = export_secrets('')

# Save all secrets to a JSON file as a backup
with open('secrets_backup.json', 'w') as f:
    json.dump(all_secrets, f, indent=4)

print("Secrets export complete. Data saved to 'secrets_backup.json'")
