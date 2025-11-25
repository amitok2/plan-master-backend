#!/usr/bin/env python3
"""
Test script to verify Gemini 3 Pro Preview integration with NEW SDK
"""
import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

# Load environment variables
load_dotenv()

def test_basic_connection():
    """Test basic Gemini API connection"""
    print("=" * 60)
    print("TEST 1: Basic Gemini API Connection (New SDK)")
    print("=" * 60)
    
    api_key = os.environ.get("GEMINI_API_KEY")
    
    if not api_key:
        print("❌ GEMINI_API_KEY not found in environment")
        print("Please set it in .env file or environment variables")
        return False
    
    print(f"✅ API Key found (starts with: {api_key[:10]}...)")
    
    try:
        client = genai.Client(api_key=api_key)
        print("✅ Gemini Client initialized successfully")
        return True
    except Exception as e:
        print(f"❌ Failed to initialize Gemini Client: {e}")
        return False

def test_gemini_3_simple():
    """Test Gemini 3 Pro with simple query"""
    print("\n" + "=" * 60)
    print("TEST 2: Gemini 3 Pro Preview - Simple Query")
    print("=" * 60)
    
    try:
        api_key = os.environ.get("GEMINI_API_KEY")
        client = genai.Client(api_key=api_key)
        
        print("✅ Client initialized for gemini-3-pro-preview")
        
        prompt = "What is 2 + 2? Answer in one sentence."
        print(f"\nPrompt: {prompt}")
        print("Generating response...")
        
        response = client.models.generate_content(
            model="gemini-3-pro-preview",
            contents=prompt,
        )
        
        print("\n✅ Response received:")
        print("-" * 60)
        print(response.text)
        print("-" * 60)
        return True
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nPossible causes:")
        print("1. You don't have access to gemini-3-pro-preview yet")
        print("2. The SDK version is outdated (need google-genai >= 1.0.0)")
        print("3. API key doesn't have proper permissions")
        return False

def test_gemini_3_complex():
    """Test Gemini 3 Pro with complex reasoning"""
    print("\n" + "=" * 60)
    print("TEST 3: Gemini 3 Pro Preview - Complex Reasoning")
    print("=" * 60)
    
    try:
        api_key = os.environ.get("GEMINI_API_KEY")
        client = genai.Client(api_key=api_key)
        
        print("✅ Client initialized for gemini-3-pro-preview")
        
        prompt = "Analyze the trade-offs between using a monolithic vs microservices architecture. Be concise (3-4 sentences)."
        print(f"\nPrompt: {prompt}")
        print("Generating response...")
        
        response = client.models.generate_content(
            model="gemini-3-pro-preview",
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

def test_with_config():
    """Test Gemini 3 Pro with generation config"""
    print("\n" + "=" * 60)
    print("TEST 4: Gemini 3 Pro Preview - With Config")
    print("=" * 60)
    
    try:
        api_key = os.environ.get("GEMINI_API_KEY")
        client = genai.Client(api_key=api_key)
        
        print("✅ Client initialized with config")
        
        prompt = "List 3 benefits of using Python for backend development."
        print(f"\nPrompt: {prompt}")
        print("Generating response with temperature=1.0...")
        
        response = client.models.generate_content(
            model="gemini-3-pro-preview",
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=1.0,
            )
        )
        
        print("\n✅ Response received:")
        print("-" * 60)
        print(response.text)
        print("-" * 60)
        return True
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return False

def test_clarify_simulation():
    """Simulate the /plan/clarify endpoint logic"""
    print("\n" + "=" * 60)
    print("TEST 5: Simulating /plan/clarify Endpoint")
    print("=" * 60)
    
    try:
        api_key = os.environ.get("GEMINI_API_KEY")
        client = genai.Client(api_key=api_key)
        
        print("✅ Client initialized for clarification")
        
        # Simulate a feature request
        feature_request = "Add user authentication to my app"
        codebase_context = "Simple Flask app with 2 routes: / and /api/data"
        
        system_prompt = """You are a Senior Product Manager. Analyze the feature request and ask 2-3 clarifying questions.
        Keep it brief for this test."""
        
        prompt = f"{system_prompt}\n\nFeature Request: {feature_request}\n\nCodebase Context:\n{codebase_context}"
        
        print(f"\nFeature Request: {feature_request}")
        print(f"Codebase: {codebase_context}")
        print("\nGenerating clarifying questions...")
        
        response = client.models.generate_content(
            model="gemini-3-pro-preview",
            contents=prompt,
        )
        
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
    print("\n🚀 GEMINI 3 PRO PREVIEW INTEGRATION TEST (New SDK)")
    print("=" * 60)
    
    results = []
    
    # Run tests
    results.append(("Basic Connection", test_basic_connection()))
    
    if results[0][1]:  # Only continue if connection works
        results.append(("Simple Query Test", test_gemini_3_simple()))
        results.append(("Complex Reasoning Test", test_gemini_3_complex()))
        results.append(("Config Test", test_with_config()))
        results.append(("Clarify Endpoint Simulation", test_clarify_simulation()))
    
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

