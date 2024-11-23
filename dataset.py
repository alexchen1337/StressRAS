import kagglehub
import pandas as pd
import os

# Download latest version
path = kagglehub.dataset_download("ryanluong1/valorant-champion-tour-2021-2023-data")

# Create data directory if it doesn't exist
data_dir = os.path.join(os.path.dirname(__file__), "data")
os.makedirs(data_dir, exist_ok=True)

# Move downloaded files to data directory and convert CSV to TSV
if isinstance(path, str):
    path = [path]  # Convert single path to list if necessary
    
for file in path:
    # First determine if we should convert to TSV
    is_csv = file.lower().endswith('.csv')
    
    # Prepare destination path - change extension to .tsv if needed
    base_name = os.path.basename(file)
    if is_csv:
        base_name = base_name.rsplit('.', 1)[0] + '.tsv'
    dest = os.path.join(data_dir, base_name)
    
    # Remove destination file if it already exists
    if os.path.exists(dest):
        try:
            os.remove(dest)
        except PermissionError:
            print(f"Warning: Could not remove existing file {dest}. Trying to continue...")
            continue
            
    # For CSV files, read and save directly as TSV
    if is_csv:
        try:
            df = pd.read_csv(file)
            df.to_csv(dest, sep='\t', index=False)
            print(f"Converted {os.path.basename(file)} to TSV format")
        except Exception as e:
            print(f"Error converting {file} to TSV: {str(e)}")
            continue
    else:
        # For non-CSV files, just move them
        try:
            os.rename(file, dest)
        except PermissionError:
            print(f"Error: Could not move file {file} to {dest}. Please check file permissions.")
            continue

print("Dataset files saved to:", data_dir)

# Move these function definitions before the call
def split_large_csv(file_path, max_size_mb=95):
    # Convert MB to bytes
    max_size_bytes = max_size_mb * 1024 * 1024
    
    # Get the base name and directory of the file
    base_name = os.path.splitext(os.path.basename(file_path))[0]
    directory = os.path.dirname(file_path)
    
    # Read the CSV in chunks
    chunk_size = 10000  # Adjust this number based on your RAM capacity
    chunks = pd.read_csv(file_path, chunksize=chunk_size)
    
    current_size = 0
    current_chunk = []
    file_counter = 1
    
    for chunk in chunks:
        current_chunk.append(chunk)
        # Estimate size in memory
        current_size += chunk.memory_usage(deep=True).sum()
        
        if current_size >= max_size_bytes:
            # Combine and save current chunks
            combined_df = pd.concat(current_chunk, ignore_index=True)
            output_path = os.path.join(directory, f"{base_name}_part{file_counter}.csv")
            combined_df.to_csv(output_path, index=False)
            print(f"Created {output_path}")
            
            # Reset for next file
            current_chunk = []
            current_size = 0
            file_counter += 1
    
    # Save any remaining data
    if current_chunk:
        combined_df = pd.concat(current_chunk, ignore_index=True)
        output_path = os.path.join(directory, f"{base_name}_part{file_counter}.csv")
        combined_df.to_csv(output_path, index=False)
        print(f"Created {output_path}")

def process_data_directory(directory_path, max_size_mb=95):
    for file in os.listdir(directory_path):
        if file.endswith('.csv'):
            file_path = os.path.join(directory_path, file)
            file_size_mb = os.path.getsize(file_path) / (1024 * 1024)
            
            if file_size_mb > max_size_mb:
                print(f"\nSplitting {file} ({file_size_mb:.2f} MB)...")
                split_large_csv(file_path, max_size_mb)
            else:
                print(f"\nSkipping {file} ({file_size_mb:.2f} MB) - under size limit")

# Now call the function
process_data_directory(data_dir)

if __name__ == "__main__":
    data_dir = os.path.join(os.path.dirname(__file__), "data")
    process_data_directory(data_dir)