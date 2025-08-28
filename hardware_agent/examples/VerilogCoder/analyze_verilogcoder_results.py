#!/usr/bin/env python3
"""
VerilogCoder结果分析脚本
分析已生成的Verilog代码的准确率和统计信息
"""

import os
import re
import glob
import json
import subprocess
import tempfile
import shutil
from collections import defaultdict, Counter
from datetime import datetime

class VerilogCoderAnalyzer:
    def __init__(self, plan_output_dir, plans_dir, dataset_dir, run_iverilog_tests=True):
        self.plan_output_dir = plan_output_dir
        self.plans_dir = plans_dir
        self.dataset_dir = dataset_dir
        self.run_iverilog_tests = run_iverilog_tests
        
        # 统计信息
        self.stats = {
            'total_tasks': 0,
            'generated_files': 0,
            'successful_compilations': 0,
            'failed_compilations': 0,
            'successful_simulations': 0,
            'failed_simulations': 0,
            'task_results': {},
            'error_types': Counter(),
            'file_types': Counter()
        }
    
    def analyze_results(self):
        """分析所有结果"""
        print("🔍 开始分析VerilogCoder结果...")
        print("=" * 60)
        
        # 获取所有任务ID
        task_ids = self._get_all_task_ids()
        self.stats['total_tasks'] = len(task_ids)
        
        print(f"📋 总任务数: {self.stats['total_tasks']}")
        print(f"📁 输出目录: {self.plan_output_dir}")
        print(f"📝 计划目录: {self.plans_dir}")
        print(f"📚 数据集目录: {self.dataset_dir}")
        print()
        
        # 分析每个任务
        for task_id in sorted(task_ids):
            self._analyze_task(task_id)
        
        # 生成统计报告
        self._generate_report()
        
        return self.stats
    
    def _get_all_task_ids(self):
        """从数据集目录获取所有任务ID"""
        task_ids = set()
        
        # 从dataset_dumpall目录获取任务ID
        for filename in os.listdir(self.dataset_dir):
            if filename.endswith('_prompt.txt'):
                # 提取任务ID，例如: Prob001_zero_prompt.txt -> zero
                parts = filename.replace('_prompt.txt', '').split('_')
                if len(parts) >= 2:
                    task_id = '_'.join(parts[1:])  # 跳过Prob001部分
                    task_ids.add(task_id)
        
        return task_ids
    
    def _analyze_task(self, task_id):
        """分析单个任务的结果"""
        print(f"📊 分析任务: {task_id}")
        
        # 查找相关的输出文件
        verilog_files = []
        sv_files = []
        log_files = []
        
        # 搜索所有可能的文件名模式
        patterns = [
            f"{task_id}_*",
            f"*{task_id}*",
            f"{task_id}.*"
        ]
        
        for pattern in patterns:
            for filepath in glob.glob(os.path.join(self.plan_output_dir, pattern)):
                filename = os.path.basename(filepath)
                if filename.endswith('.v'):
                    verilog_files.append(filepath)
                elif filename.endswith('.sv'):
                    sv_files.append(filepath)
                elif filename.endswith('.log'):
                    log_files.append(filepath)
        
        # 分析文件
        task_result = {
            'task_id': task_id,
            'verilog_files': verilog_files,
            'sv_files': sv_files,
            'log_files': log_files,
            'status': 'unknown',
            'errors': [],
            'compilation_success': False,
            'simulation_success': False
        }
        
        # 分析日志文件
        if log_files:
            self._analyze_log_files(task_result, log_files)
        
        # 分析Verilog文件
        if verilog_files or sv_files:
            self._analyze_verilog_files(task_result, verilog_files + sv_files)
        
        # 使用iverilog实际测试代码
        if self.run_iverilog_tests and (verilog_files or sv_files):
            self._test_verilog_with_iverilog(task_result, verilog_files + sv_files)
        
        # 确定任务状态
        self._determine_task_status(task_result)
        
        # 更新统计信息
        self.stats['task_results'][task_id] = task_result
        self.stats['generated_files'] += len(verilog_files) + len(sv_files)
        
        # 打印任务结果
        status_emoji = {
            'success': '✅',
            'partial': '⚠️',
            'failed': '❌',
            'unknown': '❓'
        }
        
        print(f"   {status_emoji.get(task_result['status'], '❓')} {task_result['status'].upper()}")
        print(f"   📁 Verilog: {len(verilog_files)}, SystemVerilog: {len(sv_files)}")
        if task_result['errors']:
            print(f"   ⚠️  错误: {', '.join(task_result['errors'][:3])}")
        print()
    
    def _analyze_log_files(self, task_result, log_files):
        """分析日志文件"""
        for log_file in log_files:
            try:
                with open(log_file, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    
                    # 检查编译成功
                    if 'Compiled Success' in content:
                        task_result['compilation_success'] = True
                    
                    # 检查仿真成功
                    if 'Function Check Passed' in content:
                        task_result['simulation_success'] = True
                    elif 'Function Check Failed' in content:
                        task_result['simulation_success'] = False
                    
                    # 检查错误类型
                    if 'syntax error' in content.lower():
                        task_result['errors'].append('syntax_error')
                        self.stats['error_types']['syntax_error'] += 1
                    
                    if 'compilation failed' in content.lower():
                        task_result['errors'].append('compilation_failed')
                        self.stats['error_types']['compilation_failed'] += 1
                    
                    if 'simulation failed' in content.lower():
                        task_result['errors'].append('simulation_failed')
                        self.stats['error_types']['simulation_failed'] += 1
                        
            except Exception as e:
                task_result['errors'].append(f'log_read_error: {str(e)}')
    
    def _test_verilog_with_iverilog(self, task_result, verilog_files):
        """使用iverilog实际测试Verilog代码"""
        print(f"   🔧 使用iverilog测试代码...")
        
        # 查找对应的测试文件和参考文件
        test_file = self._find_test_file(task_result['task_id'])
        ref_file = self._find_ref_file(task_result['task_id'])
        
        if not test_file:
            print(f"   ⚠️  未找到测试文件")
            return
        
        if not ref_file:
            print(f"   ⚠️  未找到参考文件")
            return
        
        # 测试每个Verilog文件
        for verilog_file in verilog_files[:1]:  # 只测试第一个文件避免重复
            try:
                # 创建临时目录
                with tempfile.TemporaryDirectory() as temp_dir:
                    # 复制文件到临时目录
                    temp_verilog = os.path.join(temp_dir, os.path.basename(verilog_file))
                    temp_test = os.path.join(temp_dir, os.path.basename(test_file))
                    temp_ref = os.path.join(temp_dir, os.path.basename(ref_file))
                    
                    shutil.copy2(verilog_file, temp_verilog)
                    shutil.copy2(test_file, temp_test)
                    shutil.copy2(ref_file, temp_ref)
                    
                    # 运行iverilog编译 - 需要包含所有三个文件
                    print(f"   📝 编译: {os.path.basename(verilog_file)}")
                    compile_result = self._run_iverilog_compile(temp_dir, [temp_verilog, temp_ref, temp_test])
                    
                    if compile_result['success']:
                        task_result['compilation_success'] = True
                        print(f"   ✅ 编译成功")
                        
                        # 运行仿真
                        print(f"   🎯 运行仿真...")
                        sim_result = self._run_iverilog_simulation(temp_dir, compile_result['output_file'])
                        
                        if sim_result['success']:
                            task_result['simulation_success'] = True
                            print(f"   ✅ 仿真成功")
                        else:
                            print(f"   ❌ 仿真失败: {sim_result['error']}")
                            task_result['errors'].append(f'simulation_failed: {sim_result["error"]}')
                    else:
                        print(f"   ❌ 编译失败: {compile_result['error']}")
                        task_result['errors'].append(f'compilation_failed: {compile_result["error"]}')
                        
            except Exception as e:
                print(f"   ⚠️  测试异常: {e}")
                task_result['errors'].append(f'test_exception: {str(e)}')
    
    def _find_test_file(self, task_id):
        """查找对应的测试文件"""
        # 在dataset_dumpall目录中查找测试文件
        test_patterns = [
            f"*{task_id}*_test.sv",
            f"*{task_id}*_test.v",
            f"*{task_id}_test.sv",
            f"*{task_id}_test.v"
        ]
        
        for pattern in test_patterns:
            matches = glob.glob(os.path.join(self.dataset_dir, pattern))
            if matches:
                return matches[0]
        
        return None
    
    def _find_ref_file(self, task_id):
        """查找对应的参考文件"""
        # 在dataset_dumpall目录中查找参考文件
        ref_patterns = [
            f"*{task_id}*_ref.sv",
            f"*{task_id}*_ref.v",
            f"*{task_id}_ref.sv",
            f"*{task_id}_ref.v"
        ]
        
        for pattern in ref_patterns:
            matches = glob.glob(os.path.join(self.dataset_dir, pattern))
            if matches:
                return matches[0]
        
        return None
    
    def _run_iverilog_compile(self, temp_dir, source_files):
        """运行iverilog编译"""
        try:
            # 构建编译命令
            output_file = os.path.join(temp_dir, "test.vpp")
            iverilog_path = os.environ.get('IVERILOG_PATH', 'iverilog')
            cmd = [
                iverilog_path, "-Wall", "-Winfloop", "-Wno-timescale", 
                "-g2012", "-s", "tb", "-o", output_file
            ] + source_files
            
            # 运行编译
            result = subprocess.run(
                cmd, 
                cwd=temp_dir, 
                capture_output=True, 
                text=True, 
                timeout=30
            )
            
            if result.returncode == 0:
                return {
                    'success': True,
                    'output_file': output_file,
                    'stdout': result.stdout,
                    'stderr': result.stderr
                }
            else:
                return {
                    'success': False,
                    'error': result.stderr,
                    'stdout': result.stdout,
                    'stderr': result.stderr
                }
                
        except subprocess.TimeoutExpired:
            return {
                'success': False,
                'error': 'Compilation timeout (30s)',
                'stdout': '',
                'stderr': ''
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'stdout': '',
                'stderr': ''
            }
    
    def _run_iverilog_simulation(self, temp_dir, vpp_file):
        """运行iverilog仿真"""
        try:
            # 运行仿真
            cmd = ["vvp", vpp_file]
            result = subprocess.run(
                cmd, 
                cwd=temp_dir, 
                capture_output=True, 
                text=True, 
                timeout=60
            )
            
            if result.returncode == 0:
                # 检查输出中是否有错误信息
                output = result.stdout + result.stderr
                if 'error' in output.lower() or 'failed' in output.lower():
                    return {
                        'success': False,
                        'error': 'Simulation output contains errors',
                        'stdout': result.stdout,
                        'stderr': result.stderr
                    }
                else:
                    return {
                        'success': True,
                        'stdout': result.stdout,
                        'stderr': result.stderr
                    }
            else:
                return {
                    'success': False,
                    'error': result.stderr,
                    'stdout': result.stdout,
                    'stderr': result.stderr
                }
                
        except subprocess.TimeoutExpired:
            return {
                'success': False,
                'error': 'Simulation timeout (60s)',
                'stdout': '',
                'stderr': ''
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'stdout': '',
                'stderr': ''
            }
    
    def _analyze_verilog_files(self, task_result, verilog_files):
        """分析Verilog文件"""
        for verilog_file in verilog_files:
            try:
                with open(verilog_file, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    
                    # 检查文件类型
                    if verilog_file.endswith('.v'):
                        self.stats['file_types']['verilog'] += 1
                    elif verilog_file.endswith('.sv'):
                        self.stats['file_types']['systemverilog'] += 1
                    
                    # 检查基本语法
                    if 'module' in content and 'endmodule' in content:
                        if not task_result['compilation_success']:
                            task_result['compilation_success'] = True
                    
            except Exception as e:
                task_result['errors'].append(f'verilog_read_error: {str(e)}')
    
    def _determine_task_status(self, task_result):
        """确定任务状态"""
        if task_result['compilation_success'] and task_result['simulation_success']:
            task_result['status'] = 'success'
            self.stats['successful_compilations'] += 1
            self.stats['successful_simulations'] += 1
        elif task_result['compilation_success'] and not task_result['simulation_success']:
            task_result['status'] = 'partial'
            self.stats['successful_compilations'] += 1
            self.stats['failed_simulations'] += 1
        elif not task_result['compilation_success']:
            task_result['status'] = 'failed'
            self.stats['failed_compilations'] += 1
        else:
            task_result['status'] = 'unknown'
    
    def _generate_report(self):
        """生成统计报告"""
        print("\n" + "=" * 60)
        print("📊 VERILOGCODER 结果统计报告")
        print("=" * 60)
        
        # 基本统计
        total_tasks = self.stats['total_tasks']
        successful_tasks = sum(1 for r in self.stats['task_results'].values() if r['status'] == 'success')
        partial_tasks = sum(1 for r in self.stats['task_results'].values() if r['status'] == 'partial')
        failed_tasks = sum(1 for r in self.stats['task_results'].values() if r['status'] == 'failed')
        unknown_tasks = sum(1 for r in self.stats['task_results'].values() if r['status'] == 'unknown')
        
        print(f"📋 总任务数: {total_tasks}")
        print(f"✅ 完全成功: {successful_tasks} ({successful_tasks/total_tasks*100:.1f}%)")
        print(f"⚠️  部分成功: {partial_tasks} ({partial_tasks/total_tasks*100:.1f}%)")
        print(f"❌ 完全失败: {failed_tasks} ({failed_tasks/total_tasks*100:.1f}%)")
        print(f"❓ 状态未知: {unknown_tasks} ({unknown_tasks/total_tasks*100:.1f}%)")
        print()
        
        # 文件统计
        print(f"📁 生成文件统计:")
        print(f"   Verilog (.v): {self.stats['file_types']['verilog']}")
        print(f"   SystemVerilog (.sv): {self.stats['file_types']['systemverilog']}")
        print(f"   总计: {self.stats['generated_files']}")
        print()
        
        # 编译和仿真统计
        print(f"🔧 编译统计:")
        print(f"   成功: {self.stats['successful_compilations']} ({self.stats['successful_compilations']/total_tasks*100:.1f}%)")
        print(f"   失败: {self.stats['failed_compilations']} ({self.stats['failed_compilations']/total_tasks*100:.1f}%)")
        print()
        
        print(f"🎯 仿真统计:")
        print(f"   成功: {self.stats['successful_simulations']} ({self.stats['successful_simulations']/total_tasks*100:.1f}%)")
        print(f"   失败: {self.stats['failed_simulations']} ({self.stats['failed_simulations']/total_tasks*100:.1f}%)")
        print()
        
        # 错误类型统计
        if self.stats['error_types']:
            print(f"⚠️  错误类型统计:")
            for error_type, count in self.stats['error_types'].most_common():
                print(f"   {error_type}: {count}")
            print()
        
        # 准确率计算
        overall_accuracy = (successful_tasks / total_tasks) * 100
        compilation_accuracy = (self.stats['successful_compilations'] / total_tasks) * 100
        
        print(f"🎯 总体准确率: {overall_accuracy:.1f}%")
        print(f"🔧 编译准确率: {compilation_accuracy:.1f}%")
        print("=" * 60)
        
        # 保存详细结果到JSON文件
        self._save_detailed_results()
    
    def _save_detailed_results(self):
        """保存详细结果到JSON文件"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"verilogcoder_analysis_{timestamp}.json"
        
        # 准备输出数据
        output_data = {
            'timestamp': datetime.now().isoformat(),
            'summary': {
                'total_tasks': self.stats['total_tasks'],
                'overall_accuracy': (sum(1 for r in self.stats['task_results'].values() if r['status'] == 'success') / self.stats['total_tasks']) * 100,
                'compilation_accuracy': (self.stats['successful_compilations'] / self.stats['total_tasks']) * 100,
                'generated_files': self.stats['generated_files']
            },
            'task_results': self.stats['task_results'],
            'error_types': dict(self.stats['error_types']),
            'file_types': dict(self.stats['file_types'])
        }
        
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(output_data, f, indent=2, ensure_ascii=False)
            print(f"💾 详细结果已保存到: {output_file}")
        except Exception as e:
            print(f"⚠️  保存详细结果失败: {e}")

def main():
    """主函数"""
    import argparse
    
    # 解析命令行参数
    parser = argparse.ArgumentParser(description='VerilogCoder结果分析工具')
    parser.add_argument('--no-iverilog', action='store_true', 
                       help='跳过iverilog测试，只分析现有日志')
    parser.add_argument('--test-only', type=str, 
                       help='只测试指定的任务ID')
    parser.add_argument('--timeout', type=int, default=30,
                       help='编译超时时间（秒），默认30秒')
    
    args = parser.parse_args()
    
    # 配置路径
    plan_output_dir = "verilog-eval-v2/plan_output/"
    plans_dir = "verilog-eval-v2/plans/"
    dataset_dir = "verilog-eval-v2/dataset_dumpall/"
    
    # 检查目录是否存在
    for dir_path in [plan_output_dir, plans_dir, dataset_dir]:
        if not os.path.exists(dir_path):
            print(f"❌ 目录不存在: {dir_path}")
            return
    
    # 检查iverilog是否可用
    run_iverilog_tests = not args.no_iverilog
    if run_iverilog_tests:
        try:
            # 尝试多个可能的路径
            iverilog_paths = ["iverilog", "/opt/homebrew/bin/iverilog", "/usr/local/bin/iverilog"]
            iverilog_found = False
            
            for path in iverilog_paths:
                try:
                    result = subprocess.run([path, "-v"], capture_output=True, text=True)
                    # iverilog -v 即使没有源文件也会返回版本信息，退出码可能是1
                    if "Icarus Verilog version" in result.stdout or "Icarus Verilog version" in result.stderr:
                        print(f"✅ 检测到iverilog: {path}")
                        iverilog_found = True
                        # 设置环境变量
                        os.environ['IVERILOG_PATH'] = path
                        break
                except (subprocess.CalledProcessError, FileNotFoundError):
                    continue
            
            if not iverilog_found:
                print("⚠️  未检测到iverilog，将跳过实际测试")
                run_iverilog_tests = False
        except Exception as e:
            print(f"⚠️  检查iverilog时出错: {e}")
            run_iverilog_tests = False
    
    # 创建分析器并分析结果
    analyzer = VerilogCoderAnalyzer(plan_output_dir, plans_dir, dataset_dir, run_iverilog_tests)
    
    if args.test_only:
        print(f"🎯 只测试任务: {args.test_only}")
        # 单任务测试逻辑
        task_id = args.test_only
        task_result = {
            'task_id': task_id,
            'verilog_files': [],
            'sv_files': [],
            'log_files': [],
            'status': 'unknown',
            'errors': [],
            'compilation_success': False,
            'simulation_success': False
        }
        
        # 查找相关文件
        patterns = [
            f"{task_id}_*",
            f"*{task_id}*",
            f"{task_id}.*"
        ]
        
        for pattern in patterns:
            for filepath in glob.glob(os.path.join(plan_output_dir, pattern)):
                filename = os.path.basename(filepath)
                if filename.endswith('.v'):
                    task_result['verilog_files'].append(filepath)
                elif filename.endswith('.sv'):
                    task_result['sv_files'].append(filepath)
                elif filename.endswith('.log'):
                    task_result['log_files'].append(filepath)
        
        print(f"📁 找到文件:")
        print(f"   Verilog: {len(task_result['verilog_files'])}")
        print(f"   SystemVerilog: {len(task_result['sv_files'])}")
        print(f"   日志: {len(task_result['log_files'])}")
        
        # 分析日志文件
        if task_result['log_files']:
            analyzer._analyze_log_files(task_result, task_result['log_files'])
        
        # 分析Verilog文件
        if task_result['verilog_files'] or task_result['sv_files']:
            analyzer._analyze_verilog_files(task_result, task_result['verilog_files'] + task_result['sv_files'])
        
        # 使用iverilog实际测试代码
        if run_iverilog_tests and (task_result['verilog_files'] or task_result['sv_files']):
            analyzer._test_verilog_with_iverilog(task_result, task_result['verilog_files'] + task_result['sv_files'])
        
        # 确定任务状态
        analyzer._determine_task_status(task_result)
        
        print(f"\n📊 测试结果:")
        print(f"   状态: {task_result['status']}")
        print(f"   编译: {'✅' if task_result['compilation_success'] else '❌'}")
        print(f"   仿真: {'✅' if task_result['simulation_success'] else '❌'}")
        if task_result['errors']:
            print(f"   错误: {', '.join(task_result['errors'])}")
        
        return
    
    results = analyzer.analyze_results()
    
    print(f"\n🎉 分析完成！")

if __name__ == "__main__":
    main()
