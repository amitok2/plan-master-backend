#!/usr/bin/env python3
"""
Test script to verify Gemini 3 Pro Preview integration
"""
import os
import sys
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()

def test_basic_connection():
    """Test basic Gemini API connection"""
    print("=" * 60)
    print("TEST 1: Basic Gemini API Connection")
    print("=" * 60)
    
    api_key = os.environ.get("GEMINI_API_KEY")
    
    if not api_key:
        print("❌ GEMINI_API_KEY not found in environment")
        print("Please set it in .env file or environment variables")
        return False
    
    print(f"✅ API Key found (starts with: {api_key[:10]}...)")
    
    try:
        genai.configure(api_key=api_key)
        print("✅ Gemini API configured successfully")
        return True
    except Exception as e:
        print(f"❌ Failed to configure Gemini API: {e}")
        return False

def test_gemini_3_low_thinking():
    """Test Gemini 3 Pro with low thinking level"""
    print("\n" + "=" * 60)
    print("TEST 2: Gemini 3 Pro Preview - Without thinking_level (default)")
    print("=" * 60)
    
    try:
        # Try without thinking_level parameter first
        model = genai.GenerativeModel(
            'gemini-3-pro-preview',
            generation_config={
                "temperature": 1.0
            }
        )
        print("✅ Model initialized: gemini-3-pro-preview (default config)")
        
        prompt = "What is 2 + 2? Answer in one sentence."
        print(f"\nPrompt: {prompt}")
        print("Generating response...")
        
        response = model.generate_content(prompt)
        
        print("\n✅ Response received:")
        print("-" * 60)
        print(response.text)
        print("-" * 60)
        return True
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nPossible causes:")
        print("1. You don't have access to gemini-3-pro-preview yet")
        print("2. The SDK version is outdated")
        print("3. API key doesn't have proper permissions")
        return False

def test_gemini_3_high_thinking():
    """Test Gemini 3 Pro with complex reasoning"""
    print("\n" + "=" * 60)
    print("TEST 3: Gemini 3 Pro Preview - Complex Reasoning Task")
    print("=" * 60)
    
    try:
        model = genai.GenerativeModel(
            'gemini-3-pro-preview',
            generation_config={
                "temperature": 1.0
            }
        )
        print("✅ Model initialized: gemini-3-pro-preview (default config)")
        
        prompt = "Analyze the trade-offs between using a monolithic vs microservices architecture. Be concise."
        print(f"\nPrompt: {prompt}")
        print("Generating response...")
        
        response = model.generate_content(prompt)
        
        print("\n✅ Response received:")
        print("-" * 60)
        print(response.text)
        print("-" * 60)
        return True
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return False

def test_clarify_endpoint_simulation():
    """Simulate the /plan/clarify endpoint logic"""
    print("\n" + "=" * 60)
    print("TEST 4: Simulating /plan/clarify Endpoint")
    print("=" * 60)
    
    try:
        api_key = os.environ.get("GEMINI_API_KEY")
        genai.configure(api_key=api_key)
        
        model = genai.GenerativeModel(
            'gemini-3-pro-preview',
            generation_config={
                "temperature": 1.0
            }
        )
        print("✅ Model initialized for clarification")
        
        # Simulate a feature request
        feature_request = "Add user authentication to my app"
        codebase_context = "Simple Flask app with 2 routes: / and /api/data"
        
        system_prompt = """You are a Senior Product Manager. Analyze the feature request and ask 2-3 clarifying questions.
        Keep it brief for this test."""
        
        prompt = f"{system_prompt}\n\nFeature Request: {feature_request}\n\nCodebase Context:\n{codebase_context}"
        
        print(f"\nFeature Request: {feature_request}")
        print(f"Codebase: {codebase_context}")
        print("\nGenerating clarifying questions...")
        
        response = model.generate_content(prompt)
        
        print("\n✅ Clarifying Questions Generated:")
        print("-" * 60)
        print(response.text)
        print("-" * 60)
        
        needs_clarification = "No clarification needed" not in response.text
        print(f"\nNeeds Clarification: {needs_clarification}")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return False

def main():
    print("\n🚀 GEMINI 3 PRO PREVIEW INTEGRATION TEST")
    print("=" * 60)
    
    results = []
    
    # Run tests
    results.append(("Basic Connection", test_basic_connection()))
    
    if results[0][1]:  # Only continue if connection works
        results.append(("Simple Query Test", test_gemini_3_low_thinking()))
        results.append(("Complex Reasoning Test", test_gemini_3_high_thinking()))
        results.append(("Clarify Endpoint Simulation", test_clarify_endpoint_simulation()))
    
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
        print("\n🎉 All tests passed! Gemini 3 Pro Preview is working correctly.")
        return 0
    else:
        print("\n⚠️  Some tests failed. Check the error messages above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())

