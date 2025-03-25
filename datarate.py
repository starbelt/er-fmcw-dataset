import csv
import numpy as np
import argparse
import sys
import os
from collections import defaultdict

def calculate_avg_sample_rate(file_path):
    """Calculate the average sample rate from a CSV file with timestamps."""
    try:
        # Check if file exists
        if not os.path.isfile(file_path):
            print(f"Error: File '{file_path}' not found.")
            return None
            
        # Read the CSV file, skipping any comment lines
        with open(file_path, 'r') as f:
            lines = [line for line in f if not line.strip().startswith('//')]
        
        # Parse the CSV data
        reader = csv.reader(lines)
        header = next(reader)  # Skip header row
        
        # Get timestamps (assuming first column is timestamp)
        timestamps = []
        for row in reader:
            if row:  # Check if row is not empty
                try:
                    timestamps.append(float(row[0]))
                except (ValueError, IndexError):
                    continue
        
        # Get unique timestamps and sort them
        unique_timestamps = sorted(set(timestamps))
        
        if len(unique_timestamps) <= 1:
            print("Error: Not enough unique timestamps to calculate sample rate.")
            return None
        
        # Calculate time differences between consecutive timestamps
        time_diffs = [unique_timestamps[i+1] - unique_timestamps[i] 
                     for i in range(len(unique_timestamps)-1)]
        
        # Calculate average frequency (Hz)
        sample_rates = [1/diff for diff in time_diffs if diff > 0]
        avg_rate = np.mean(sample_rates)
        
        return avg_rate
    
    except Exception as e:
        print(f"Error: {e}")
        return None

def analyze_dataset_directory(base_dir="DataSet"):
    """
    Analyze all CSV files in the dataset directory structure:
    DataSet > range bin > FilteredCSV > *.csv
    Returns a dictionary of sample rates by range bin.
    """
    # Get the full path to the base directory
    base_path = os.path.join(os.getcwd(), base_dir)
    if not os.path.exists(base_path):
        print(f"Error: Directory '{base_path}' not found.")
        return None, None
    
    # Dictionary to store rates by range bin
    rates_by_bin = defaultdict(list)
    all_rates = []
    
    # Process each range bin directory
    for range_bin in os.listdir(base_path):
        range_bin_path = os.path.join(base_path, range_bin)
        
        # Skip if not a directory
        if not os.path.isdir(range_bin_path):
            continue
            
        # Check for FilteredCSV directory
        filtered_csv_path = os.path.join(range_bin_path, "FilteredCSV")
        if not os.path.exists(filtered_csv_path):
            print(f"Warning: No FilteredCSV directory found in {range_bin_path}")
            continue
            
        # Process each CSV file in the FilteredCSV directory
        csv_files = [f for f in os.listdir(filtered_csv_path) if f.endswith('.csv')]
        
        for csv_file in csv_files:
            file_path = os.path.join(filtered_csv_path, csv_file)
            rate = calculate_avg_sample_rate(file_path)
            
            if rate is not None:
                rates_by_bin[range_bin].append(rate)
                all_rates.append(rate)
                print(f"Processed: {file_path} - Sample rate: {rate:.2f} Hz")
    
    return rates_by_bin, all_rates

def main():
    parser = argparse.ArgumentParser(description='Calculate sample rates from CSV files in DataSet directory.')
    parser.add_argument('--dir', default='DataSet', help='Base directory to scan (default: DataSet)')
    parser.add_argument('file', nargs='?', help='Single CSV file to analyze (optional)')
    
    args = parser.parse_args()
    
    if args.file:
        # Analyze single file
        file_path = args.file
        avg_rate = calculate_avg_sample_rate(file_path)
        
        if avg_rate is not None:
            print(f"Average sample rate for {file_path}: {avg_rate:.2f} Hz")
        else:
            print(f"Failed to calculate average sample rate for {file_path}.")
    else:
        # Analyze entire dataset
        rates_by_bin, all_rates = analyze_dataset_directory(args.dir)
        
        if rates_by_bin and all_rates:
            print("\n===== Sample Rates by Range Bin =====")
            for bin_name, rates in sorted(rates_by_bin.items()):
                avg_bin_rate = np.mean(rates)
                print(f"Range bin {bin_name}: {avg_bin_rate:.2f} Hz (from {len(rates)} files)")
            
            overall_avg = np.mean(all_rates)
            print(f"\nOverall average sample rate: {overall_avg:.2f} Hz")
            print(f"Total files processed: {len(all_rates)}")
        else:
            print("No valid data found or error in processing.")

if __name__ == "__main__":
    main()