from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime
import sqlite3
import joblib  # For loading the ML model
import json
from dotenv import load_dotenv
import os
from pathlib import Path
from utils import calculate_headers_complexity, calculate_payload_complexity
from skill_score_calculator import calculate_normalized_skill_score
import traceback

load_dotenv()

app = FastAPI()

model = joblib.load(Path(os.getenv("ROOT_PATH")) / os.getenv("MODEL_PATH"))

DATABASE = Path(os.getenv("SQLITE_DB_URL"))

# Pydantic model to receive attack data
class Attack(BaseModel):
    id: int
    type: int
    timestamp: datetime
    source_ip: str
    dest_ip: str
    protocol: str
    payload: Dict[str, Any]
    http_headers: Dict[str, Any]
    path: str
    skill_score: Optional[float] = None
    skill_level: Optional[int] = None

# Placeholder functions if you need them
def calculate_complexity(headers: Dict[str, Any], payload: Dict[str, Any]) -> (float, float):
    # Replace with your actual logic for calculating complexities
    headers_complexity = calculate_headers_complexity(headers)  # Sample logic
    payload_complexity = calculate_payload_complexity(json.dumps(payload))  # Sample logic
    return headers_complexity, payload_complexity

def calculate_skill_score(headers_complexity: float, payload_complexity: float, attack: Attack) -> float:
    weight = attack_type_weights.get(attack.type)
    if weight is None:
        raise ValueError("calculate_skill_score: Invalid attack type")

    attack_data = {
        "Weight": weight,
        "Num_Attempts": 10,           # Hardcoded as per requirement
        "Duration": 20.0,             # Hardcoded as per requirement (20 minutes)
        "Headers_Complexity": headers_complexity,   # Placeholder for actual complexity
        "Payload_Complexity": payload_complexity    # Placeholder for actual complexity
    }

    skill_score = calculate_normalized_skill_score(attack_data)
    return skill_score

skill_level_mapping = {
"Low Skill": 1,
"Medium-Low Skill": 2,
"Medium-High Skill": 3,
"High Skill": 4
}

def map_skill_level(label: str) -> int:
    return skill_level_mapping.get(label, 1)  # Default to 1 (Low Skill) if label is not found

# Mapping for attack types to their corresponding weight values
attack_type_weights = {
    1: 9.0,   # SQL_Injection
    2: 5.0,   # XSS_Attack
    3: 10.0,  # DOS
    4: 3.0,   # PortScanning
    5: 7.0    # BruteForceLogin
}

def predict_skill_level(skill_score: float) -> int:
    # Predict skill level label using the ML model
    label = model.predict([[skill_score]])[0]  # Assuming model returns a label as a string
    return map_skill_level(label)

def update_database(attack_id: int, skill_score: float, skill_level: int):
    print("DATABASE:", DATABASE)
    print("MODEL Path: ", Path(os.getenv("MODEL_URL")))

    # Update the SQLite database with the new skill_score and skill_level
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE attacks SET skill_score = ?, skill_level = ? WHERE id = ?",
        (skill_score, skill_level, attack_id)
    )
    conn.commit()
    conn.close()

# Function to find the key(s) by value
def get_key_by_value(dictionary, target_value):
    return [key for key, value in dictionary.items() if value == target_value]

@app.post("/process-attack")
async def process_attack(attack: Attack):
    try:
        # Step 2: Calculate Headers and Payload Complexities
        headers_complexity, payload_complexity = calculate_complexity(attack.http_headers, attack.payload)
        print(f"Headers Complexity: {headers_complexity}")
        
        # Step 3: Calculate Skill Score and normalize
        skill_score = round(calculate_skill_score(headers_complexity, payload_complexity, attack), 4)
        print(f"Skill Score: {skill_score}")
        
        # Step 4: Predict Skill Level using the ML Model
        skill_level = predict_skill_level(skill_score)
        
        # Step 5: Print results to the console
        print(f"Attack ID: {attack.id}")
        print(f"Skill Score: {skill_score}")
        print(f"Predicted Skill Level (int): {skill_level}")
        skill_level_label = get_key_by_value(skill_level_mapping, skill_level)
        print(f"Predicted Skill Level (Str): {skill_level_label[0]}")
        
        # Step 6: Update the SQLite database with skill_score and skill_level
        update_database(attack.id, skill_score, skill_level)

        return {"message": "Attack processed successfully", "id": attack.id, "skill_score": skill_score, "skill_level": skill_level}

    except Exception as e:
        print("".join(traceback.format_exception(None, e, e.__traceback__)))
        raise HTTPException(status_code=500, detail=str(e))
