#!/usr/bin/env python3
"""
Quick test for Gemini 2.5 Pro
"""
import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

# Load environment variables
load_dotenv()

def test_gemini_25_basic():
    """Test Gemini 2.5 Pro basic functionality"""
    print("=" * 60)
    print("TEST 1: Gemini 2.5 Pro - Basic Query")
    print("=" * 60)
    
    try:
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            print("❌ GEMINI_API_KEY not found")
            return False
            
        client = genai.Client(api_key=api_key)
        
        prompt = "What is 5 + 7? Answer in one sentence."
        print(f"\nPrompt: {prompt}")
        print("Generating response...")
        
        response = client.models.generate_content(
            model="gemini-2.5-pro",
            contents=prompt,
        )
        
        print("\n✅ Response received:")
        print("-" * 60)
        print(response.text)
        print("-" * 60)
        return True
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return False

def test_gemini_25_prd_simulation():
    """Test Gemini 2.5 Pro for PRD generation (simulated)"""
    print("\n" + "=" * 60)
    print("TEST 2: Gemini 2.5 Pro - PRD Generation Simulation")
    print("=" * 60)
    
    try:
        api_key = os.environ.get("GEMINI_API_KEY")
        client = genai.Client(api_key=api_key)
        
        system_prompt = """You are a Senior Product Manager. Create a brief PRD (5-7 lines) for the following feature.
        
        Include:
        1. Overview (1 sentence)
        2. Target Users (1 sentence)
        3. Key Requirements (2-3 bullet points)
        """
        
        feature = "Add a dark mode toggle to the settings page"
        codebase = "React app with 5 components, using Context API for state"
        
        prompt = f"{system_prompt}\n\nFeature: {feature}\n\nCodebase: {codebase}"
        
        print(f"\nFeature Request: {feature}")
        print(f"Codebase: {codebase}")
        print("\nGenerating PRD...")
        
        response = client.models.generate_content(
            model="gemini-2.5-pro",
            contents=prompt,
        )
        
        print("\n✅ PRD Generated:")
        print("-" * 60)
        print(response.text)
        print("-" * 60)
        return True
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return False

def test_gemini_25_tasks_simulation():
    """Test Gemini 2.5 Pro for task breakdown"""
    print("\n" + "=" * 60)
    print("TEST 3: Gemini 2.5 Pro - Task Breakdown")
    print("=" * 60)
    
    try:
        api_key = os.environ.get("GEMINI_API_KEY")
        client = genai.Client(api_key=api_key)
        
        system_prompt = """You are a Technical Lead. Break down this feature into 4-5 actionable tasks.
        Format as a numbered list with brief descriptions."""
        
        blueprint = """
        Feature: Add user authentication
        Files to create:
        - src/auth/login.js
        - src/auth/register.js
        - src/components/LoginForm.jsx
        """
        
        prompt = f"{system_prompt}\n\nBlueprint:\n{blueprint}"
        
        print("Generating task breakdown...")
        
        response = client.models.generate_content(
            model="gemini-2.5-pro",
            contents=prompt,
        )
        
        print("\n✅ Tasks Generated:")
        print("-" * 60)
        print(response.text)
        print("-" * 60)
        return True
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return False

def test_gemini_25_speed():
    """Test Gemini 2.5 Pro response speed"""
    print("\n" + "=" * 60)
    print("TEST 4: Gemini 2.5 Pro - Speed Test")
    print("=" * 60)
    
    try:
        import time
        
        api_key = os.environ.get("GEMINI_API_KEY")
        client = genai.Client(api_key=api_key)
        
        prompt = "List 3 benefits of using TypeScript. Be concise."
        
        print(f"\nPrompt: {prompt}")
        print("Measuring response time...")
        
        start_time = time.time()
        
        response = client.models.generate_content(
            model="gemini-2.5-pro",
            contents=prompt,
        )
        
        end_time = time.time()
        duration = end_time - start_time
        
        print(f"\n✅ Response received in {duration:.2f} seconds")
        print("-" * 60)
        print(response.text)
        print("-" * 60)
        
        if duration < 10:
            print(f"✅ Speed: GOOD ({duration:.2f}s)")
        else:
            print(f"⚠️  Speed: SLOW ({duration:.2f}s)")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return False

def main():
    print("\n🚀 GEMINI 2.5 PRO QUICK TEST")
    print("=" * 60)
    
    results = []
    
    # Run tests
    results.append(("Basic Query", test_gemini_25_basic()))
    results.append(("PRD Generation", test_gemini_25_prd_simulation()))
    results.append(("Task Breakdown", test_gemini_25_tasks_simulation()))
    results.append(("Speed Test", test_gemini_25_speed()))
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    for test_name, passed in results:
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"{test_name}: {status}")
    
    total = len(results)
    passed = sum(1 for _, p in results if p)
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! Gemini 2.5 Pro is working correctly.")
        print("\n📊 Summary:")
        print("   - Model: gemini-2.5-pro")
        print("   - Status: ✅ Operational")
        print("   - Use Case: Default model for most tasks")
        print("   - Performance: Good balance of speed and quality")
        return 0
    else:
        print("\n⚠️  Some tests failed. Check the error messages above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())


