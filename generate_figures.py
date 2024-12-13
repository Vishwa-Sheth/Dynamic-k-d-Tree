import matplotlib.pyplot as plt
import csv
import os

# Get the directory of the current script
# This ensures that the script will work regardless of the working directory
current_directory = os.path.dirname(os.path.abspath(__file__))

# Load data from the CSV file
# 'analysis_results.csv' contains the results of various strategies for the k-d tree
input_file = os.path.join(current_directory, "analysis_results.csv")
analysis_results = []

# Read the CSV file and process each row
with open(input_file, mode="r") as file:
    reader = csv.DictReader(file)  # Use DictReader to access columns by their headers
    for idx, row in enumerate(reader):
        # Assign shorter names to techniques using I (Insertion) and D (Deletion)
        insertion_index = idx // 3 + 1  # Group rows into insertion strategies (every 3 rows per group)
        deletion_index = idx % 3 + 1   # Cycle through deletion strategies within a group
        short_name = f"I{insertion_index}-D{deletion_index}"  # Format the name as 'I1-D1', 'I2-D2', etc.
        
        # Append processed data to the analysis_results list
        analysis_results.append({
            "technique": short_name,  # Shortened strategy name
            "preprocessing_time": float(row["Preprocessing Time (s)"]),  # Preprocessing time in seconds
            "space_usage": int(row["Space Usage (bytes)"]),  # Space usage in bytes
            "total_query_time": float(row["Total Query Time (s)"])  # Query time in seconds
        })

# Extract data for plotting
# Prepare lists for strategies and their corresponding performance metrics
strategies = [result["technique"] for result in analysis_results]
preprocessing_times = [result["preprocessing_time"] for result in analysis_results]
query_times = [result["total_query_time"] for result in analysis_results]
space_usages = [result["space_usage"] for result in analysis_results]

# Determine the best strategy for each metric
# Identify the strategy with the lowest value for preprocessing time, query time, and space usage
best_preprocessing = strategies[preprocessing_times.index(min(preprocessing_times))]
best_query_time = strategies[query_times.index(min(query_times))]
best_space_usage = strategies[space_usages.index(min(space_usages))]

# Plot preprocessing time
# Create a bar chart for preprocessing time
plt.figure(figsize=(10, 6))
plt.bar(strategies, preprocessing_times, color="skyblue")  # Blue bars for preprocessing times
plt.axhline(y=min(preprocessing_times), color="red", linestyle="--", label=f"Best: {best_preprocessing}")  # Highlight the best strategy
plt.xlabel("Strategies (I=Insertion, D=Deletion)")  # X-axis label
plt.ylabel("Preprocessing Time (s)")  # Y-axis label
plt.title("Preprocessing Time for Different Strategies")  # Chart title
plt.xticks(rotation=45, ha="right")  # Rotate x-axis labels for readability
plt.legend()  # Add a legend for the best strategy
plt.tight_layout()  # Adjust layout for better spacing
preprocessing_time_file = os.path.join(current_directory, "preprocessing_time.png")  # File path for saving
plt.savefig(preprocessing_time_file)  # Save the figure as an image

# Plot query time
# Create a bar chart for query time
plt.figure(figsize=(10, 6))
plt.bar(strategies, query_times, color="lightgreen")  # Green bars for query times
plt.axhline(y=min(query_times), color="red", linestyle="--", label=f"Best: {best_query_time}")  # Highlight the best strategy
plt.xlabel("Strategies (I=Insertion, D=Deletion)")  # X-axis label
plt.ylabel("Query Time (s)")  # Y-axis label
plt.title("Query Time for Different Strategies")  # Chart title
plt.xticks(rotation=45, ha="right")  # Rotate x-axis labels for readability
plt.legend()  # Add a legend for the best strategy
plt.tight_layout()  # Adjust layout for better spacing
query_time_file = os.path.join(current_directory, "query_time.png")  # File path for saving
plt.savefig(query_time_file)  # Save the figure as an image

# Plot space usage
# Create a bar chart for space usage
plt.figure(figsize=(10, 6))
plt.bar(strategies, space_usages, color="salmon")  # Red bars for space usage
plt.axhline(y=min(space_usages), color="red", linestyle="--", label=f"Best: {best_space_usage}")  # Highlight the best strategy
plt.xlabel("Strategies (I=Insertion, D=Deletion)")  # X-axis label
plt.ylabel("Space Usage (Bytes)")  # Y-axis label
plt.title("Space Usage for Different Strategies")  # Chart title
plt.xticks(rotation=45, ha="right")  # Rotate x-axis labels for readability
plt.legend()  # Add a legend for the best strategy
plt.tight_layout()  # Adjust layout for better spacing
space_usage_file = os.path.join(current_directory, "space_usage.png")  # File path for saving
plt.savefig(space_usage_file)  # Save the figure as an image

# Print the paths of the saved figures
print(f"Figures saved to the same directory as the script:")
print(f"- {preprocessing_time_file}")
print(f"- {query_time_file}")
print(f"- {space_usage_file}")
