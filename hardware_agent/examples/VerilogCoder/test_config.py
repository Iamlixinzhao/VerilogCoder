#!/usr/bin/env python3
"""
Test script to verify configuration import works correctly
"""

def test_config_import():
    """Test if configuration can be imported correctly"""
    try:
        from hardware_agent.examples.VerilogCoder.run_config import (
            get_task_ids_to_run, 
            get_task_count_info,
            RUN_ALL_TASKS
        )
        print("✅ Configuration import successful!")
        print(f"   RUN_ALL_TASKS: {RUN_ALL_TASKS}")
        print(f"   Task IDs to run: {get_task_ids_to_run()}")
        print(f"   Task count info: {get_task_count_info()}")
        return True
    except ImportError as e:
        print(f"❌ Configuration import failed: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def test_verilog_case_manager():
    """Test if VerilogCaseManager can be created with config"""
    try:
        from hardware_agent.examples.VerilogCoder.verilog_examples_manager import VerilogCaseManager
        from hardware_agent.examples.VerilogCoder.run_config import get_task_ids_to_run
        
        task_ids = get_task_ids_to_run()
        dataset_dir = "hardware_agent/examples/VerilogCoder/verilog-eval-v2/dataset_dumpall/"
        
        case_manager = VerilogCaseManager(file_path=dataset_dir, task_ids=task_ids)
        total_tasks = case_manager.total_tasks()
        
        print(f"✅ VerilogCaseManager created successfully!")
        print(f"   Total tasks: {total_tasks}")
        print(f"   First task ID: {case_manager.get_cur_task_id()}")
        return True
    except Exception as e:
        print(f"❌ VerilogCaseManager test failed: {e}")
        return False

if __name__ == "__main__":
    print("Testing VerilogCoder Configuration...")
    print("=" * 50)
    
    config_ok = test_config_import()
    print()
    
    if config_ok:
        case_manager_ok = test_verilog_case_manager()
        print()
        
        if case_manager_ok:
            print("🎉 All tests passed! Configuration is ready to use.")
        else:
            print("⚠️  Some tests failed. Please check the configuration.")
    else:
        print("❌ Configuration test failed. Please fix the configuration first.")
