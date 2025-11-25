#!/usr/bin/env python3
"""
Comprehensive test for all AI providers: Gemini, Claude, and GPT
"""
import os
import sys
import time
from dotenv import load_dotenv
from google import genai
from google.genai import types
import anthropic
from openai import OpenAI

# Load environment variables
load_dotenv()

def test_gemini():
    """Test Gemini 2.5 Pro"""
    print("\n" + "=" * 60)
    print("TEST 1: Gemini 2.5 Pro")
    print("=" * 60)
    
    try:
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            print("⚠️  GEMINI_API_KEY not configured - SKIPPING")
            return None
            
        client = genai.Client(api_key=api_key)
        
        prompt = "What is 3 + 4? Answer in one sentence."
        print(f"Prompt: {prompt}")
        print("Generating response...")
        
        start = time.time()
        response = client.models.generate_content(
            model="gemini-2.5-pro",
            contents=prompt,
        )
        duration = time.time() - start
        
        print(f"\n✅ Response received in {duration:.2f}s:")
        print("-" * 60)
        print(response.text)
        print("-" * 60)
        return True
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return False

def test_claude():
    """Test Claude 4.5 Sonnet"""
    print("\n" + "=" * 60)
    print("TEST 2: Claude 4.5 Sonnet")
    print("=" * 60)
    
    try:
        api_key = os.environ.get("ANTHROPIC_API_KEY")
        if not api_key:
            print("⚠️  ANTHROPIC_API_KEY not configured - SKIPPING")
            return None
            
        client = anthropic.Anthropic(api_key=api_key)
        
        prompt = "What is 5 + 6? Answer in one sentence."
        print(f"Prompt: {prompt}")
        print("Generating response...")
        
        start = time.time()
        message = client.messages.create(
            model="claude-sonnet-4-5",
            max_tokens=1024,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )
        duration = time.time() - start
        
        print(f"\n✅ Response received in {duration:.2f}s:")
        print("-" * 60)
        print(message.content[0].text)
        print("-" * 60)
        return True
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return False

def test_gpt():
    """Test GPT-5.1"""
    print("\n" + "=" * 60)
    print("TEST 3: GPT-5.1")
    print("=" * 60)
    
    try:
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            print("⚠️  OPENAI_API_KEY not configured - SKIPPING")
            return None
            
        client = OpenAI(api_key=api_key)
        
        prompt = "What is 7 + 8? Answer in one sentence."
        print(f"Prompt: {prompt}")
        print("Generating response...")
        
        start = time.time()
        result = client.responses.create(
            model="gpt-5.1",
            input=prompt,
            reasoning={"effort": "low"},
            text={"verbosity": "medium"}
        )
        duration = time.time() - start
        
        print(f"\n✅ Response received in {duration:.2f}s:")
        print("-" * 60)
        print(result.output_text)
        print("-" * 60)
        return True
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return False

def test_clarification_task():
    """Test clarification with Claude (best for reasoning)"""
    print("\n" + "=" * 60)
    print("TEST 4: Clarification Task (Claude 4.5)")
    print("=" * 60)
    
    try:
        api_key = os.environ.get("ANTHROPIC_API_KEY")
        if not api_key:
            print("⚠️  ANTHROPIC_API_KEY not configured - SKIPPING")
            return None
            
        client = anthropic.Anthropic(api_key=api_key)
        
        prompt = """You are a Senior Product Manager. Analyze this feature request and ask 2-3 clarifying questions.

Feature Request: Add user authentication to my app
Codebase: Simple Flask app with 2 routes: / and /api/data

Keep it brief for this test."""
        
        print("Generating clarifying questions...")
        
        start = time.time()
        message = client.messages.create(
            model="claude-sonnet-4-5",
            max_tokens=2048,
            messages=[{"role": "user", "content": prompt}]
        )
        duration = time.time() - start
        
        print(f"\n✅ Response received in {duration:.2f}s:")
        print("-" * 60)
        print(message.content[0].text)
        print("-" * 60)
        return True
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return False

