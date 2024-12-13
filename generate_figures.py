import matplotlib.pyplot as plt
import csv
import os

# Get the directory of the current script
current_directory = os.path.dirname(os.path.abspath(__file__))

# Load data from the CSV file
input_file = os.path.join(current_directory, "analysis_results.csv")
analysis_results = []

with open(input_file, mode="r") as file:
    reader = csv.DictReader(file)
    for idx, row in enumerate(reader):
        # Assign shorter names to techniques
        insertion_index = idx // 3 + 1  # Divide into groups of 3 for insertion strategies
        deletion_index = idx % 3 + 1   # Cycle through deletion strategies
        short_name = f"I{insertion_index}-D{deletion_index}"
        analysis_results.append({
            "technique": short_name,
            "preprocessing_time": float(row["Preprocessing Time (s)"]),
            "space_usage": int(row["Space Usage (bytes)"]),
            "total_query_time": float(row["Total Query Time (s)"])
        })

# Extract data for plotting
strategies = [result["technique"] for result in analysis_results]
preprocessing_times = [result["preprocessing_time"] for result in analysis_results]
query_times = [result["total_query_time"] for result in analysis_results]
space_usages = [result["space_usage"] for result in analysis_results]

# Determine the best strategy for each metric
best_preprocessing = strategies[preprocessing_times.index(min(preprocessing_times))]
best_query_time = strategies[query_times.index(min(query_times))]
best_space_usage = strategies[space_usages.index(min(space_usages))]

# Plot preprocessing time
plt.figure(figsize=(10, 6))
plt.bar(strategies, preprocessing_times, color="skyblue")
plt.axhline(y=min(preprocessing_times), color="red", linestyle="--", label=f"Best: {best_preprocessing}")
plt.xlabel("Strategies (I=Insertion, D=Deletion)")
plt.ylabel("Preprocessing Time (s)")
plt.title("Preprocessing Time for Different Strategies")
plt.xticks(rotation=45, ha="right")
plt.legend()
plt.tight_layout()
preprocessing_time_file = os.path.join(current_directory, "preprocessing_time.png")
plt.savefig(preprocessing_time_file)

# Plot query time
plt.figure(figsize=(10, 6))
plt.bar(strategies, query_times, color="lightgreen")
plt.axhline(y=min(query_times), color="red", linestyle="--", label=f"Best: {best_query_time}")
plt.xlabel("Strategies (I=Insertion, D=Deletion)")
plt.ylabel("Query Time (s)")
plt.title("Query Time for Different Strategies")
plt.xticks(rotation=45, ha="right")
plt.legend()
plt.tight_layout()
query_time_file = os.path.join(current_directory, "query_time.png")
plt.savefig(query_time_file)

# Plot space usage
plt.figure(figsize=(10, 6))
plt.bar(strategies, space_usages, color="salmon")
plt.axhline(y=min(space_usages), color="red", linestyle="--", label=f"Best: {best_space_usage}")
plt.xlabel("Strategies (I=Insertion, D=Deletion)")
plt.ylabel("Space Usage (Bytes)")
plt.title("Space Usage for Different Strategies")
plt.xticks(rotation=45, ha="right")
plt.legend()
plt.tight_layout()
space_usage_file = os.path.join(current_directory, "space_usage.png")
plt.savefig(space_usage_file)

print(f"Figures saved to the same directory as the script:")
print(f"- {preprocessing_time_file}")
print(f"- {query_time_file}")
print(f"- {space_usage_file}")

