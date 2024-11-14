from data_analysis import load_data
import pandas as pd
import sys
import os
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.preprocessing import MinMaxScaler

# Load the scaled data
# Load the scaled data
df_scaled = load_data(file_path=r'C:\Users\jimzord12\GitHub\Honeypots-Contextual-Behavior-PoC\datasheet\files\encoded_scaled_attacks.csv')

# ### K-Mean Clusters ###
# # Define the optimal number of clusters
# optimal_k = 4  # Replace with your determined K
# scaled_features = ['Weight', 'Num_Attempts', 'Duration', 'Headers_Complexity', 'Payload_Complexity']

# # Initialize and Fit K-Means
# kmeans = KMeans(n_clusters=optimal_k, random_state=42)
# kmeans.fit(df_scaled[scaled_features])

# # Assign Cluster Labels
# df_scaled['Cluster'] = kmeans.labels_

# # Display the first few cluster assignments
# print(df_scaled[['Weight', 'Num_Attempts', 'Duration', 'Headers_Complexity', 'Payload_Complexity', 'Cluster']].head())

# # Save the clustered dataset
# df_scaled.to_csv('clustered_attacks.csv', index=False)
# print("\nK-Means clustering completed and saved to 'clustered_attacks.csv'.\n")

# # Check unique cluster labels
# unique_clusters = df_scaled['Cluster'].unique()
# unique_clusters_sorted = sorted(unique_clusters)
# print(f"Unique Cluster Labels: {unique_clusters_sorted}")
# print(f"Total Number of Clusters: {len(unique_clusters_sorted)}")

# ### Visualize the Clusters ###

# # Initialize PCA to reduce to 2 components
# pca = PCA(n_components=2, random_state=42)
# principal_components = pca.fit_transform(df_scaled[scaled_features])

# # Create a DataFrame with principal components
# pca_df = pd.DataFrame(data=principal_components, columns=['PC1', 'PC2'])

# # Concatenate Cluster Labels
# pca_df = pd.concat([pca_df, df_scaled['Cluster']], axis=1)

# # Plot the clusters
# plt.figure(figsize=(10, 7))
# sns.scatterplot(x='PC1', y='PC2', hue='Cluster', data=pca_df, palette='Set1', s=100, alpha=0.7)
# plt.title('K-Means Clusters Visualization using PCA')
# plt.xlabel('Principal Component 1')
# plt.ylabel('Principal Component 2')
# plt.legend(title='Cluster')
# plt.grid(True)
# plt.show()

# # Group by Cluster and calculate mean of features
# cluster_summary = df_scaled.groupby('Cluster')[scaled_features].mean()
# print("\nCluster Summary (Mean Values):")
# print(cluster_summary)

###############################################
# def assign_skill_levels(cluster_summary):
#     """
#     Assigns skill levels to clusters based on feature means.
#     """
#     # Example logic based on 'Weight' and 'Payload_Complexity'
#     # Customize as per your data insights
#     sorted_clusters = cluster_summary.sort_values(by=['Weight', 'Payload_Complexity'], ascending=False).index.tolist()
    
#     skill_mapping = {}
#     for idx, cluster in enumerate(sorted_clusters):
#         if idx == 0:
#             skill_mapping[cluster] = 'High Skill'
#         elif idx == 1:
#             skill_mapping[cluster] = 'Medium Skill'
#         elif idx == 2:
#             skill_mapping[cluster] = 'Low Skill'
#         else:
#             skill_mapping[cluster] = 'Bot'
    
#     print("\nSkill Mapping:")
#     print(skill_mapping)
    
#     return skill_mapping

# # Assign skill levels
# skill_mapping = assign_skill_levels(cluster_summary)

# # Map skill levels to the dataset
# df_scaled['Skill_Level'] = df_scaled['Cluster'].map(skill_mapping)

# # Display updated dataset
# print("\nDataset with Skill Levels:")
# print(df_scaled[['Attack_ID', 'Cluster', 'Skill_Level']].head())

# print("- Data Description -")
# print(df_scaled.describe())  # Display summary statistics
# print("\n")

# # Display information about the dataset
# print("- Data Info -")
# print(df_scaled.info())
# print("\n")

# # Save the final dataset
# df_scaled.to_csv('final_clustered_attacks.csv', index=False)
# print("\nFinal clustered dataset with Skill Levels saved to 'final_clustered_attacks.csv'.")

#####################################################
######## SKILL SCORE CALCULATION ####################
# Load the scaled dataset

# Define the features to include in Skill Score
features = ['Weight', 'Num_Attempts', 'Duration', 'Headers_Complexity', 'Payload_Complexity']

