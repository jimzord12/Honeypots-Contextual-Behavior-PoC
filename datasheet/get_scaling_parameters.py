from data_analysis import load_data
import json

df_initial = load_data()

# List of features used for Skill Score calculation
features = ['Weight', 'Num_Attempts', 'Duration', 'Headers_Complexity', 'Payload_Complexity']

# Verify the presence of these features in the dataset
missing_features = [feature for feature in features if feature not in df_initial.columns]
if missing_features:
    raise ValueError(f"The following required features are missing from the dataset: {missing_features}")
else:
    print("All required features are present in the dataset.")

### FINDING THE MAXIMUM AND MINIMUM VALUES OF EACH FEATURE ###

# Initialize the FEATURE_SCALING_PARAMS dictionary
FEATURE_SCALING_PARAMS = {}

# Calculate min and max for each feature
for feature in features:
    min_val = df_initial[feature].min()
    max_val = df_initial[feature].max()
    FEATURE_SCALING_PARAMS[feature] = {'min': float(min_val), 'max': float(max_val)}

# Display the scaling parameters
print("Feature Scaling Parameters:")
for feature, params in FEATURE_SCALING_PARAMS.items():
    print(f"{feature}: min = {params['min']}, max = {params['max']}")

    # Save the FEATURE_SCALING_PARAMS to a JSON file
with open('feature_scaling_params.json', 'w') as f:
    json.dump(FEATURE_SCALING_PARAMS, f, indent=4)

print("FEATURE_SCALING_PARAMS saved to 'feature_scaling_params.json'.")