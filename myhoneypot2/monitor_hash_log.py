import json
import time
import requests
from dotenv import load_dotenv
import os
import signal
import sys

load_dotenv()

def signal_handler(sig, frame):
    print("\nExiting...")
    sys.exit(0)

# Register signal handler
signal.signal(signal.SIGINT, signal_handler)

def determine_attack_type(title):
    if "sql" in title.lower():
        return 1
    elif "xss" in title.lower():
        return 2
    elif "dos" in title.lower():
        return 3
    elif "scanning" in title.lower():
        return 4
    elif "brute force" in title.lower() or "bruteforce" in title.lower():
        return 5
    return None

def send_to_server(data):
    url = os.getenv("GO_SERVER_URL")
    headers = {'Content-Type': 'application/json'}

    try:
        response = requests.post(url, json=data, headers=headers, timeout=10)
        if response.status_code == 201:
            print("Successfully sent log entry to Go server.")
        else:
            print(f"Failed to send log entry: {response.status_code} - {response.text}")
    except requests.exceptions.Timeout:
        print("Request timed out while sending log entry to server.")
    except requests.exceptions.RequestException as e:
        print(f"Error sending log entry to server: {e}")

def ping_go_server():
    print("Waiting for 5 seconds before pinging the Go server...")
    time.sleep(5)  # Delay for 5 seconds

    try:
        port = os.getenv("GO_SERVER_PORT")
        url = f"http://localhost:{port}/"
        headers = {'Content-Type': 'application/json'}
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            print("Successfully connected to Go server.")
        else:
            print(f"Failed to connect to Go server: {response.status_code} - {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"Error connecting to Go server: {e}")

def monitor_log_file(filepath, output_json):
    with open(filepath, 'r') as file, open(output_json, 'a') as json_file:
        file.seek(0, 2)  # Move to the end of the file
        print(f"Monitoring {filepath} for relevant log entries...\n")

        while True:
            line = file.readline()
            if not line:
                time.sleep(1)
                continue

            try:
                log_entry = json.loads(line.strip())
                if (
                    "http" in log_entry and
                    "info" in log_entry and
                    "type" in log_entry and
                    log_entry["type"] == "malicious"
                ):
                    attack_type = determine_attack_type(log_entry["info"].get("title"))
                    if attack_type is None:
                        print("Unable to determine attack type. Skipping entry.")
                        continue

                    formatted_log = {
                        "source_ip": log_entry["http"].get("client_ip"),
                        "dest_ip": os.getenv("HONEYPOT_IP", "localhost"),
                        "protocol": "HTTP",
                        "payload": log_entry["request"].get("body", {}),
                        "http_headers": log_entry["request"].get("headers", {}),
                        "path": log_entry["http"].get("path"),
                        "type": attack_type
                    }

                    json.dump(formatted_log, json_file)
                    json_file.write("\n")
                    send_to_server(formatted_log)
                    print("Processed and sent:", json.dumps(formatted_log, indent=2))

            except json.JSONDecodeError:
                print("Failed to decode log entry as JSON:", line)

if __name__ == "__main__":
    ping_go_server()
    log_file_path = "./logs/attacks.log"
    output_json_path = "./logs/filtered_attacks.json"
    monitor_log_file(log_file_path, output_json_path)
