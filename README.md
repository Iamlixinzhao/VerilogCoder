# VerilogCoder

一个基于AI的Verilog代码生成和验证工具，支持多种LLM后端，包括OpenAI API和本地vLLM服务。

## 🚀 项目特性

- **AI驱动的Verilog代码生成**: 使用大语言模型自动生成Verilog代码
- **多LLM后端支持**: 支持OpenAI API、本地vLLM服务等
- **Verilog验证**: 集成iverilog进行代码编译和仿真验证
- **批量测试**: 支持Verilog-Eval-v2基准测试集的批量处理
- **智能错误检测**: 自动识别和修复常见的Verilog语法错误

## 🏗️ 项目结构

```
VerilogCoder/
├── hardware_agent/           # 硬件代理核心模块
│   ├── examples/            # 示例和测试
│   │   └── VerilogCoder/   # VerilogCoder主程序
│   └── general_agent.py    # 通用代理模块
├── autogen/                 # AutoGen框架核心
├── setup.py                 # 安装配置
├── OAI_CONFIG_LIST         # LLM配置文件
└── README.md               # 项目说明
```

## 📋 系统要求

- Python 3.8+
- iverilog (用于Verilog编译和仿真)
- 足够的磁盘空间用于模型缓存

## 🛠️ 安装步骤

### 1. 克隆项目
```bash
git clone https://github.com/yourusername/VerilogCoder.git
cd VerilogCoder
```

### 2. 创建虚拟环境
```bash
conda create -n hardware_agent python=3.10
conda activate hardware_agent
```

### 3. 安装依赖
```bash
pip install -e .
pip install vcdvcd pandas ply
```

### 4. 安装iverilog
```bash
# macOS
brew install icarus-verilog

# Ubuntu/Debian
sudo apt-get install iverilog

# CentOS/RHEL
sudo yum install iverilog
```

## 🔧 配置

### OpenAI API配置
创建 `OAI_CONFIG_LIST` 文件：
```json
[
    {
        "model": "gpt-4o",
        "api_key": "your-openai-api-key"
    }
]
```

### vLLM本地服务配置
```json
[
    {
        "model": "microsoft/DialoGPT-small",
        "api_base": "http://localhost:8000/v1",
        "api_type": "open_ai",
        "api_key": "dummy-key"
    }
]
```

## 🚀 使用方法

### 启动vLLM本地服务
```bash
# 启动vLLM服务
vllm serve microsoft/DialoGPT-small --host 0.0.0.0 --port 8000 -O0

# 或者使用启动脚本
python start_vllm_local.py
```

### 运行VerilogCoder
```bash
cd hardware_agent/examples/VerilogCoder

# 运行单个测试
python run_verilog_coder.py \
    --generate_plan_dir verilog-eval-v2/plan_output \
    --generate_verilog_dir verilog-eval-v2/plan_output \
    --verilog_example_dir verilog-eval-v2/dataset_dumpall

# 运行所有测试
python run_verilog_coder.py \
    --generate_plan_dir verilog-eval-v2/plan_output \
    --generate_verilog_dir verilog-eval-v2/plan_output \
    --verilog_example_dir verilog-eval-v2/dataset_dumpall
```

### 分析结果
```bash
# 分析生成结果
python analyze_verilogcoder_results.py

# 测试特定任务
python analyze_verilogcoder_results.py --test-only zero
```

## 📊 性能评估

项目支持Verilog-Eval-v2基准测试集，包含156个Verilog编码任务，涵盖：
- 基本逻辑门
- 组合逻辑电路
- 时序逻辑电路
- 复杂数字系统

## 🔍 故障排除

### 常见问题

1. **ModuleNotFoundError**: 确保已激活正确的conda环境
2. **iverilog未找到**: 检查iverilog是否正确安装并添加到PATH
3. **vLLM启动失败**: 检查模型名称和端口配置

### 调试模式
```bash
# 启用详细日志
export TORCHDYNAMO_VERBOSE=1
export TORCH_LOGS="+dynamo"
```

## 🤝 贡献指南

欢迎提交Issue和Pull Request！请确保：
- 代码符合PEP 8规范
- 添加适当的测试用例
- 更新相关文档

## 📄 许可证

本项目采用MIT许可证 - 详见 [LICENSE](LICENSE) 文件

## 🙏 致谢

- [AutoGen](https://github.com/microsoft/autogen) - 多智能体对话框架
- [vLLM](https://github.com/vllm-project/vllm) - 高性能LLM推理引擎
- [Verilog-Eval-v2](https://github.com/NVlabs/verilog-eval) - Verilog评估基准

## 📞 联系方式

如有问题或建议，请通过以下方式联系：
- 提交GitHub Issue
- 发送邮件至: your-email@example.com

---

⭐ 如果这个项目对你有帮助，请给它一个星标！

