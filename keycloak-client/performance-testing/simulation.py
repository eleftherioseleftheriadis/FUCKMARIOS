import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

# Keycloak endpoints
keycloak_base_url = "https://clientportal-sso.ingotbrokers.app/realms/CustomerAuthRealm/protocol/openid-connect"
token_endpoint = f"{keycloak_base_url}/token"
logout_endpoint = f"{keycloak_base_url}/logout"

# Client and user credentials
client_id = "client-portal-ui"  # Replace with your client ID
username = "xxx"      # Replace with your username
password = "xxx"      # Replace with your password

def login():
    """Simulate a login request to Keycloak."""
    payload = {
        'client_id': client_id,
        'grant_type': 'password',
        'username': username,
        'password': password,
        'scope': 'openid phone profile email offline_access address'
    }
    response = requests.post(token_endpoint, data=payload)
    if response.status_code == 200:
        print("Login successful!")
        return response.json()
    else:
        print(f"Login failed! Status Code: {response.status_code}, Response: {response.text}")
        return None

def refresh_token(refresh_token):
    """Simulate a refresh token request."""
    payload = {
        'client_id': client_id,
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token
    }
    response = requests.post(token_endpoint, data=payload)
    if response.status_code == 200:
        print("Token refreshed successfully!")
        return response.json()
    else:
        print(f"Token refresh failed! Status Code: {response.status_code}, Response: {response.text}")
        return None

def logout(refresh_token):
    """Simulate a logout request."""
    payload = {
        'client_id': client_id,
        'refresh_token': refresh_token,
    }
    response = requests.post(logout_endpoint, data=payload)
    if response.status_code == 204:
        print("Logout successful!")
    else:
        print(f"Logout failed! Status Code: {response.status_code}, Response: {response.text}")

def simulate_user():
    """
    Simulate the full flow for a single user:
    - Login
    - Refresh Token
    - Logout
    """
    tokens = login()
    if tokens:
        refresh_token_value = tokens.get('refresh_token')

        # Simulate token refresh
        new_tokens = refresh_token(refresh_token_value)

        # Simulate logout
        logout(refresh_token_value)

def main(concurrent_users):
    """
    Simulate multiple users performing the login-refresh-logout flow concurrently.
    
    :param concurrent_users: Number of concurrent users to simulate.
    """
    with ThreadPoolExecutor(max_workers=concurrent_users) as executor:
        # Submit tasks for each simulated user session
        futures = [executor.submit(simulate_user) for _ in range(concurrent_users)]

        # Wait for all tasks to complete
        for future in as_completed(futures):
            future.result()  # This will raise any exceptions that occurred during execution

if __name__ == "__main__":
    # Number of concurrent users to simulate
    concurrent_users = 100  # Adjust this number based on your load testing needs

    # Run the load test
    main(concurrent_users)
