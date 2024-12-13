# Dynamic k-d Tree for Streaming Data

This project implements a **dynamic k-d tree** to efficiently handle streaming spatial data with various insertion and deletion techniques. The goal is to analyze the performance of different strategies in terms of **preprocessing time**, **query time**, and **space usage**, and to visualize these trade-offs using generated figures.

## Project Structure

- **`analysis.py`**: 
  - Downloads the NYC Open Data streaming dataset.
  - Implements a dynamic k-d tree with configurable insertion and deletion strategies.
  - Evaluates the performance of the dynamic k-d tree.
  - Outputs results into a CSV file (`analysis_results.csv`).

- **`analysis_results.csv`**: 
  - Contains the performance metrics for each combination of insertion and deletion strategies:
    - **Preprocessing Time (s)**: Time taken to build the k-d tree.
    - **Space Usage (bytes)**: Memory consumed by the k-d tree.
    - **Total Query Time (s)**: Time required to perform queries on the tree.

- **`generate_figures.py`**: 
  - Reads `analysis_results.csv` to generate visualizations of the performance metrics.
  - Outputs figures:
    - **`preprocessing_time.png`**: Bar chart for preprocessing time.
    - **`query_time.png`**: Bar chart for query time.
    - **`space_usage.png`**: Bar chart for space usage.

- **Figures**:
  - **`preprocessing_time.png`**: Shows preprocessing time for each strategy.
  - **`query_time.png`**: Shows query time for each strategy.
  - **`space_usage.png`**: Shows space usage for each strategy.

## Instructions

### Step 1: Run the Analysis
1. Execute the `analysis.py` script:
   ```bash
   python analysis.py
   ```
   This will:
   - Download the NYC Open Data dataset.
   - Build the dynamic k-d tree with various strategies.
   - Output the performance metrics into `analysis_results.csv`.

### Step 2: Generate Figures
1. Execute the `generate_figures.py` script:
   ```bash
   python generate_figures.py
   ```
   This will:
   - Read `analysis_results.csv`.
   - Generate and save the figures (`preprocessing_time.png`, `query_time.png`, `space_usage.png`) in the same directory.

## Results

The generated figures provide insights into the performance of different strategies:
1. **Preprocessing Time**:
   - Compares how long it takes to build the tree for each strategy.
2. **Query Time**:
   - Evaluates the time efficiency of performing queries on the tree.
3. **Space Usage**:
   - Analyzes the memory efficiency of each strategy.

## Example Strategies
Each strategy is represented in the format `Ix-Dx`:
- **`I1`**: Basic Insertion
- **`I2`**: Rebalanced Insertion
- **`I3`**: Advanced Insertion
- **`D1`**: LRU Deletion
- **`D2`**: Oldest Deletion
- **`D3`**: Temporal Deletion

For example:
- `I1-D1`: Basic Insertion with LRU Deletion.
- `I2-D3`: Rebalanced Insertion with Temporal Deletion.

## Dependencies

- Python 3.x
- Required Libraries:
  - `matplotlib`
  - `pandas`
  - `csv`
  - `requests`

Install dependencies using:
```bash
pip install matplotlib pandas requests
```

## Dataset

- Dataset Source: [NYC Open Data](https://data.cityofnewyork.us/resource/t29m-gskq.csv)
- Downloaded dynamically during the execution of `analysis.py`.

