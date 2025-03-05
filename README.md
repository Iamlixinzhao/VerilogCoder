# VerilogCoder: Autonomous Verilog Coding Agents with Graph-based Planning and Abstract Syntax Tree (AST)-based Waveform Tracing Tool

## Description
VerilogCoder is an autonomous verilog coding agent that using graph-based planning and AST-based waveform tracing tool. The paper is in [https://arxiv.org/abs/2408.08927v1]. We use Verilog Eval Human v2 benchmarks on https://gitlab-master.nvidia.com/avr/verilog-eval-v2/-/tree/main?ref_type=heads for experiments.

## LLM Models
The prompts are finetuned for GPT-4 and Llama3. User can switch to other LLM models with their own prompts.

## Benchmark and Generated .sv from VerilogCoder in the paper
- **Case Dir**: ```<project_home_dir>/hardware_agent/examples/VerilogCoder/verilog-eval-v2/```
- **Benchmark Dir**: ```<case_dir>/dataset_dumpall```
- **VerilogCoder Generated Plan Reference Dir**: ```<case_dir>/plans```
- **VerilogCoder Generated Verilog File Reference Dir**: ```<case_dir>/plan_output```

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

## Installation

1. Create conda environment
```
#Create conda env with python >= 3.10
conda create -n hardware_agent python=3.10.13
conda activate hardware_agent
```

2. Install the packages
```
#setup environment in conda env
pip install -e . or python setup.py install (non-editable mode)
pip install pypdf
pip install PILLOW
pip install network
pip install matplotlib
pip install pydantic==2.10.1
pip install langchain==0.3.14
pip install llangchain_openai==0.2.14
pip install langchain_community==0.3.14
pip install chromadb==0.4.24
pip install IPython 
pip install markdownify 
pip install pypdf 
pip install sentence_transformers==2.7.0
pip install -U chainlit 
export PYTHONPATH=<cur_dir_path>:$PYTHONPATH
```

## Quick Start
1. Use the OAI_CONFIG_LIST to setup the LLM models.
```
[
    {
        "model": "gpt-4-turbo",
	"api_key": ""
    }
]
```

2. make a temp working directory.
```
mkdir verilog_tool_tmp
```

3. Select the cases to run VerilogCoder in hardware_agent/examples/VerilogCoder/run_verilog_coder.py using user_task_ids.
```
# Load verilog problem sets
# Add questions
user_task_ids = {'zero'}
case_manager = VerilogCaseManager(file_path=args.verilog_example_dir, task_ids=user_task_ids)
```

4. Run the command for "python hardware_agent/examples/VerilogCoder/run_verilog_coder.py --generate_plan_dir <TCRG_plan_dir> --generate_verilog_dir <Verilog_code_dir> --verilog_example_dir <Verilog_Eval_v2_benchmark_dir>".
   
Example:
```
python hardware_agent/examples/VerilogCoder/run_verilog_coder.py --generate_plan_dir <case_dir>/plans/ --generate_verilog_dir <case_dir>/plan_output/ --verilog_example_dir <case_dir>
```