# Assign weights (adjust these values based on feature importance)
weights = {
    'Weight': 1.5,
    'Num_Attempts': 1.0,
    'Duration': 1.0,
    'Headers_Complexity': 1.2,
    'Payload_Complexity': 1.3
}

# Calculate Skill Score as weighted sum
df_scaled['Skill_Score'] = (
    df_scaled['Weight'] * weights['Weight'] +
    df_scaled['Num_Attempts'] * weights['Num_Attempts'] +
    df_scaled['Duration'] * weights['Duration'] +
    df_scaled['Headers_Complexity'] * weights['Headers_Complexity'] +
    df_scaled['Payload_Complexity'] * weights['Payload_Complexity']
)

# Display the first few Skill Scores
print("First 5 Skill Scores:")
print(df_scaled[['Skill_Score']].head())

# Save the updated dataset
df_scaled.to_csv('logs/clustered_attacks_with_skill_score.csv', index=False)
print("Skill Score calculated and saved to 'clustered_attacks_with_skill_score.csv'.")

# Plot Histogram using Matplotlib
plt.figure(figsize=(10, 6))
plt.hist(df_scaled['Skill_Score'], bins=30, color='skyblue', edgecolor='black')
plt.title('Distribution of Skill Scores')
plt.xlabel('Skill Score')
plt.ylabel('Frequency')
plt.grid(axis='y', alpha=0.75)
plt.show()

# Alternatively, using Seaborn
plt.figure(figsize=(10, 6))
sns.histplot(df_scaled['Skill_Score'], bins=30, kde=True, color='skyblue')
plt.title('Distribution of Skill Scores with KDE')
plt.xlabel('Skill Score')
plt.ylabel('Frequency')
plt.show()

########################################################################################
### Normalizing Skill Scores ###
scaler = MinMaxScaler()
df_scaled['Skill_Score_Normalized'] = scaler.fit_transform(df_scaled[['Skill_Score']])

# Display the first few normalized Skill Scores
print("First 5 Normalized Skill Scores:")
print(df_scaled[['Skill_Score_Normalized']].head())

# Save the updated dataset
df_scaled.to_csv('logs/clustered_attacks_with_normalized_skill_score.csv', index=False)
print("Normalized Skill Score calculated and saved to 'clustered_attacks_with_normalized_skill_score.csv'.")

plt.figure(figsize=(10, 6))
plt.hist(df_scaled['Skill_Score_Normalized'], bins=30, color='skyblue', edgecolor='black')
plt.title('Distribution of Normalized Skill Scores')
plt.xlabel('Skill Score')
plt.ylabel('Frequency')
plt.grid(axis='y', alpha=0.75)
plt.show()

# Alternatively, using Seaborn
plt.figure(figsize=(10, 6))
sns.histplot(df_scaled['Skill_Score_Normalized'], bins=30, kde=True, color='skyblue')
plt.title('Distribution of Normalized Skill Scores with KDE')
plt.xlabel('Skill Score')
plt.ylabel('Frequency')
plt.show()

########################################################################################
## Define Skill Levels Based on Skill Score Segments
# Define custom quantiles
bins = [ -float('inf'), 0.25, 0.5, 0.75, float('inf') ]

# Define labels
labels = ['Low Skill', 'Medium-Low Skill', 'Medium-High Skill', 'High Skill']

# Assign Skill Levels based on custom quantiles
df_scaled['Skill_Level'] = pd.cut(df_scaled['Skill_Score_Normalized'], bins=bins, labels=labels)

# Display the first few Skill Level assignments
print("First 5 Skill Level Assignments:")
print(df_scaled[['Skill_Score_Normalized', 'Skill_Level']].head())

# Save the updated dataset
df_scaled.to_csv('logs/final_attacks_with_skill_levels.csv', index=False)
print("Skill Levels assigned and saved to 'final_clustered_attacks_with_skill_levels.csv'.")

plt.figure(figsize=(10, 6))
plt.hist(df_scaled['Skill_Level'], bins=30, color='skyblue', edgecolor='black')
plt.title('Distribution of Normalized Skill Scores')
plt.xlabel('Skill Score')
plt.ylabel('Frequency')
plt.grid(axis='y', alpha=0.75)
plt.show()

# Alternatively, using Seaborn
plt.figure(figsize=(10, 6))
sns.histplot(df_scaled['Skill_Level'], bins=30, kde=True, color='skyblue')
plt.title('Distribution of Skill Levels with KDE')
plt.xlabel('Skill Score')
plt.ylabel('Frequency')
plt.show()