#!/usr/bin/env python3
"""
Configuration file for VerilogCoder run modes
"""

# =============================================================================
# RUN MODES - Choose one of the following options:
# =============================================================================

# Option 1: Run ALL available tasks (156 tasks)
# This will process every single Verilog problem in the dataset
RUN_ALL_TASKS = True

# Option 2: Run specific tasks only
# Uncomment and modify the line below to run specific tasks
# RUN_ALL_TASKS = False
# SPECIFIC_TASK_IDS = {
#     'zero',           # Simple zero output
#     'mux2to1',        # 2-to-1 multiplexer
#     'dff',            # D flip-flop
#     'fsm1',           # Finite state machine 1
#     'vector2',        # Vector operations
# }

# Option 3: Run a subset of tasks for testing
# Uncomment and modify the line below to run a subset
# RUN_ALL_TASKS = False
# SPECIFIC_TASK_IDS = {
#     'zero',           # Simple zero output
#     'notgate',        # NOT gate
#     'andgate',        # AND gate
#     'norgate',        # NOR gate
# }

# =============================================================================
# ADVANCED CONFIGURATION
# =============================================================================

# Maximum number of tasks to run (useful for testing with large datasets)
# Set to None for unlimited, or set a number like 10 for testing
MAX_TASKS_TO_RUN = None

# Skip tasks that already have generated outputs
SKIP_COMPLETED_TASKS = False

# =============================================================================
# TASK CATEGORIES (for reference)
# =============================================================================

# Basic gates and combinational logic
BASIC_GATES = {
    'zero', 'notgate', 'andgate', 'norgate', 'xnorgate',
    'gates', 'gates4', 'gates100', 'gatesv', 'gatesv100'
}

# Sequential logic
SEQUENTIAL = {
    'dff', 'dff8', 'dff8ar', 'dff8p', 'dff8r', 'dff16e',
    'count10', 'count15', 'count1to10', 'count_clock', 'countbcd'
}

# Finite State Machines
FSM_TASKS = {
    'fsm1', 'fsm1s', 'fsm2', 'fsm2s', 'fsm3', 'fsm3comb',
    'fsm3onehot', 'fsm3s', 'fsm_hdlc', 'fsm_onehot',
    'fsm_ps2', 'fsm_ps2data', 'fsm_serial', 'fsm_serialdata'
}

# Vector operations
VECTOR_TASKS = {
    'vector0', 'vector1', 'vector2', 'vector3', 'vector4', 'vector5',
    'vector100r', 'vectorr', 'vectorgates'
}

# Circuit problems
CIRCUIT_TASKS = {
    'circuit1', 'circuit2', 'circuit3', 'circuit4', 'circuit5',
    'circuit6', 'circuit7', 'circuit8', 'circuit9', 'circuit10'
}

# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def get_task_ids_to_run():
    """
    Get the task IDs that should be run based on configuration
    """
    if RUN_ALL_TASKS:
        return set()  # Empty set means run all available tasks
    else:
        return SPECIFIC_TASK_IDS

def get_task_count_info():
    """
    Get information about how many tasks will be run
    """
    if RUN_ALL_TASKS:
        return "ALL available tasks (156 tasks)"
    else:
        count = len(SPECIFIC_TASK_IDS)
        return f"{count} specific tasks: {', '.join(sorted(SPECIFIC_TASK_IDS))}"

if __name__ == "__main__":
    print("VerilogCoder Configuration")
    print("=" * 40)
    print(f"Run mode: {get_task_count_info()}")
    print(f"Max tasks: {MAX_TASKS_TO_RUN or 'Unlimited'}")
    print(f"Skip completed: {SKIP_COMPLETED_TASKS}")
