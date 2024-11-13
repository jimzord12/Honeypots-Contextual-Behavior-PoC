from data_analysis import load_data
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import matplotlib.pyplot as plt
import seaborn as sns
import joblib

df = load_data(file_path=r'C:\Users\jimzord12\GitHub\Honeypots-Contextual-Behavior-PoC\datasheet\final_attacks_with_skill_levels.csv')

# Features and Target
X = df[['Skill_Score_Normalized']]  # Feature
y = df['Skill_Level']               # Target

#############################################################
# Split the data: 80% training, 20% testing
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# Check the distribution in training and testing sets
print("Training set distribution:")
print(y_train.value_counts(normalize=True))
print("\nTesting set distribution:")
print(y_test.value_counts(normalize=True))

#############################################################
# Initialize the Decision Tree Classifier
dt_classifier = DecisionTreeClassifier(random_state=42, class_weight='balanced')  # 'balanced' helps with class imbalance

# Train the model
dt_classifier.fit(X_train, y_train)

print("\nDecision Tree model trained successfully.\n")

#############################################################

####    Evaluating the Model   ####

# Predict on the test set
y_pred = dt_classifier.predict(X_test)

# Overall Accuracy
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy:.2f}")

# Classification Report
print("\nClassification Report:")
print(classification_report(y_test, y_pred))

#############################################################

####   Saving and Deploying the Model   ####

# Save the trained model to a file
joblib.dump(dt_classifier, 'skill_level_classifier.joblib')
print("Model saved as 'skill_level_classifier.joblib'.")

#############################################################

####   Example Function load/using the Model   ####

###############################################################

def predict_skill_level(skill_score, model_path='skill_level_classifier.joblib'):
    """
    Predicts the Skill Level based on the Skill Score using the saved model.
    
    Parameters:
    - skill_score (float): Normalized Skill Score between 0 and 1.
    - model_path (str): Path to the saved model file.
    
    Returns:
    - str: Predicted Skill Level.
    """
    # Load the model
    model = joblib.load(model_path)
    
    # Ensure skill_score is a list of lists as scikit-learn expects 2D array
    prediction = model.predict([[skill_score]])
    
    return prediction[0]

# Example Usage
sample_skill_score = 0.6
skill_level = predict_skill_level(sample_skill_score)
print(f"Skill Score: {sample_skill_score} --> Skill Level: {skill_level}")

