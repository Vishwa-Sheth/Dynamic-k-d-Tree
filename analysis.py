import math
import time
import sys
from collections import defaultdict
import pandas as pd
from io import StringIO
import requests
import csv
import os

# Base Node class
class Node:
    def __init__(self, point, depth=0, timestamp=None):
        self.point = point
        self.left = None
        self.right = None
        self.depth = depth
        self.timestamp = timestamp if timestamp else time.time()
        self.access_time = self.timestamp  # For LRU strategies

# Flexible KDTree
class KDTree:
    def __init__(self, k, max_size, insertion_strategy, deletion_strategy):
        self.root = None
        self.k = k
        self.max_size = max_size
        self.size = 0
        self.points = []  # For LRU or rebalancing strategies
        self.insertion_strategy = insertion_strategy
        self.deletion_strategy = deletion_strategy

    def insert(self, point):
        timestamp = time.time()
        self.points.append((point, timestamp))
        self.root = self.insertion_strategy(self, self.root, point, 0, timestamp)
        self.size += 1

        # Enforce window size by deleting excess nodes
        while self.size > self.max_size:
            self.deletion_strategy(self)

    def delete(self, point):
        def find_min(node, d, depth):
            if node is None:
                return None
            cd = depth % self.k

            if cd == d:
                if node.left is None:
                    return node
                return find_min(node.left, d, depth + 1)

            return min(node,
                       find_min(node.left, d, depth + 1),
                       find_min(node.right, d, depth + 1),
                       key=lambda x: x.point[d] if x else math.inf)

        def delete_rec(node, point, depth):
            if node is None:
                return None

            cd = depth % self.k

            if node.point == point:
                if node.right is not None:
                    min_node = find_min(node.right, cd, depth + 1)
                    node.point = min_node.point
                    node.right = delete_rec(node.right, min_node.point, depth + 1)
                elif node.left is not None:
                    min_node = find_min(node.left, cd, depth + 1)
                    node.point = min_node.point
                    node.right = delete_rec(node.left, min_node.point, depth + 1)
                    node.left = None
                else:
                    return None
            elif point[cd] < node.point[cd]:
                node.left = delete_rec(node.left, point, depth + 1)
            else:
                node.right = delete_rec(node.right, point, depth + 1)

            return node

        self.root = delete_rec(self.root, point, 0)
        self.size -= 1

    def subtree_size(self, node):
        """Calculate the size of a subtree rooted at the given node."""
        if node is None:
            return 0
        return 1 + self.subtree_size(node.left) + self.subtree_size(node.right)

    def query(self, target):
        """Evaluate the tree by searching for a point nearest to the target."""
        best = {"node": None, "dist": float("inf")}

        def search(node, depth):
            if node is None:
                return

            cd = depth % self.k
            dist = sum((node.point[i] - target[i]) ** 2 for i in range(len(target)))

            if dist < best["dist"]:
                best["node"] = node
                best["dist"] = dist

            next_branch = node.left if target[cd] < node.point[cd] else node.right
            opposite_branch = node.right if target[cd] < node.point[cd] else node.left

            search(next_branch, depth + 1)
            if abs(target[cd] - node.point[cd]) < best["dist"]:
                search(opposite_branch, depth + 1)

        start_time = time.time()
        search(self.root, 0)
        end_time = time.time()

        execution_time = end_time - start_time
        return best["node"], best["dist"], execution_time

# Insertion Strategies
def basic_insertion(kdtree, node, point, depth, timestamp):
    if node is None:
        return Node(point, depth, timestamp)

    cd = depth % kdtree.k
    if point[cd] < node.point[cd]:
        node.left = basic_insertion(kdtree, node.left, point, depth + 1, timestamp)
    else:
        node.right = basic_insertion(kdtree, node.right, point, depth + 1, timestamp)

    return node

def rebalance_insertion(kdtree, node, point, depth, timestamp):
    kdtree.points.append((point, timestamp))
    if kdtree.size % 100 == 0:  # Rebalance every 100 insertions
        kdtree.root = build_balanced_tree(kdtree.points, kdtree.k, depth=0)
    return basic_insertion(kdtree, node, point, depth, timestamp)

