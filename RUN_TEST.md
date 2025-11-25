# How to Run Gemini 3 Pro Preview Test

I've created a comprehensive test script to verify the Gemini 3 Pro Preview integration.

## Prerequisites

1. Make sure you have the `.env` file in the `plan-master-backend` directory with:
   ```
   GEMINI_API_KEY=your_actual_api_key_here
   ```

2. Install dependencies:
   ```bash
   cd plan-master-backend
   pip install -r requirements.txt
   ```

## Run the Test

```bash
cd plan-master-backend
python3 test_gemini_integration.py
```

## What the Test Does

The script runs 4 tests:

1. **Basic Connection Test**: Verifies the API key is configured correctly
2. **Low Thinking Level Test**: Tests `gemini-3-pro-preview` with `thinking_level: "low"`
3. **High Thinking Level Test**: Tests `gemini-3-pro-preview` with `thinking_level: "high"`
4. **Clarify Endpoint Simulation**: Simulates the `/plan/clarify` endpoint logic

## Expected Output

If everything is working correctly, you should see:

```
🚀 GEMINI 3 PRO PREVIEW INTEGRATION TEST
============================================================
TEST 1: Basic Gemini API Connection
============================================================
✅ API Key found (starts with: AIzaSy...)
✅ Gemini API configured successfully

============================================================
TEST 2: Gemini 3 Pro Preview - Low Thinking Level
============================================================
✅ Model initialized: gemini-3-pro-preview (thinking_level: low)

Prompt: What is 2 + 2? Answer in one sentence.
Generating response...

✅ Response received:
------------------------------------------------------------
2 + 2 equals 4.
------------------------------------------------------------

... (more tests)

============================================================
TEST SUMMARY
============================================================
Basic Connection: ✅ PASSED
Low Thinking Test: ✅ PASSED
High Thinking Test: ✅ PASSED
Clarify Endpoint Simulation: ✅ PASSED

Total: 4/4 tests passed

🎉 All tests passed! Gemini 3 Pro Preview is working correctly.
```

## Troubleshooting

If you see errors:

1. **"GEMINI_API_KEY not found"**: Create a `.env` file with your API key
2. **"You don't have access to gemini-3-pro-preview"**: Your account might not have access to the preview model yet
3. **"Unknown field for GenerationConfig: thinking_level"**: Update the SDK:
   ```bash
   pip install --upgrade google-generativeai
   ```

## Next Steps

Once all tests pass, you can deploy the updated `main.py` to Render with confidence that Gemini 3 Pro Preview will work correctly.

