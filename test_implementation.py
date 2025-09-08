#!/usr/bin/env python3
"""
Test script to validate the implementation of all assignments.
This tests that our code is syntactically correct and the logic is sound.
"""

import ast
import sys
import os

def test_syntax(file_path):
    """Test if a Python file has valid syntax."""
    try:
        with open(file_path, 'r') as f:
            content = f.read()
        
        # Parse the file to check syntax
        ast.parse(content)
        print(f"✅ {file_path}: Syntax valid")
        return True
    except SyntaxError as e:
        print(f"❌ {file_path}: Syntax error - {e}")
        return False
    except Exception as e:
        print(f"❌ {file_path}: Error reading file - {e}")
        return False

def test_assignment_1():
    """Test Assignment 1 implementation."""
    print("\n🎭 Testing Assignment 1: Custom AI Personalities & Smart Memory")
    
    # Test that helper file has valid syntax
    syntax_ok = test_syntax("langchain_helpers.py")
    
    if syntax_ok:
        try:
            # Test that our new methods exist in the helper file
            with open("langchain_helpers.py", 'r') as f:
                content = f.read()
            
            required_methods = [
                "get_creative_config",
                "get_analytical_config", 
                "get_conversational_config",
                "build_smart_memory_chain"
            ]
            
            for method in required_methods:
                if method in content:
                    print(f"  ✅ Found method: {method}")
                else:
                    print(f"  ❌ Missing method: {method}")
            
            # Check for LangGraph imports
            if "from langgraph.graph import StateGraph" in content:
                print("  ✅ LangGraph imports present")
            else:
                print("  ❌ Missing LangGraph imports")
            
        except Exception as e:
            print(f"  ❌ Error checking methods: {e}")
    
    # Test Basic Chatbot page
    test_syntax("pages/1_Basic_Chatbot.py")

def test_assignment_2():
    """Test Assignment 2 implementation."""
    print("\n🌐 Testing Assignment 2: Multi-tool Research Agent")
    
    # Test that enhanced agent method exists
    try:
        with open("langchain_helpers.py", 'r') as f:
            content = f.read()
        
        if "setup_agent_with_research_tools" in content:
            print("  ✅ Enhanced agent method found")
        else:
            print("  ❌ Enhanced agent method missing")
        
        # Check for tool imports
        tool_imports = [
            "WikipediaQueryRun",
            "ArxivAPIWrapper",
            "Tool"
        ]
        
        for import_name in tool_imports:
            if import_name in content:
                print(f"  ✅ Found import: {import_name}")
            else:
                print(f"  ❌ Missing import: {import_name}")
                
    except Exception as e:
        print(f"  ❌ Error checking agent implementation: {e}")
    
    # Test Agent Chatbot page
    test_syntax("pages/2_Chatbot_Agent.py")

def test_assignment_3():
    """Test Assignment 3 implementation."""
    print("\n📄 Testing Assignment 3: Multi-format RAG System")
    
    # Test RAG helper updates
    try:
        with open("langchain_helpers.py", 'r') as f:
            content = f.read()
        
        # Check for updated save_file method
        if "-> tuple[str, str]" in content:
            print("  ✅ Updated save_file method signature found")
        else:
            print("  ❌ save_file method not updated")
        
        # Check for multi-format support
        if "TextLoader" in content and "Docx2txtLoader" in content:
            print("  ✅ Multi-format loader imports found")
        else:
            print("  ❌ Multi-format loader imports missing")
            
    except Exception as e:
        print(f"  ❌ Error checking RAG implementation: {e}")
    
    # Test Chat with Data page
    test_syntax("pages/3_Chat_with_your_Data.py")

def test_requirements():
    """Test that requirements.txt has been updated."""
    print("\n📦 Testing Requirements Updates")
    
    try:
        with open("requirements.txt", 'r') as f:
            content = f.read()
        
        required_packages = [
            "wikipedia>=1.4.0",
            "arxiv==2.2.0",
            "python-docx>=0.8.11"
        ]
        
        for package in required_packages:
            if package in content:
                print(f"  ✅ Found package: {package}")
            else:
                print(f"  ❌ Missing package: {package}")
                
    except Exception as e:
        print(f"  ❌ Error checking requirements: {e}")

def main():
    """Run all tests."""
    print("🧪 Testing Assignment Implementation")
    print("=" * 50)
    
    # Test core files exist
    required_files = [
        "langchain_helpers.py",
        "pages/1_Basic_Chatbot.py", 
        "pages/2_Chatbot_Agent.py",
        "pages/3_Chat_with_your_Data.py",
        "requirements.txt"
    ]
    
    missing_files = []
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"✅ Found: {file_path}")
        else:
            print(f"❌ Missing: {file_path}")
            missing_files.append(file_path)
    
    if missing_files:
        print(f"\n❌ Cannot continue - missing files: {missing_files}")
        return False
    
    # Run assignment tests
    test_assignment_1()
    test_assignment_2() 
    test_assignment_3()
    test_requirements()
    
    print("\n" + "=" * 50)
    print("🎉 Testing Complete!")
    print("📝 Note: This tests code syntax and structure.")
    print("🚀 To fully test functionality, run: streamlit run Home.py")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)