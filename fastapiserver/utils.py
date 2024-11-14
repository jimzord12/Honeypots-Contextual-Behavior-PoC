import json
import re

def get_min_max_values():
    json_file = r'C:\Users\jimzord12\GitHub\Honeypots-Contextual-Behavior-PoC\datasheet\feature_scaling_params.json'
    try:
        with open(json_file, 'r') as f:
            scaling_params = json.load(f)
        print(f"Scaling parameters loaded from '{json_file}'.")
        return scaling_params
    except FileNotFoundError:
        raise FileNotFoundError(f"The file '{json_file}' does not exist.")
    except json.JSONDecodeError:
        raise ValueError(f"The file '{json_file}' contains invalid JSON.")


def calculate_headers_complexity(headers):
    """
    Calculate headers complexity based on the number of unique headers 
    and the average length of header names and values.
    """


    if not headers:
        return 0
    
    # Number of unique headers
    num_headers = len(headers)
    
    # Average length of header names and values
    avg_length = sum(len(k) + len(str(v)) for k, v in headers.items()) / num_headers
    
    # Complexity formula: (number of headers + average length) / 2
    complexity_score = (num_headers + avg_length) / 2

    result = round(complexity_score, 3)

    min_max_values = get_min_max_values()

    if result > min_max_values['Headers_Complexity']['max']:
        return min_max_values['Headers_Complexity']['max'] 
    return result


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

    min_max_values = get_min_max_values()

    result = round(complexity_score, 3)
    if result > min_max_values['Payload_Complexity']['max']:
        return min_max_values['Payload_Complexity']['max']
    return result