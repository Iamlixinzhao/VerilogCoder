## Hardware Agent Marco

It is a framework for LLM based hardware agent framework, including the RAG, ReACT, memory management, planner, and multi-agent collaborate framework. 
Marco Chat Bot is availabe for code base related questions and quick start.

**Note: It is still in a preliminary development phase. The main branch is protected now until ci test and code review are setup.**

## Installation

1. Create conda environment
```
#Create conda env with python >= 3.10
conda create -n hardware_agent python=3.10.13
conda activate hardware_agent
```

2. ADLR Gateway Chat Installation
- Apply the DL access to chipnemo-llmgateway-access
- Install ADLRchat
```   
% pip config set global.index-url https://urm.nvidia.com/artifactory/api/pypi/nv-shared-pypi/simple 
% pip install -U adlrchat==0.1.29
% adlrchat-login --role adlrchat-chipnemo-llmgateway --servername llm_gateway --refresh True
```

3. Install the packages
```
#setup environment in conda env
pip install -e . or python setup.py install (non-editable mode)
pip install pypdf
pip install PILLOW
pip install network
pip install matplotlib
pip install langchain==0.3.14
pip install llangchain_openai==0.2.14
pip install langchain_community==0.3.14
pip install chromadb==0.4.24
pip install pydantic==2.10.1
pip install IPython 
pip install markdownify 
pip install pypdf 
pip install sentence_transformers
pip install -U chainlit 
export PYTHONPATH=<hardware_agent_path>:$PYTHONPATH
```

### llamaindex install for RAG
Install Nov. 11. 2024 llamaindex version.
```
pip install llama-index==0.11.23
pip install llama-index-llms-nvidia==0.2.7 
pip install llama-index-embeddings-nvidia==0.2.5 
pip install llama-index-postprocessor-nvidia-rerank==0.3.3 
pip install llama-index-postprocessor-rankgpt-rerank==0.2.0 
pip install llama-index-vector-stores-chroma==0.2.2 
pip insatll llama-index-readers-confluence==0.2.2 
```

## Upgrade ADLR from old version: Upgrade ADLR chat library from 0.1.5 to 0.1.29
The instructions for upgrading the env from old adlrchat library.
```
pip install -U adlrchat==0.1.29 
pip install -U chainlit 
pip uninstall pydantic-core 
pip uninstall pydantic 
pip install pydantic==2.10.1 
pip uninstall langchain-cohere 
pip install langchain-cohere 
```

## Unit test
1. Provide your ChipNemo NVCF API key in OAI_CONFIG_LIST_CHIPNEMO_NVCF file. Instruction to generate API key: https://nvidia-my.sharepoint.com/:w:/p/chiatungh/EeWVUCehvw9Grfv_GvZ3D1wBjA28g-Mc5RWsIu7a-sxnfA?e=oJ0OeN
2. Run unit test.
```
python -m unittest hardware_agent.tests.hardware_agent_tests.TestHardwareAgent
```

## Hardware agent directory
(project_dir)/hardware_agent/

## Hardware agent chat bot for code base query and quick start 🚀🚀
```
python hardware_agent/AutoConfigGen/marco_chat_agent.py
```
Chat Bot README: https://gitlab-master.nvidia.com/avr/hardware-agent-marco/-/blob/main/hardware_agent/AutoConfigGen/README.md

## Docker
Docker is used in the agent system to provide a securely isolated environment for agent actions. It allows for arbitrary code execution, web browsing, and other actions without the risk of harming the user's system

check [./devcontainer](https://gitlab-master.nvidia.com/avr/hardware-agent-marco/-/tree/generalist_agent/.devcontainer?ref_type=heads) for docker setup and usage


