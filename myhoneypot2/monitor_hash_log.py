import json
import time
import requests

def determine_attack_type(title):
    # Map keywords to attack types (case insensitive)
    if "sql" in title.lower():
        return 1  # SQL Injection
    elif "xss" in title.lower():
        return 2  # XSS Attack
    elif "dos" in title.lower():
        return 3  # DOS Attack
    elif "scanning" in title.lower():
        return 4  # Port Scanning
    elif "brute force" in title.lower():
        return 5  # Brute Force Login
    else:
        return None  # Unknown type

def send_to_server(data):
    url = "http://localhost:8080/create-attack"
    headers = {'Content-Type': 'application/json'}

    try:
        response = requests.post(url, json=data, headers=headers)
        if response.status_code == 201:
            print("Successfully sent log entry to Go server.")
        else:
            print(f"Failed to send log entry: {response.status_code} - {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"Error sending log entry to server: {e}")

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
                
                # Filter for logs with specific structure
                if (
                    "http" in log_entry and
                    "info" in log_entry and
                    "type" in log_entry and
                    log_entry["type"] == "malicious"
                ):
                    # Determine attack type based on the title in info
                    attack_type = determine_attack_type(log_entry["info"].get("title", ""))
                    if attack_type is None:
                        print("Warning: Unable to determine attack type for entry.")
                        continue  # Skip if the attack type is unknown

                    # Construct a dictionary with the relevant fields
                    formatted_log = {
                        "source_ip": log_entry["http"].get("client_ip"),
                        "dest_ip": "localhost",  # Set as honeypot IP or change as needed
                        "protocol": "HTTP",
                        "payload": log_entry["request"].get("body", {}),
                        "http_headers": log_entry["request"].get("headers", {}),
                        "path": log_entry["http"].get("path"),
                        "type": attack_type  # Add the attack type as determined
                    }

                    # Write the formatted log entry to JSON file
                    json.dump(formatted_log, json_file)
                    json_file.write("\n")  # Add newline for readability
                    
                    # Send the formatted log entry to the Go server
                    send_to_server(formatted_log)

                    # Print confirmation to console
                    print("Relevant log entry with attack type processed and sent:")
                    print(json.dumps(formatted_log, indent=2))
                    print("\n---\n")

            except json.JSONDecodeError:
                print("Failed to decode log entry as JSON:", line)

if __name__ == "__main__":
    log_file_path = "./logs/attacks.log"
    output_json_path = "./logs/filtered_attacks.json"
    monitor_log_file(log_file_path, output_json_path)
