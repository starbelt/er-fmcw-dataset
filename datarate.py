import csv
import numpy as np
import argparse
import sys
import os

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

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Calculate the average sample rate from a CSV file.')
    parser.add_argument('file', nargs='?', help='Path to the CSV file')
    args = parser.parse_args()
    
    file_path = args.file
    
    # If no file path was provided as an argument, prompt the user
    if file_path is None:
        file_path = input("Enter the path to the CSV file: ")
    
    # Calculate and print the average sample rate
    avg_rate = calculate_avg_sample_rate(file_path)
    
    if avg_rate is not None:
        print(f"Average sample rate: {avg_rate:.2f} Hz")
    else:
        print("Failed to calculate average sample rate.")

if __name__ == "__main__":
    main()