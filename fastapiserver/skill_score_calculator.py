# skill_score_calculator.py

import json
import pandas as pd

# Load the feature scaling parameters from the JSON file
def load_scaling_params(json_file=r'C:\Users\jimzord12\GitHub\Honeypots-Contextual-Behavior-PoC\datasheet\feature_scaling_params.json'):
    """
    Loads feature scaling parameters from a JSON file.
    
    Parameters:
    - json_file (str): Path to the JSON file containing scaling parameters.
    
    Returns:
    - dict: A dictionary containing min and max values for each feature.
    """
    try:
        with open(json_file, 'r') as f:
            scaling_params = json.load(f)
        print(f"Scaling parameters loaded from '{json_file}'.")
        return scaling_params
    except FileNotFoundError:
        raise FileNotFoundError(f"The file '{json_file}' does not exist.")
    except json.JSONDecodeError:
        raise ValueError(f"The file '{json_file}' contains invalid JSON.")

# Define feature weights (ensure these match your domain knowledge)
FEATURE_WEIGHTS = {
    'Weight': 1.5,
    'Num_Attempts': 1.0,
    'Duration': 1.0,
    'Headers_Complexity': 1.2,
    'Payload_Complexity': 1.3
}

# Skill Score scaling parameters (replace with actual values from training)
SKILL_SCORE_SCALING_PARAMS = {
    'min': 0.0,  # Replace with actual minimum Skill Score from training data
    'max': 10.0  # Replace with actual maximum Skill Score from training data
}

def calculate_normalized_skill_score(attack_json, scaling_params=None):
    """
    Calculates the normalized Skill Score for a given attack.
    
    Parameters:
    - attack_json (dict): A dictionary representing the raw attack data with the following keys:
        - 'Weight' (float)
        - 'Num_Attempts' (int or float)
        - 'Duration' (float) in seconds
        - 'Headers_Complexity' (float)
        - 'Payload_Complexity' (float)
    - scaling_params (dict, optional): A dictionary containing min and max values for each feature.
        If None, it loads from 'feature_scaling_params.json'.
    
    Returns:
    - float: The normalized Skill Score between 0 and 1.
    
    Raises:
    - ValueError: If any required feature is missing or has invalid values.
    """
    if scaling_params is None:
        scaling_params = load_scaling_params()
    
    # List of required features
    required_features = ['Weight', 'Num_Attempts', 'Duration', 'Headers_Complexity', 'Payload_Complexity']
    
    # Check for missing features
    missing_features = [feature for feature in required_features if feature not in attack_json]
    if missing_features:
        raise ValueError(f"Missing features: {missing_features}")
    
    # Extract and validate feature values
    try:
        weight = float(attack_json['Weight'])
        num_attempts = float(attack_json['Num_Attempts'])
        duration = float(attack_json['Duration'])
        headers_complexity = float(attack_json['Headers_Complexity'])
        payload_complexity = float(attack_json['Payload_Complexity'])
    except (ValueError, TypeError) as e:
        raise ValueError(f"Invalid feature values: {e}")
    
    # Min-Max Scaling function
    def min_max_scale(value, min_val, max_val):
        if max_val - min_val == 0:
            return 0.0  # Avoid division by zero
        return (value - min_val) / (max_val - min_val)
    
    # Scale each feature
    weight_scaled = min_max_scale(weight, scaling_params['Weight']['min'], scaling_params['Weight']['max'])
    num_attempts_scaled = min_max_scale(num_attempts, scaling_params['Num_Attempts']['min'], scaling_params['Num_Attempts']['max'])
    duration_scaled = min_max_scale(duration, scaling_params['Duration']['min'], scaling_params['Duration']['max'])
    headers_complexity_scaled = min_max_scale(headers_complexity, scaling_params['Headers_Complexity']['min'], scaling_params['Headers_Complexity']['max'])
    payload_complexity_scaled = min_max_scale(payload_complexity, scaling_params['Payload_Complexity']['min'], scaling_params['Payload_Complexity']['max'])
    
    # Calculate Skill Score as a weighted sum of scaled features
    skill_score = (
        weight_scaled * FEATURE_WEIGHTS['Weight'] +
        num_attempts_scaled * FEATURE_WEIGHTS['Num_Attempts'] +
        duration_scaled * FEATURE_WEIGHTS['Duration'] +
        headers_complexity_scaled * FEATURE_WEIGHTS['Headers_Complexity'] +
        payload_complexity_scaled * FEATURE_WEIGHTS['Payload_Complexity']
    )
    
    # Normalize the Skill Score using Min-Max scaling
    normalized_skill_score = min_max_scale(skill_score, SKILL_SCORE_SCALING_PARAMS['min'], SKILL_SCORE_SCALING_PARAMS['max'])
    
    # Ensure the normalized Skill Score is within [0, 1]
    normalized_skill_score = max(0.0, min(normalized_skill_score, 1.0))
    
    return normalized_skill_score

if __name__ == "__main__":
    # Example raw attack data for testing
    sample_attack = {
        "Weight": 7.5,
        "Num_Attempts": 50,
        "Duration": 30.0,            # 30 minutes
        "Headers_Complexity": 5,
        "Payload_Complexity": 2
    }
    
    try:
        score = calculate_normalized_skill_score(sample_attack)
        print(f"Normalized Skill Score: {score:.4f}")
    except ValueError as e:
        print(f"Error: {e}")
