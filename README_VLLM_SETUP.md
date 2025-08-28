# 🚀 VerilogCoder vLLM 本地部署指南

本指南将帮助你在本地MacBook上使用vLLM框架运行VerilogCoder项目，无需依赖OpenAI API。

## 📋 前置要求

### 1. Python环境
- Python 3.8+
- pip包管理器

### 2. 硬件要求
- **最低**: 8GB RAM, 4GB VRAM (如果使用GPU)
- **推荐**: 16GB RAM, 8GB+ VRAM
- **CPU**: 支持AVX2指令集

### 3. 操作系统
- macOS 10.15+ (Catalina)
- 支持Metal Performance Shaders (MPS) 用于GPU加速

## 🛠️ 安装步骤

### 1. 安装vLLM
```bash
# 安装vLLM (CPU版本，适合MacBook)
pip install vllm

# 或者安装GPU版本 (如果有NVIDIA GPU)
pip install vllm[gpu]
```

### 2. 安装依赖
```bash
pip install requests
```

## 🚀 使用方法

### 步骤1: 启动vLLM本地服务

```bash
# 启动vLLM服务
python start_vllm_local.py
```

**注意**: 
- 首次启动会下载模型，可能需要几分钟到几小时
- 建议使用较小的模型进行测试，如 `microsoft/DialoGPT-medium`
- 服务启动后会在 `http://localhost:8000` 运行

### 步骤2: 测试配置

在新的终端窗口中运行：
```bash
python test_vllm_config.py
```

这个脚本会：
- 测试vLLM服务连接
- 验证OpenAI兼容性
- 测试VerilogCoder集成

### 步骤3: 切换配置

测试成功后，切换配置文件：
```bash
# 备份原始配置
mv OAI_CONFIG_LIST OAI_CONFIG_LIST.backup

# 使用vLLM配置
mv VLLM_CONFIG_LIST OAI_CONFIG_LIST
```

### 步骤4: 运行VerilogCoder

现在可以运行VerilogCoder项目：
```bash
python run_verilog_coder.py --generate_plan_dir verilog-eval-v2/plans/ --generate_verilog_dir verilog-eval-v2/plan_output/ --verilog_example_dir verilog-eval-v2/dataset_dumpall/
```

## 🔧 配置说明

### VLLM_CONFIG_LIST 结构
```json
[
    {
        "model": "microsoft/DialoGPT-medium",
        "api_base": "http://localhost:8000/v1",
        "api_type": "open_ai",
        "api_key": "dummy-key"
    }
]
```

### 可用的模型选项

#### 轻量级模型 (推荐用于测试)
- `microsoft/DialoGPT-medium` - 345M参数
- `microsoft/DialoGPT-small` - 117M参数
- `distilgpt2` - 82M参数

#### 中等模型
- `gpt2` - 124M参数
- `gpt2-medium` - 355M参数

#### 高级模型 (需要更多资源)
- `gpt2-large` - 774M参数
- `gpt2-xl` - 1.5B参数

## 🎯 性能优化

### 1. 内存优化
```bash
# 启动时限制内存使用
vllm serve microsoft/DialoGPT-medium --max-model-len 512 --gpu-memory-utilization 0.8
```

### 2. 批处理优化
```bash
# 启用批处理以提高吞吐量
vllm serve microsoft/DialoGPT-medium --max-batch-size 8
```

### 3. 量化优化
```bash
# 使用INT8量化减少内存占用
vllm serve microsoft/DialoGPT-medium --quantization int8
```

## 🐛 常见问题

### 1. 内存不足
**症状**: 启动时崩溃或报内存错误
**解决方案**: 
- 使用更小的模型
- 减少 `max-model-len` 参数
- 关闭其他占用内存的应用

### 2. 模型下载失败
**症状**: 长时间卡在下载阶段
**解决方案**:
- 检查网络连接
- 使用国内镜像源
- 手动下载模型文件

### 3. 服务启动失败
**症状**: 端口被占用或权限错误
**解决方案**:
- 检查端口8000是否被占用
- 使用 `--port 8001` 指定其他端口
- 确保有足够的系统权限

## 📊 性能对比

| 模型 | 参数量 | 内存占用 | 推理速度 | 代码质量 |
|------|--------|----------|----------|----------|
| DialoGPT-small | 117M | ~2GB | 快 | 中等 |
| DialoGPT-medium | 345M | ~4GB | 中等 | 良好 |
| GPT-2 | 124M | ~3GB | 快 | 中等 |
| GPT-2-medium | 355M | ~5GB | 中等 | 良好 |

## 🔄 生产环境部署

当本地测试成功后，可以部署到服务器：

### 1. 服务器要求
- Linux系统 (Ubuntu 20.04+)
- NVIDIA GPU (推荐RTX 3090+)
- 32GB+ RAM
- 100GB+ 存储空间

### 2. 部署命令
```bash
# 使用systemd服务
sudo systemctl enable vllm-verilogcoder
sudo systemctl start vllm-verilogcoder

# 或使用Docker
docker run -d --gpus all -p 8000:8000 vllm/verilogcoder
```

## 📚 参考资料

- [vLLM官方文档](https://docs.vllm.ai/)
- [OpenAI API兼容性](https://docs.vllm.ai/en/latest/serving/openai_compatible.html)
- [模型性能基准](https://docs.vllm.ai/en/latest/models/performance.html)

## 🆘 获取帮助

如果遇到问题：
1. 检查vLLM服务状态
2. 查看服务日志
3. 确认配置文件格式
4. 参考vLLM官方文档

---

**注意**: 本地vLLM部署主要用于开发和测试。生产环境建议使用云服务或专用服务器。
