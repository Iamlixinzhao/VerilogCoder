#!/usr/bin/env python3
"""
启动vLLM本地服务脚本
用于在本地测试VerilogCoder项目
"""

import subprocess
import sys
import time
import requests
import json
from pathlib import Path

def check_vllm_installation():
    """检查vLLM是否已安装"""
    try:
        subprocess.run(["vllm", "--help"], capture_output=True, check=True)
        print("✅ vLLM已安装")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ vLLM未安装")
        print("请先安装vLLM: pip install vllm")
        return False

def start_vllm_service(model_name="microsoft/DialoGPT-medium", port=8000):
    """启动vLLM服务"""
    print(f"🚀 启动vLLM服务...")
    print(f"   模型: {model_name}")
    print(f"   端口: {port}")
    print(f"   API端点: http://localhost:{port}/v1")
    
    # 构建vLLM启动命令
    cmd = [
        "vllm", "serve", model_name,
        "--host", "0.0.0.0",
        "--port", str(port),
        "--openai-compatible"
    ]
    
    try:
        print(f"📝 执行命令: {' '.join(cmd)}")
        print("⏳ 启动中，请等待...")
        
        # 启动vLLM服务
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # 等待服务启动
        print("🔄 等待服务启动...")
        time.sleep(10)
        
        # 检查服务是否启动成功
        if check_service_health(port):
            print("✅ vLLM服务启动成功！")
            print(f"🌐 服务地址: http://localhost:{port}")
            print(f"📚 API文档: http://localhost:{port}/docs")
            print("\n💡 现在你可以:")
            print("   1. 修改OAI_CONFIG_LIST为VLLM_CONFIG_LIST")
            print("   2. 运行VerilogCoder项目")
            print("   3. 按Ctrl+C停止服务")
            
            # 保持服务运行
            try:
                process.wait()
            except KeyboardInterrupt:
                print("\n🛑 收到停止信号，正在关闭服务...")
                process.terminate()
                process.wait()
                print("✅ 服务已关闭")
        else:
            print("❌ 服务启动失败")
            process.terminate()
            return False
            
    except Exception as e:
        print(f"❌ 启动服务时出错: {e}")
        return False
    
    return True

def check_service_health(port):
    """检查服务健康状态"""
    try:
        response = requests.get(f"http://localhost:{port}/health", timeout=5)
        return response.status_code == 200
    except:
        return False

def test_openai_compatibility(port):
    """测试OpenAI兼容性"""
    try:
        # 测试聊天完成API
        url = f"http://localhost:{port}/v1/chat/completions"
        headers = {"Content-Type": "application/json"}
        data = {
            "model": "microsoft/DialoGPT-medium",
            "messages": [{"role": "user", "content": "Hello!"}],
            "max_tokens": 50
        }
        
        response = requests.post(url, headers=headers, json=data, timeout=10)
        if response.status_code == 200:
            print("✅ OpenAI兼容性测试通过")
            return True
        else:
            print(f"❌ OpenAI兼容性测试失败: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ OpenAI兼容性测试出错: {e}")
        return False

def main():
    """主函数"""
    print("🔧 vLLM本地服务启动器")
    print("=" * 50)
    
    # 检查vLLM安装
    if not check_vllm_installation():
        sys.exit(1)
    
    # 配置参数
    model_name = "microsoft/DialoGPT-medium"  # 使用较小的模型进行测试
    port = 8000
    
    print(f"\n📋 配置信息:")
    print(f"   模型: {model_name}")
    print(f"   端口: {port}")
    print(f"   用途: 本地测试VerilogCoder项目")
    
    # 启动服务
    if start_vllm_service(model_name, port):
        print("\n🎉 服务启动完成！")
    else:
        print("\n❌ 服务启动失败")
        sys.exit(1)

if __name__ == "__main__":
    main()
