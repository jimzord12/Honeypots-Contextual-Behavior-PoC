import pandas as pd
import sys
import os
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score
from sklearn.cluster import KMeans

def load_data(file_path=r'C:\Users\jimzord12\GitHub\Honeypots-Contextual-Behavior-PoC\datasheet\files\synthetic_attacks.csv'):
    # """
    # Loads the synthetic attacks dataset from a CSV file.

    # Parameters:
    # - file_path (str): The path to the CSV file.

    # Returns:
    # - df (pd.DataFrame): The loaded DataFrame.
    # """
    try:
        # Resolve the absolute path of the file
        file_path = os.path.abspath(file_path)
        print(f"The File's PAth: '{file_path}'")
        
        # Change the working directory to the file's directory
        file_directory = os.path.dirname(file_path)
        os.chdir(file_directory)
        print(f"Changed working directory to: {os.getcwd()}")

        # Load the data
        df = pd.read_csv(file_path)
        print(f"Data loaded successfully from '{file_path}'.\n")

        # Display all columns in the output
        pd.set_option('display.max_columns', None)

        return df
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found. Please ensure the file exists in the specified directory.")
        sys.exit(1)  # Exit the script with a non-zero status indicating an error
    except pd.errors.EmptyDataError:
        print(f"Error: The file '{file_path}' is empty. Please provide a valid CSV file with data.")
        sys.exit(1)
    except pd.errors.ParserError:
        print(f"Error: The file '{file_path}' could not be parsed. Please ensure it is a well-formatted CSV file.")
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred while loading the file: {e}")
        sys.exit(1)

if __name__ == "__main__":
    # Attempt to load the data
    df = load_data()

    # print("- Data Head -")
    # print(df.head())  # Display the first few rows of the dataset
    # print("\n")

    ### One-Hot Encode Attack_Type
    df_encoded = pd.get_dummies(df, columns=['Attack_Type'], drop_first=True)

    # Display the first few rows of the encoded dataframe
    # print(df_encoded.head())

    #######################
    ### Feature Scaling ###
    #######################
    # Step 2: Identify Features to Scale
    # Exclude 'Attack_ID' and the one-hot encoded 'Attack_Type' columns
    features_to_scale = ['Weight', 'Num_Attempts', 'Duration', 'Headers_Complexity', 'Payload_Complexity']

    # Step 3: Initialize the Scaler
    scaler = StandardScaler()

    # Step 4: Fit and Transform the Features
    df_encoded[features_to_scale] = scaler.fit_transform(df_encoded[features_to_scale])

    # Display the scaled features to verify
    # print("\nScaled Numerical Features:")
    # print(df_encoded[features_to_scale].head())

    # Save the Scaled Dataset for Future Use
    df_encoded.to_csv('logs/encoded_scaled_attacks.csv', index=False)
    print("\nFeature scaling completed and saved to 'encoded_scaled_attacks.csv'.\n")

    ##########################################################################################
    ### Determine the Optimal Number of Clusters (K) using Elbow Method & Silhouette Score ###
    ##########################################################################################
    # Define the range for K
    K_range = range(1, 11)
    wcss = []

    for K in K_range:
        kmeans = KMeans(n_clusters=K, random_state=42)
        kmeans.fit(df_encoded[features_to_scale])
        wcss.append(kmeans.inertia_)

    # Plot the Elbow Curve
    plt.figure(figsize=(8, 5))
    plt.plot(K_range, wcss, marker='o')
    plt.title('Elbow Method for Determining Optimal K')
    plt.xlabel('Number of Clusters (K)')
    plt.ylabel('Within-Cluster Sum of Squares (WCSS)')
    plt.xticks(K_range)
    plt.grid(True)
    plt.show()

    ### Silhouette Score
    silhouette_scores = []

    # Start from K=2 since silhouette score is not defined for K=1
    for K in range(2, 11):
        kmeans = KMeans(n_clusters=K, random_state=42)
        kmeans.fit(df_encoded[features_to_scale])
        labels = kmeans.labels_
        score = silhouette_score(df_encoded[features_to_scale], labels)
        silhouette_scores.append(score)

    # Plot the Silhouette Scores
    plt.figure(figsize=(8, 5))
    plt.plot(range(2, 11), silhouette_scores, marker='o', color='green')
    plt.title('Silhouette Scores for Various K')
    plt.xlabel('Number of Clusters (K)')
    plt.ylabel('Silhouette Score')
    plt.xticks(range(2, 11))
    plt.grid(True)
    plt.show()

