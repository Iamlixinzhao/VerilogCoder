#!/usr/bin/env python3
"""
Script to extract all available task IDs from the dataset_dumpall directory
"""

import os
import re

def get_all_task_ids(dataset_dir):
    """
    Extract all task IDs from the dataset_dumpall directory
    """
    if not os.path.exists(dataset_dir):
        print(f"Error: Directory {dataset_dir} does not exist")
        return set()
    
    files = os.listdir(dataset_dir)
    task_ids = set()
    
    for file in files:
        if file.endswith('_prompt.txt'):
            # Extract task ID from filename like "Prob001_zero_prompt.txt"
            # The task ID is "zero" in this case
            match = re.match(r'Prob\d+_(.+)_prompt\.txt', file)
            if match:
                task_id = match.group(1)
                task_ids.add(task_id)
    
    return sorted(list(task_ids))

def main():
    dataset_dir = "hardware_agent/examples/VerilogCoder/verilog-eval-v2/dataset_dumpall/"
    
    print("Scanning directory:", dataset_dir)
    task_ids = get_all_task_ids(dataset_dir)
    
    print(f"\nFound {len(task_ids)} task IDs:")
    for i, task_id in enumerate(task_ids, 1):
        print(f"{i:3d}. {task_id}")
    
    print(f"\nTotal: {len(task_ids)} tasks")
    
    # Generate the set format for copy-paste
    print(f"\nSet format for run_verilog_coder.py:")
    print("user_task_ids = {")
    for task_id in task_ids:
        print(f"    '{task_id}',")
    print("}")

if __name__ == "__main__":
    main()