def advanced_insertion(kdtree, node, point, depth, timestamp):
    if node is None:
        return Node(point, depth, timestamp)

    cd = depth % kdtree.k
    left_size = kdtree.subtree_size(node.left)
    right_size = kdtree.subtree_size(node.right)

    if left_size > right_size:
        node.right = advanced_insertion(kdtree, node.right, point, depth + 1, timestamp)
    else:
        node.left = advanced_insertion(kdtree, node.left, point, depth + 1, timestamp)

    return node

# Deletion Strategies
def lru_deletion(kdtree):
    if kdtree.points:
        lru_point = min(kdtree.points, key=lambda x: x[1])
        kdtree.points.remove(lru_point)
        kdtree.delete(lru_point[0])

def oldest_deletion(kdtree):
    if kdtree.points:
        oldest_point = min(kdtree.points, key=lambda x: x[1])
        kdtree.points.remove(oldest_point)
        kdtree.delete(oldest_point[0])

def temporal_deletion(kdtree):
    if kdtree.points:
        oldest_point = min(kdtree.points, key=lambda x: x[1])
        kdtree.points.remove(oldest_point)
        kdtree.delete(oldest_point[0])

# Utility for building balanced tree
def build_balanced_tree(points, k, depth):
    if not points:
        return None

    cd = depth % k
    points.sort(key=lambda x: x[0][cd])
    median_index = len(points) // 2

    node = Node(points[median_index][0], depth, points[median_index][1])
    node.left = build_balanced_tree(points[:median_index], k, depth + 1)
    node.right = build_balanced_tree(points[median_index + 1:], k, depth + 1)

    return node

# Fetch data
def fetch_data():
    url = "https://data.cityofnewyork.us/resource/t29m-gskq.csv"
    response = requests.get(url)
    if response.status_code == 200:
        data = pd.read_csv(StringIO(response.text))
        data_points = [
            (row['pulocationid'], row['dolocationid'], row['passenger_count'], row['trip_distance'], row['fare_amount'])
            for _, row in data.iterrows()
        ]
        return data_points
    else:
        raise Exception("Failed to download dataset")

# Load data and split into 90% for building and 10% for querying
data_points = fetch_data()
split_index = int(len(data_points) * 0.9)
build_data = data_points[:split_index]
query_data = data_points[split_index:]

# Define all combinations
insertion_strategies = [basic_insertion, rebalance_insertion, advanced_insertion]
deletion_strategies = [lru_deletion, oldest_deletion, temporal_deletion]

# Analysis
analysis_results = []
for insertion in insertion_strategies:
    for deletion in deletion_strategies:
        kdtree = KDTree(
            k=5,
            max_size=10,
            insertion_strategy=insertion,
            deletion_strategy=deletion,
        )

        # Build KDTree
        start_time = time.time()
        for point in build_data:
            kdtree.insert(point)
        preprocessing_time = time.time() - start_time

        # Calculate space usage
        space_usage = sys.getsizeof(kdtree) + sum(sys.getsizeof(node) for node in kdtree.points)

        # Query KDTree
        total_query_time = 0
        for query_point in query_data:
            _, _, query_time = kdtree.query(query_point)
            total_query_time += query_time

        # Store results
        analysis_results.append({
            "technique": f"{insertion.__name__}-{deletion.__name__}",
            "preprocessing_time": preprocessing_time,
            "space_usage": space_usage,
            "total_query_time": total_query_time,
        })

# Display results
print("\nAnalysis Results:")
for result in analysis_results:
    print(f"Technique: {result['technique']}")
    print(f"  Preprocessing Time: {result['preprocessing_time']:.6f} seconds")
    print(f"  Space Usage: {result['space_usage']} bytes")
    print(f"  Total Query Time: {result['total_query_time']:.6f} seconds\n")


# Save analysis results to a CSV file
# Determine the current directory of the script
current_directory = os.path.dirname(os.path.abspath(__file__))
output_file = os.path.join(current_directory, "analysis_results.csv")

with open(output_file, mode="w", newline="") as file:
    writer = csv.writer(file)
    
    # Write the header
    writer.writerow(["Technique", "Preprocessing Time (s)", "Space Usage (bytes)", "Total Query Time (s)"])
    
    # Write the data rows
    for result in analysis_results:
        writer.writerow([
            result["technique"],
            result["preprocessing_time"],
            result["space_usage"],
            result["total_query_time"]
        ])

print(f"Analysis results have been saved to '{output_file}'.")