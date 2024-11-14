import pandas as pd
import sys
import os
import matplotlib.pyplot as plt
import seaborn as sns

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

    # Proceed with further data analysis...
    print("-= DATA ANALYSIS =-")

    print("- Data Head -")
    print(df.head())  # Display the first few rows of the dataset
    print("\n")

    print("- Data Description -")
    print(df.describe())  # Display summary statistics
    print("\n")

    # Display information about the dataset
    print("- Data Info -")
    print(df.info())
    print("\n")

    # Get the shape of the dataset
    print("- Data Shape -")
    print(f"Dataset contains {df.shape[0]} rows and {df.shape[1]} columns.")
    print("\n")

    #################################

    # Data Visualization

    # List of numerical features
    numerical_features = ['Weight', 'Num_Attempts', 'Duration', 'Headers_Complexity', 'Payload_Complexity']

    # # Plot histograms (Useful)
    # df[numerical_features].hist(bins=15, figsize=(15, 10), layout=(3, 2))
    # plt.suptitle('Distribution of Numerical Features')
    # plt.show()

    # # Plot boxplots
    # plt.figure(figsize=(15, 10))
    # for idx, feature in enumerate(numerical_features, 1):
    #     plt.subplot(3, 2, idx)
    #     sns.boxplot(y=df[feature])
    #     plt.title(f'Boxplot of {feature}')
    # plt.tight_layout()
    # plt.show()

    # # Calculate correlation matrix
    # corr_matrix = df[numerical_features].corr()

    # # Plot heatmap
    # plt.figure(figsize=(8, 6))
    # sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt=".2f")
    # plt.title('Correlation Heatmap of Numerical Features')
    # plt.show()

    # # Countplot for Attack_Type  (Useful)
    # plt.figure(figsize=(8, 6))
    # sns.countplot(x='Attack_Type', data=df, palette='Set2')
    # plt.title('Frequency of Each Attack Type')
    # plt.xlabel('Attack Type')
    # plt.ylabel('Count')
    # plt.show()

    # Pairplot colored by Attack_Type
    # sns.pairplot(df, hue='Attack_Type', vars=numerical_features, palette='Set1')
    # plt.suptitle('Pairplot of Numerical Features by Attack Type', y=1.02)
    # plt.show()
