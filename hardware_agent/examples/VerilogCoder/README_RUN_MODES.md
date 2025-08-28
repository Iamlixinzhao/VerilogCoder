# VerilogCoder 运行模式说明

## 🚀 快速开始

### 运行所有测试 (156个任务)
```bash
python hardware_agent/examples/VerilogCoder/run_verilog_coder.py \
    --generate_plan_dir hardware_agent/examples/VerilogCoder/verilog-eval-v2/plans/ \
    --generate_verilog_dir hardware_agent/examples/VerilogCoder/verilog-eval-v2/plan_output/ \
    --verilog_example_dir hardware_agent/examples/VerilogCoder/verilog-eval-v2/dataset_dumpall/
```

### 运行单个测试 (用于调试)
```bash
# 修改 run_config.py 中的 RUN_ALL_TASKS = False
# 并设置 SPECIFIC_TASK_IDS = {'zero'}
```

## 📋 运行模式

### 1. 运行所有测试 (默认模式)
- **配置文件**: `run_config.py` 中设置 `RUN_ALL_TASKS = True`
- **任务数量**: 156个Verilog设计问题
- **适用场景**: 完整测试、性能评估、基准测试

### 2. 运行特定测试
- **配置文件**: `run_config.py` 中设置 `RUN_ALL_TASKS = False`
- **自定义任务**: 在 `SPECIFIC_TASK_IDS` 中指定要运行的任务
- **适用场景**: 调试特定问题、测试特定功能

### 3. 运行测试子集
- **配置文件**: 使用预定义的任务类别
- **示例**: 只运行基本门电路、FSM、向量操作等

## ⚙️ 配置选项

### 基本配置
```python
# run_config.py

# 运行所有任务
RUN_ALL_TASKS = True

# 或运行特定任务
RUN_ALL_TASKS = False
SPECIFIC_TASK_IDS = {'zero', 'mux2to1', 'dff'}
```

### 高级配置
```python
# 限制最大任务数量 (用于测试)
MAX_TASKS_TO_RUN = 10

# 跳过已完成的任务
SKIP_COMPLETED_TASKS = True
```

## 🎯 任务分类

### 基本门电路
- `zero`, `notgate`, `andgate`, `norgate`, `xnorgate`
- `gates`, `gates4`, `gates100`, `gatesv`, `gatesv100`

### 时序逻辑
- `dff`, `dff8`, `dff8ar`, `dff8p`, `dff8r`, `dff16e`
- `count10`, `count15`, `count1to10`, `count_clock`, `countbcd`

### 有限状态机
- `fsm1`, `fsm1s`, `fsm2`, `fsm2s`, `fsm3`, `fsm3comb`
- `fsm3onehot`, `fsm3s`, `fsm_hdlc`, `fsm_onehot`
- `fsm_ps2`, `fsm_ps2data`, `fsm_serial`, `fsm_serialdata`

### 向量操作
- `vector0`, `vector1`, `vector2`, `vector3`, `vector4`, `vector5`
- `vector100r`, `vectorr`, `vectorgates`

### 电路问题
- `circuit1`, `circuit2`, `circuit3`, `circuit4`, `circuit5`
- `circuit6`, `circuit7`, `circuit8`, `circuit9`, `circuit10`

## 🔧 使用示例

### 示例1: 只运行基本门电路
```python
# run_config.py
RUN_ALL_TASKS = False
SPECIFIC_TASK_IDS = {
    'zero', 'notgate', 'andgate', 'norgate', 'xnorgate'
}
```

### 示例2: 只运行FSM相关任务
```python
# run_config.py
RUN_ALL_TASKS = False
SPECIFIC_TASK_IDS = {
    'fsm1', 'fsm2', 'fsm3', 'fsm_hdlc', 'fsm_onehot'
}
```

### 示例3: 限制任务数量进行测试
```python
# run_config.py
RUN_ALL_TASKS = True
MAX_TASKS_TO_RUN = 5  # 只运行前5个任务
```

## 📊 输出说明

### 进度显示
```
[Info]: Starting to process 156 tasks...
============================================================

[Task 1/156]: Processing 'zero'
----------------------------------------
✅ Task 'zero' completed successfully
Progress: 0.6% (1/156)

[Task 2/156]: Processing 'mux2to1'
----------------------------------------
✅ Task 'mux2to1' completed successfully
Progress: 1.3% (2/156)
```

### 最终结果
```
============================================================
🏁 FINAL RESULTS
============================================================
✅ Passed tasks: 150
   zero, mux2to1, dff, fsm1, vector2, ...

❌ Failed tasks: 6
   kmap2, edgedetect2, m2014_q4d, ...

📊 Success rate: 96.2% (150/156)
============================================================
```

## 🚨 注意事项

1. **运行时间**: 运行所有156个任务可能需要很长时间，建议先用少量任务测试
2. **资源消耗**: 确保有足够的内存和存储空间
3. **API限制**: 如果使用付费API，注意调用次数和成本
4. **错误处理**: 脚本会自动跳过出错的任务，继续处理其他任务

## 🛠️ 故障排除

### 常见问题
1. **配置导入错误**: 确保 `run_config.py` 文件在正确位置
2. **任务ID不存在**: 检查任务ID是否在可用列表中
3. **内存不足**: 减少同时运行的任务数量

### 调试模式
```python
# run_config.py
RUN_ALL_TASKS = False
SPECIFIC_TASK_IDS = {'zero'}  # 只运行一个简单任务
MAX_TASKS_TO_RUN = 1
```
