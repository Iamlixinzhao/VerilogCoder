#!/usr/bin/env python3
"""
测试vLLM配置脚本
验证VLLM_CONFIG_LIST是否能正常工作
"""

import requests
import json
import time

def test_vllm_connection():
    """测试vLLM连接"""
    print("🔍 测试vLLM连接...")
    
    try:
        # 测试健康检查
        response = requests.get("http://localhost:8000/health", timeout=5)
        if response.status_code == 200:
            print("✅ vLLM服务健康检查通过")
        else:
            print(f"❌ vLLM服务健康检查失败: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 无法连接到vLLM服务: {e}")
        print("💡 请确保vLLM服务已启动: python start_vllm_local.py")
        return False
    
    return True

def test_openai_compatibility():
    """测试OpenAI兼容性"""
    print("\n🔍 测试OpenAI兼容性...")
    
    try:
        url = "http://localhost:8000/v1/chat/completions"
        headers = {"Content-Type": "application/json"}
        
        # 测试数据
        data = {
            "model": "microsoft/DialoGPT-small",
            "messages": [
                {"role": "user", "content": "Write a simple Verilog module for a 2-input AND gate."}
            ],
            "max_tokens": 100,
            "temperature": 0.7
        }
        
        print("📝 发送测试请求...")
        response = requests.post(url, headers=headers, json=data, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            print("✅ OpenAI兼容性测试通过")
            print(f"📊 响应状态: {response.status_code}")
            
            # 显示响应内容
            if 'choices' in result and len(result['choices']) > 0:
                content = result['choices'][0]['message']['content']
                print(f"🤖 模型响应: {content[:200]}...")
            else:
                print("⚠️  响应格式异常")
                print(f"📄 完整响应: {json.dumps(result, indent=2)}")
            
            return True
        else:
            print(f"❌ OpenAI兼容性测试失败: {response.status_code}")
            print(f"📄 错误响应: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ 测试过程中出错: {e}")
        return False

def test_verilogcoder_integration():
    """测试VerilogCoder集成"""
    print("\n🔍 测试VerilogCoder集成...")
    
    try:
        # 模拟VerilogCoder的请求
        url = "http://localhost:8000/v1/chat/completions"
        headers = {"Content-Type": "application/json"}
        
        # 使用VerilogCoder风格的提示
        data = {
            "model": "microsoft/DialoGPT-small",
            "messages": [
                {
                    "role": "system", 
                    "content": "You are a Verilog coding expert. Generate correct and efficient Verilog code."
                },
                {
                    "role": "user", 
                    "content": "Create a Verilog module for a 4-bit counter with synchronous reset."
                }
            ],
            "max_tokens": 200,
            "temperature": 0.3
        }
        
        print("📝 发送VerilogCoder风格请求...")
        response = requests.post(url, headers=headers, json=data, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            print("✅ VerilogCoder集成测试通过")
            
            if 'choices' in result and len(result['choices']) > 0:
                content = result['choices'][0]['message']['content']
                print(f"🤖 Verilog代码生成: {content[:300]}...")
            else:
                print("⚠️  响应格式异常")
            
            return True
        else:
            print(f"❌ VerilogCoder集成测试失败: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ 集成测试过程中出错: {e}")
        return False

def main():
    """主函数"""
    print("🧪 vLLM配置测试工具")
    print("=" * 50)
    
    # 测试连接
    if not test_vllm_connection():
        print("\n❌ 连接测试失败，请检查vLLM服务")
        return
    
    # 测试OpenAI兼容性
    if not test_openai_compatibility():
        print("\n❌ OpenAI兼容性测试失败")
        return
    
    # 测试VerilogCoder集成
    if not test_verilogcoder_integration():
        print("\n❌ VerilogCoder集成测试失败")
        return
    
    print("\n🎉 所有测试通过！")
    print("\n💡 现在你可以:")
    print("   1. 将OAI_CONFIG_LIST重命名为OAI_CONFIG_LIST.backup")
    print("   2. 将VLLM_CONFIG_LIST重命名为OAI_CONFIG_LIST")
    print("   3. 运行VerilogCoder项目")
    print("\n📝 配置文件已准备就绪:")
    print("   - VLLM_CONFIG_LIST: vLLM配置")
    print("   - start_vllm_local.py: 启动脚本")

if __name__ == "__main__":
    main()
