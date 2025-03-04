# VerilogCoder: Autonomous Verilog Coding Agents with Graph-based Planning and Abstract Syntax Tree (AST)-based Waveform Tracing Tool

## Description
VerilogCoder is an autonomous verilog coding agent that using graph-based planning and AST-based waveform tracing tool. The paper is in [https://arxiv.org/abs/2408.08927v1]. We use Verilog Eval Human v2 benchmarks on https://gitlab-master.nvidia.com/avr/verilog-eval-v2/-/tree/main?ref_type=heads for experiments.

## LLM Models
The prompts are finetuned for GPT-4 and Llama3. User can switch to other LLM models with their own prompts.

## Inputs and Outputs for VerilogCoder
- **Input**: Target RTL specification, and testbench. 
- **Output**: Completed functional correct Verilog module.

## Prerequisite Tool Installation
In order to run the waveform tracing tool, user need to install iverilog.

```
git clone https://github.com/steveicarus/iverilog.git && cd iverilog \ 
        && git checkout 01441687235135d1c12eeef920f75d97995da333 \ 
        && sh ./autoconf.sh  
./configure --prefix=<local dir> 
make –j4 
Make install 
export PATH=<local dir>:$PATH 
```

## Usage
1. Use the OAI_CONFIG_LIST to setup the LLM models.
2. Run the example command below.
```
python hardware_agent/examples/VerilogCoder/run_verilog_coder.py --generate_plan_dir hardware_agent/examples/VerilogCoder/verilog-eval-v2/plans/ --generate_verilog_dir hardware_agent/examples/VerilogCoder/verilog-eval-v2/plan_output/ --verilog_example_dir hardware_agent/examples/VerilogCoder/verilog-eval-v2/dataset_dumpall/
```
