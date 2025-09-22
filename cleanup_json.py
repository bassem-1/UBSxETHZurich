#!/usr/bin/env python3
"""
JSON Cleanup Script
Processes all JSON files in the data directory to keep only 'task_type' fields
from objects, removing all other fields like 'parameters'.
"""

import json
import os
import glob
from typing import Any, Dict, List, Union

def clean_object(obj: Dict[str, Any]) -> Dict[str, str]:
    """
    Clean a single object to keep only the 'task_type' field.
    
    Args:
        obj: Dictionary object to clean
        
    Returns:
        Dictionary with only 'task_type' field
    """
    if not isinstance(obj, dict):
        return obj
    
    if 'task_type' in obj:
        return {'task_type': obj['task_type']}
    else:
        # If no task_type field, return the object as is (shouldn't happen based on requirements)
        print(f"Warning: Object without 'task_type' field found: {obj}")
        return obj

def clean_json_data(data: Union[List[Dict], Dict]) -> Union[List[Dict], Dict]:
    """
    Clean JSON data - handles both arrays of objects and single objects.
    
    Args:
        data: JSON data to clean
        
    Returns:
        Cleaned JSON data
    """
    if isinstance(data, list):
        # Handle array of objects
        return [clean_object(obj) for obj in data]
    elif isinstance(data, dict):
        # Handle single object
        return clean_object(data)
    else:
        print(f"Warning: Unexpected data type: {type(data)}")
        return data

def process_json_file(file_path: str) -> bool:
    """
    Process a single JSON file.
    
    Args:
        file_path: Path to the JSON file
        
    Returns:
        True if successful, False otherwise
    """
    try:
        # Read the JSON file
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Clean the data
        cleaned_data = clean_json_data(data)
        
        # Write back to the same file with proper formatting
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(cleaned_data, f, indent=2, ensure_ascii=False)
        
        return True
    
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in {file_path}: {e}")
        return False
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return False

def main():
    """Main function to process all JSON files in the data directory."""
    
    # Get the data directory path
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(script_dir, 'data')
    
    if not os.path.exists(data_dir):
        print(f"Error: Data directory not found at {data_dir}")
        return
    
    # Find all JSON files in the data directory
    json_pattern = os.path.join(data_dir, '*.json')
    json_files = glob.glob(json_pattern)
    
    if not json_files:
        print("No JSON files found in the data directory.")
        return
    
    print(f"Found {len(json_files)} JSON files to process.")
    print("=" * 50)
    
    # Process each file
    successful = 0
    failed = 0
    
    for i, file_path in enumerate(json_files, 1):
        file_name = os.path.basename(file_path)
        print(f"[{i}/{len(json_files)}] Processing {file_name}...", end=' ')
        
        if process_json_file(file_path):
            print("✓ Success")
            successful += 1
        else:
            print("✗ Failed")
            failed += 1
    
    print("=" * 50)
    print(f"Processing complete!")
    print(f"Successful: {successful}")
    print(f"Failed: {failed}")
    print(f"Total: {len(json_files)}")

if __name__ == "__main__":
    main()