def test_prd_generation():
    """Test PRD generation with GPT-5.1"""
    print("\n" + "=" * 60)
    print("TEST 5: PRD Generation (GPT-5.1)")
    print("=" * 60)
    
    try:
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            print("⚠️  OPENAI_API_KEY not configured - SKIPPING")
            return None
            
        client = OpenAI(api_key=api_key)
        
        prompt = """You are a Senior Product Manager. Create a brief PRD (5-7 lines) for:

Feature: Add a dark mode toggle to the settings page
Codebase: React app with 5 components

Include:
1. Overview (1 sentence)
2. Target Users (1 sentence)
3. Key Requirements (2-3 bullet points)"""
        
        print("Generating PRD...")
        
        start = time.time()
        result = client.responses.create(
            model="gpt-5.1",
            input=prompt,
            reasoning={"effort": "medium"},
            text={"verbosity": "medium"}
        )
        duration = time.time() - start
        
        print(f"\n✅ Response received in {duration:.2f}s:")
        print("-" * 60)
        print(result.output_text)
        print("-" * 60)
        return True
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return False

def test_blueprint_generation():
    """Test blueprint generation with Claude"""
    print("\n" + "=" * 60)
    print("TEST 6: Blueprint Generation (Claude 4.5)")
    print("=" * 60)
    
    try:
        api_key = os.environ.get("ANTHROPIC_API_KEY")
        if not api_key:
            print("⚠️  ANTHROPIC_API_KEY not configured - SKIPPING")
            return None
            
        client = anthropic.Anthropic(api_key=api_key)
        
        prompt = """You are a Senior Software Architect. Create a brief technical blueprint (5-7 lines) for:

Feature: Add user authentication
Current: Simple Flask app with 2 routes

Include:
1. Files to create (2-3 files)
2. Implementation steps (3 steps)
Keep it concise."""
        
        print("Generating blueprint...")
        
        start = time.time()
        message = client.messages.create(
            model="claude-sonnet-4-5",
            max_tokens=2048,
            messages=[{"role": "user", "content": prompt}]
        )
        duration = time.time() - start
        
        print(f"\n✅ Response received in {duration:.2f}s:")
        print("-" * 60)
        print(message.content[0].text)
        print("-" * 60)
        return True
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return False

def main():
    print("\n🚀 MULTI-PROVIDER AI TEST SUITE")
    print("=" * 60)
    print("Testing: Gemini 2.5 Pro, Claude 4.5 Sonnet, GPT-5.1")
    print("=" * 60)
    
    results = []
    
    # Basic tests for each provider
    results.append(("Gemini 2.5 Pro", test_gemini()))
    results.append(("Claude 4.5 Sonnet", test_claude()))
    results.append(("GPT-5.1", test_gpt()))
    
    # Task-specific tests
    results.append(("Clarification (Claude)", test_clarification_task()))
    results.append(("PRD Generation (GPT)", test_prd_generation()))
    results.append(("Blueprint (Claude)", test_blueprint_generation()))
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    for test_name, passed in results:
        if passed is None:
            status = "⚠️  SKIPPED (API key not configured)"
        elif passed:
            status = "✅ PASSED"
        else:
            status = "❌ FAILED"
        print(f"{test_name}: {status}")
    
    # Count results (excluding skipped)
    actual_tests = [r for r in results if r[1] is not None]
    if not actual_tests:
        print("\n⚠️  No API keys configured. Please set at least one:")
        print("   - GEMINI_API_KEY")
        print("   - ANTHROPIC_API_KEY")
        print("   - OPENAI_API_KEY")
        return 1
    
    total = len(actual_tests)
    passed = sum(1 for _, p in actual_tests if p)
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All configured providers working correctly!")
        print("\n📊 Provider Status:")
        if os.environ.get("GEMINI_API_KEY"):
            print("   ✅ Gemini 2.5 Pro - Operational")
        if os.environ.get("ANTHROPIC_API_KEY"):
            print("   ✅ Claude 4.5 Sonnet - Operational")
        if os.environ.get("OPENAI_API_KEY"):
            print("   ✅ GPT-5.1 - Operational")
        return 0
    else:
        print("\n⚠️  Some tests failed. Check the error messages above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())

