#!/usr/bin/env python3
"""
File Merge Script
Merges TXT content into corresponding JSON files by adding a 'text' field.
This script is designed to be surgical and careful with the merge operation.
"""

import json
import os
import glob
from typing import Dict, List, Any

def read_text_file(file_path: str) -> str:
    """
    Safely read text file content.
    
    Args:
        file_path: Path to the text file
        
    Returns:
        Content of the text file as string
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read().strip()
    except Exception as e:
        raise Exception(f"Error reading text file {file_path}: {e}")

def read_json_file(file_path: str) -> Any:
    """
    Safely read JSON file content.
    
    Args:
        file_path: Path to the JSON file
        
    Returns:
        Parsed JSON data
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        raise Exception(f"Invalid JSON in {file_path}: {e}")
    except Exception as e:
        raise Exception(f"Error reading JSON file {file_path}: {e}")

def write_json_file(file_path: str, data: Any) -> None:
    """
    Safely write JSON file with proper formatting.
    
    Args:
        file_path: Path to the JSON file
        data: Data to write
    """
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    except Exception as e:
        raise Exception(f"Error writing JSON file {file_path}: {e}")

def merge_files(json_path: str, txt_path: str) -> bool:
    """
    Merge TXT content into JSON file by adding a 'text' field.
    
    Args:
        json_path: Path to the JSON file
        txt_path: Path to the TXT file
        
    Returns:
        True if successful, False otherwise
    """
    try:
        # Read both files
        json_data = read_json_file(json_path)
        txt_content = read_text_file(txt_path)
        
        # Handle different JSON structures
        if isinstance(json_data, list):
            # If it's an array, add text field to the root level
            # Create a new structure with the array and text field
            merged_data = {
                "tasks": json_data,
                "text": txt_content
            }
        elif isinstance(json_data, dict):
            # If it's an object, add text field to existing object
            merged_data = json_data.copy()
            merged_data["text"] = txt_content
        else:
            # Unexpected structure, wrap it
            merged_data = {
                "data": json_data,
                "text": txt_content
            }
        
        # Write the merged data back to JSON file
        write_json_file(json_path, merged_data)
        return True
        
    except Exception as e:
        print(f"  Error: {e}")
        return False

def find_file_pairs(data_dir: str) -> List[tuple]:
    """
    Find all JSON-TXT file pairs in the directory.
    
    Args:
        data_dir: Path to the data directory
        
    Returns:
        List of tuples (json_path, txt_path, basename)
    """
    json_files = glob.glob(os.path.join(data_dir, '*.json'))
    pairs = []
    
    for json_path in json_files:
        basename = os.path.splitext(os.path.basename(json_path))[0]
        txt_path = os.path.join(data_dir, f"{basename}.txt")
        
        if os.path.exists(txt_path):
            pairs.append((json_path, txt_path, basename))
        else:
            print(f"Warning: No corresponding TXT file found for {basename}.json")
    
    return pairs

def main():
    """Main function to merge all TXT files into corresponding JSON files."""
    
    # Get the data directory path
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(script_dir, 'data')
    
    if not os.path.exists(data_dir):
        print(f"Error: Data directory not found at {data_dir}")
        return
    
    # Find all file pairs
    pairs = find_file_pairs(data_dir)
    
    if not pairs:
        print("No file pairs found to merge.")
        return
    
    print(f"Found {len(pairs)} file pairs to merge.")
    print("=" * 60)
    
    # Process each pair
    successful = 0
    failed = 0
    
    for i, (json_path, txt_path, basename) in enumerate(pairs, 1):
        print(f"[{i}/{len(pairs)}] Merging {basename}...", end=' ')
        
        if merge_files(json_path, txt_path):
            print("✓ Success")
            successful += 1
        else:
            print("✗ Failed")
            failed += 1
    
    print("=" * 60)
    print(f"Merge operation complete!")
    print(f"Successful: {successful}")
    print(f"Failed: {failed}")
    print(f"Total pairs: {len(pairs)}")
    
    if failed == 0:
        print("\n🎉 All files merged successfully! Ready for TXT file cleanup.")
    else:
        print(f"\n⚠️  {failed} files failed to merge. Please review before cleanup.")

if __name__ == "__main__":
    main()
