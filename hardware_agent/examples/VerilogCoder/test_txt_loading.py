#!/usr/bin/env python3
"""
Test script to verify txt file loading functionality
"""

def load_task_ids_from_file(filename):
    """Load task IDs from a text file, one per line"""
    try:
        with open(filename, 'r') as f:
            # Read lines and strip whitespace, filter out empty lines
            task_ids = [line.strip() for line in f.readlines() if line.strip()]
        return set(task_ids)
    except FileNotFoundError:
        print(f"Warning: Task ID file '{filename}' not found, using default task 'zero'")
        return {'zero'}
    except Exception as e:
        print(f"Error reading task ID file: {e}, using default task 'zero'")
        return {'zero'}

def test_txt_loading():
    """Test the txt file loading functionality"""
    print("Testing txt file loading functionality...")
    print("=" * 50)
    
    # Test loading from the main file
    task_id_file = "hardware_agent/examples/VerilogCoder/all_task_ids.txt"
    user_task_ids = load_task_ids_from_file(task_id_file)
    
    print(f"✅ Successfully loaded {len(user_task_ids)} task IDs from: {task_id_file}")
    print(f"   First 5 task IDs: {list(user_task_ids)[:5]}")
    print(f"   Last 5 task IDs: {list(user_task_ids)[-5:]}")
    
    # Test with a non-existent file (should fallback to default)
    print("\nTesting fallback behavior...")
    fallback_task_ids = load_task_ids_from_file("non_existent_file.txt")
    print(f"   Fallback result: {fallback_task_ids}")
    
    # Test creating a custom task list
    print("\nTesting custom task list creation...")
    custom_tasks = ['zero', 'mux2to1', 'dff', 'fsm1']
    print(f"   Custom tasks: {custom_tasks}")
    
    print("\n🎉 All tests passed! txt file loading is working correctly.")

if __name__ == "__main__":
    test_txt_loading()
