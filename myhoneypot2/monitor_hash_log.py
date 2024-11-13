import json
import re

def calculate_headers_complexity(headers):
    """
    Calculate headers complexity with adjustments to reduce inflated scores.
    Factors considered: number of unique headers and scaled average length of headers.
    """
    if not headers:
        return 0
    
    # Number of unique headers, scaled down
    num_headers = len(headers) / 2
    
    # Average length of header names and values, scaled further
    avg_length = sum(len(k) + len(str(v)) for k, v in headers.items()) / len(headers) / 5
    
    # Complexity formula: normalize with a smaller impact for header number and average length
    complexity_score = (num_headers + avg_length) / 2
    
    # Scale the result to make it reasonable, capping at a maximum score of 10
    complexity_score = min(complexity_score, 10)
    return round(complexity_score, 3)


def calculate_payload_complexity(payload):
    """
    Calculate payload complexity based on the length of the payload,
    presence of special characters, and JSON structure depth if applicable.
    """
    if not payload:
        return 0
    
    # Convert payload to string if it's a JSON object
    payload_str = json.dumps(payload) if isinstance(payload, (dict, list)) else str(payload)
    
    # Base complexity on length of the payload
    length_score = len(payload_str) / 100  # Scale by 100 for simplicity
    
    # Special characters presence: Detect common attack patterns
    special_chars = len(re.findall(r'[\'"<>%;()&+]', payload_str)) / 10  # Scale down by 10
    
    # Depth of JSON structure (if applicable)
    def calculate_depth(obj, level=1):
        if isinstance(obj, dict):
            return level + max((calculate_depth(v, level + 1) for v in obj.values()), default=0)
        elif isinstance(obj, list):
            return level + max((calculate_depth(i, level + 1) for i in obj), default=0)
        return level

    structure_depth = calculate_depth(payload) if isinstance(payload, (dict, list)) else 1
    
    # Complexity formula: (length_score + special_chars + structure_depth) / 3
    complexity_score = (length_score + special_chars + structure_depth) / 3
    return round(complexity_score, 3)


def calculate_complexity(headers_json, payload_json):
    """
    Main function to calculate both headers and payload complexity.
    Takes headers and payload as JSON objects and returns a complexity score.
    """
    try:
        headers = json.loads(headers_json)
        payload = json.loads(payload_json)
        
        headers_complexity = calculate_headers_complexity(headers)
        payload_complexity = calculate_payload_complexity(payload)
        
        return {
            "headers_complexity": headers_complexity,
            "payload_complexity": payload_complexity
        }
    
    except json.JSONDecodeError as e:
        return {"error": f"Invalid JSON input: {e}"}


# Example usage
headers_json = """
{
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c",
    "Content-Type": "application/json",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Cookie": "sessionid=abc123; csrftoken=xyz456",
    "X-Forwarded-For": "192.168.1.1, 192.168.1.2",
    "Referer": "https://www.example.com/login",
    "X-CSRF-Token": "Y29udGV4dDpyZWFjdC1hcHA="
    }
    """
payload_json = """
{
    "username": "admin",
    "password": "pa$$w0rd!",
    "attempts": 5,
    "metadata": {
        "ip_address": "192.168.1.1",
        "location": {"city": "New York", "country": "USA"},
        "device": {
            "os": "Windows 10",
            "browser": {"name": "Chrome", "version": "91.0.4472.124"}
        }
    },
    "data": [
        {"id": 1, "type": "file_upload", "status": "success"},
        {"id": 2, "type": "login_attempt", "status": "failed"}
    ],
    "message": "<script>alert('XSS')</script>"
}
"""

complexity_scores = calculate_complexity(headers_json, payload_json)
print(complexity_scores)