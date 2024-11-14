## About the Project

This is PoC about utilizing a honeypot to determine the skill level of the attacker. The main idea is to create another metric when using honeypots to record attackers actions and reseach their behaviors.

## Structure

![The architecture](imgs/arch.png)

1. **HASH Honeypot**: The honeypot logs the attackers actions into a file.
2. **Python Monitoring Script**: A script that moniotrs the log file and sends the data to the Go Server.
3. **Go Server**:
   - Receives the data from the monitoring script.
   - Processes the data.
   - Sends the data to the SQLite DB.
   - Sends the data to the FastAPI Python Server.
4. **FastAPI Python Server**:
   - Receives the data from the Go Server.
   - Futher process them.
   - Utilizes a simple ML Classification Model to determine the skill level of the attacker.
   - Updates the SQLite DB with the results.
5. **SQLite DB**: Stores the data about the attacks and the attackers skill levels.

## About the ML Model

### Data Sheet

We synthesized a datasheet containing 200 attacks. Below you can the datasheet summary:
![Datasheet_Summary](Datasheet_Summary.png)

To calcualte the Headers and Payload Complexity, we used the following methodology:
![alt text](Header_and_Payload_Complexity-1.png)

### Processing the Data (Skill Score)

Next, we created a new feature called "Skill Score". It's purpose is to determine the skill level of the attacker.

1. First, we scaled each feature to make them comparable, we applied "min-max scaling".
2. Next, each feature’s scaled value is multiplied by a specific weight. These weights represent how important each feature is in calculating the skill score. This resulted in the following skill scores:
   ![alt text](<Distribution of Skill Scores.png>)
3. Finally, To make sure the final score is easy to interpret and lies within a range of 0 to 1, we normalize the calculated skill score again using min-max scaling. This ensures that a score of 1 represents the highest observed skill, and a score of 0 represents the lowest:
   ![alt text](<Distribution of Normalized Skill Scores with KDE.png>)

### Creating the Model

We used a simple **Decision Tree Classifier** to determine the skill level of the attacker. The model was trained on the proccessed datasheet.

Its task is to predict the skill level of the attacker based on the Skill Score feature calculated from the attack.

We manually set the thresholds for the skill levels.

| Skill Score   | Skill Level |
| ------------- | ----------- |
| 0.00 - 0.2499 | Low         |
| 0.25 - 0.4999 | Medium Low  |
| 0.50 - 0.7499 | Medium High |
| 0.75 - 1.0000 | High        |

Thus the classifacation of the attacker's skill level can be easily found. For this reason, the Model has shown an accuracy of 100%.

## Running the Project

### Setup

1. Clone the repository

```bash
git clone https://github.com/<username>/<repo>
```

2. Install the dependencies

```bash
npm install
```

### HASH

To run:

```bash
npx hash-honeypot run myhoneypot2 -l file -f ./logs/attacks.log
```

In the case that it complains that it can't find the folder `myhoneypot2`, you can create a new one by running:

```bash
npx hash-honeypot generate myhoneypot3
```

### Python Monitoring Script

To run:

```bash
python myhoneypot2/monitor_hash_log.py
```

### Go Server

Get the dependencies:

```bash
go mod tidy
```

To run:

```bash
go run --tags json1 apiserver/cmd/api/main.go
```

### FastAPI Python Server

Get the dependencies:

```bash
pip install -r requirements.txt
```

To run:

```bash
python uvicorn apiserver/main:app --reload
```

## How can this PoC be improved

1. Use real and more data.
2. Use K-means Clustering to determine how many skill levels should the attackers be classified into.
3. Train and use a more complex model to determine the skill level of the attacker.

## Personal Notes
- Add the other 4 possible attack types to HASH Honeypot.
- Write a script that starts all the services.
