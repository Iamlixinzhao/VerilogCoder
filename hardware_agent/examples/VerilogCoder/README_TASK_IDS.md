# 任务ID管理说明

## 📁 文件结构

- `all_task_ids.txt` - 包含所有156个任务ID的文本文件
- `run_verilog_coder.py` - 主运行脚本，自动从txt文件读取任务ID

## 🚀 使用方法

### 1. 运行所有任务 (默认)
```bash
python hardware_agent/examples/VerilogCoder/run_verilog_coder.py \
    --generate_plan_dir hardware_agent/examples/VerilogCoder/verilog-eval-v2/plans/ \
    --generate_verilog_dir hardware_agent/examples/VerilogCoder/verilog-eval-v2/plan_output/ \
    --verilog_example_dir hardware_agent/examples/VerilogCoder/verilog-eval-v2/dataset_dumpall/
```

脚本会自动读取 `all_task_ids.txt` 文件中的所有任务ID。

### 2. 自定义任务列表

如果你想只运行特定的任务，可以：

#### 方法A: 修改txt文件
编辑 `all_task_ids.txt`，只保留你想要运行的任务ID，每行一个：
```txt
zero
mux2to1
dff
fsm1
```

#### 方法B: 创建新的txt文件
创建一个新的txt文件，比如 `my_tasks.txt`：
```txt
zero
notgate
andgate
norgate
```

然后修改 `run_verilog_coder.py` 中的文件路径：
```python
task_id_file = "hardware_agent/examples/VerilogCoder/my_tasks.txt"
```

## 🔧 任务ID分类

### 基本门电路
```
zero, notgate, andgate, norgate, xnorgate
gates, gates4, gates100, gatesv, gatesv100
```

### 时序逻辑
```
dff, dff8, dff8ar, dff8p, dff8r, dff16e
count10, count15, count1to10, count_clock, countbcd
```

### 有限状态机
```
fsm1, fsm1s, fsm2, fsm2s, fsm3, fsm3comb
fsm3onehot, fsm3s, fsm_hdlc, fsm_onehot
fsm_ps2, fsm_ps2data, fsm_serial, fsm_serialdata
```

### 向量操作
```
vector0, vector1, vector2, vector3, vector4, vector5
vector100r, vectorr, vectorgates
```

### 电路问题
```
circuit1, circuit2, circuit3, circuit4, circuit5
circuit6, circuit7, circuit8, circuit9, circuit10
```

## 📝 文件格式

`all_task_ids.txt` 文件格式：
- 每行一个任务ID
- 忽略空行和只包含空格的行
- 自动去除每行首尾的空白字符
- 支持注释（以#开头的行会被忽略）

示例：
```txt
# 基本门电路
zero
notgate
andgate

# 时序逻辑
dff
dff8

# 有限状态机
fsm1
fsm2
```

## ⚠️ 注意事项

1. **文件路径**: 确保txt文件路径正确
2. **文件编码**: 使用UTF-8编码保存txt文件
3. **错误处理**: 如果txt文件不存在或读取失败，脚本会自动回退到运行单个任务 `{'zero'}`
4. **任务数量**: 运行所有156个任务可能需要很长时间，建议先用少量任务测试

## 🛠️ 故障排除

### 常见问题

1. **文件未找到**: 检查txt文件路径是否正确
2. **编码问题**: 确保txt文件使用UTF-8编码
3. **权限问题**: 确保脚本有读取txt文件的权限

### 调试方法

1. 检查控制台输出，确认任务数量
2. 验证txt文件内容是否正确
3. 尝试手动运行单个任务进行测试

## 📊 优势

- **易维护**: 任务ID列表集中管理
- **易修改**: 无需修改Python代码即可调整任务列表
- **易分享**: 可以轻松分享不同的任务配置
- **易版本控制**: txt文件可以单独进行版本控制
