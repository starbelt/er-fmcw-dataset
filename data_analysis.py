import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import re
from collections import defaultdict

def parse_bin_range(bin_name):
    """Extract the min and max values from a bin range string and adjust by 0.01m"""
    match = re.search(r'(\d+\.\d+)-(\d+\.\d+)', bin_name)
    if match:
        low = float(match.group(1))
        high = float(match.group(2))
        # Adjust for rounding as specified
        return low - 0.01, high + 0.01
    return None, None

def analyze_dataset(base_dir="DataSet"):
    """Analyze all bins in the dataset for accuracy"""
    results = []
    
    # Check if base directory exists
    if not os.path.exists(base_dir):
        print(f"Error: Directory '{base_dir}' not found.")
        return results
    
    # Process each bin directory
    bin_dirs = [d for d in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, d))]
    
    for bin_dir in bin_dirs:
        bin_path = os.path.join(base_dir, bin_dir)
        filtered_csv_path = os.path.join(bin_path, "FilteredCSV")
        
        if not os.path.exists(filtered_csv_path):
            print(f"Warning: No FilteredCSV directory found in {bin_path}")
            continue
        
        # Parse the bin range
        bin_low, bin_high = parse_bin_range(bin_dir)
        if bin_low is None:
            print(f"Warning: Could not parse bin range from '{bin_dir}', skipping")
            continue
            
        print(f"Processing bin: {bin_dir} (adjusted range: {bin_low:.2f}-{bin_high:.2f}m)")
        
        # Track all calculated distances for this bin
        all_distances = []
        
        # Process each CSV file
        csv_files = [f for f in os.listdir(filtered_csv_path) if f.endswith('.csv')]
        
        for csv_file in csv_files:
            file_path = os.path.join(filtered_csv_path, csv_file)
            try:
                # Read the CSV file
                df = pd.read_csv(file_path)
                
                # Extract calculated distances (Range column)
                if "Range (m)" in df.columns:
                    distances = df["Range (m)"].dropna().tolist()
                    all_distances.extend(distances)
                    
            except Exception as e:
                print(f"Error processing {file_path}: {e}")
        
        if not all_distances:
            print(f"No distance data found for bin {bin_dir}")
            continue
            
        # Calculate how many distances fall within the bin range
        in_range = [d for d in all_distances if bin_low <= d <= bin_high]
        accuracy = len(in_range) / len(all_distances) if all_distances else 0
        
        bin_result = {
            "bin_name": bin_dir,
            "bin_range": (bin_low, bin_high),
            "all_distances": all_distances,
            "in_range_count": len(in_range),
            "total_count": len(all_distances),
            "accuracy": accuracy
        }
        
        results.append(bin_result)
    
    return results

def create_distribution_charts(results, output_dir="accuracy_plots"):
    """Create distribution charts for each bin"""
    if not results:
        return
        
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Create individual bin distribution charts
    for bin_data in results:
        bin_name = bin_data["bin_name"]
        bin_low, bin_high = bin_data["bin_range"]
        all_distances = bin_data["all_distances"]
        accuracy = bin_data["accuracy"]
        
        # Create histogram with appropriate bin size
        plt.figure(figsize=(10, 6))
        
        # Determine suitable number of bins for the histogram
        range_width = max(all_distances) - min(all_distances)
        num_bins = min(30, max(10, int(range_width / 0.02)))  # About 2cm per bin
        
        n, bins, patches = plt.hist(all_distances, bins=num_bins, alpha=0.7)
        
        # Add vertical lines for bin boundaries
        plt.axvline(x=bin_low, color='r', linestyle='--', label=f'Min ({bin_low:.2f}m)')
        plt.axvline(x=bin_high, color='r', linestyle='--', label=f'Max ({bin_high:.2f}m)')
        
        plt.title(f'Distribution for Bin {bin_name}\nAccuracy: {accuracy:.2%}')
        plt.xlabel('Calculated Distance (m)')
        plt.ylabel('Count')
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        # Save the histogram
        safe_name = bin_name.replace('.', '_').replace('-', '_')
        hist_path = os.path.join(output_dir, f"hist_{safe_name}.png")
        plt.tight_layout()
        plt.savefig(hist_path)
        plt.close()
        
        print(f"Created charts for bin {bin_name}")
    
    # Create summary accuracy bar chart
    plt.figure(figsize=(12, 6))
    bin_names = [data["bin_name"] for data in sorted(results, key=lambda x: x["bin_name"])]
    accuracies = [data["accuracy"] * 100 for data in sorted(results, key=lambda x: x["bin_name"])]
    
    plt.bar(bin_names, accuracies)
    plt.title('Accuracy by Distance Bin')
    plt.xlabel('Distance Bin (m)')
    plt.ylabel('Accuracy (%)')
    plt.ylim(0, 100)
    plt.grid(True, alpha=0.3)
    plt.xticks(rotation=45, ha='right')
    
    # Save the summary plot
    summary_path = os.path.join(output_dir, "accuracy_summary.png")
    plt.tight_layout()
    plt.savefig(summary_path)
    plt.close()
    
    print(f"Created summary accuracy chart: {summary_path}")

def main():
    # Analyze the dataset
    results = analyze_dataset()
    
    # Print summary
    if results:
        print("\n===== Accuracy Summary =====")
        for bin_data in sorted(results, key=lambda x: x["bin_name"]):
            print(f"Bin {bin_data['bin_name']}: {bin_data['accuracy']:.2%} accuracy "
                  f"({bin_data['in_range_count']}/{bin_data['total_count']} measurements in range)")
                  
        # Create visualization charts
        create_distribution_charts(results)
    else:
        print("No results to display.")

if __name__ == "__main__":
    main()