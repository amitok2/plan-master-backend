# Multi-Provider AI Integration Guide

Plan Master Backend now supports **three AI providers** for maximum flexibility and performance.

## Supported Providers

### 1. **Google Gemini**
- **Models**: `gemini-2.5-pro`, `gemini-3-pro-preview`
- **Best For**: General tasks, balanced performance, cost-effective
- **API Key**: `GEMINI_API_KEY`

### 2. **Anthropic Claude**
- **Models**: `claude-sonnet-4-5`
- **Best For**: Complex reasoning, system design, clarifying questions
- **API Key**: `ANTHROPIC_API_KEY`

### 3. **OpenAI GPT**
- **Models**: `gpt-5.1`
- **Best For**: Structured documents, PRDs, configurable reasoning
- **API Key**: `OPENAI_API_KEY`

## Configuration

Add API keys to your `.env` file or environment variables:

```bash
# At least one is required, all three recommended
GEMINI_API_KEY=your_gemini_key_here
ANTHROPIC_API_KEY=your_anthropic_key_here
OPENAI_API_KEY=your_openai_key_here
```

## Model Selection Strategy

| Endpoint | Provider | Model | Reasoning |
|----------|----------|-------|-----------|
| `/analyze/categorize` | Gemini | gemini-2.5-pro | Simple classification, fast |
| `/plan/clarify` | **Claude** | claude-sonnet-4-5 | Excellent at asking insightful questions |
| `/plan/prd` | **GPT** | gpt-5.1 | Great at structured documents |
| `/plan/blueprint` | **Claude** | claude-sonnet-4-5 | Superior system design and architecture |
| `/plan/tasks` | Gemini | gemini-2.5-pro | Structured breakdown, cost-effective |
| `/repo/search` | Gemini | gemini-2.5-pro | Fast, simple task |

## Why Multiple Providers?

### **Redundancy**
- If one provider has an outage, others can handle requests
- Fallback logic can be implemented

### **Cost Optimization**
- Use cheaper models (Gemini) for simple tasks
- Reserve expensive models (Claude, GPT-5) for complex reasoning

### **Quality**
- Each model has unique strengths
- Claude excels at reasoning and architecture
- GPT-5.1 excels at structured documents
- Gemini offers best price/performance ratio

### **Performance**
- Different models have different latency characteristics
- Can optimize per-endpoint based on requirements

## Testing

Run the comprehensive test suite:

```bash
cd plan-master-backend
python3 test_all_providers.py
```

This will test:
- ✅ Basic connectivity for each provider
- ✅ Clarification task (Claude)
- ✅ PRD generation (GPT)
- ✅ Blueprint generation (Claude)

## API Usage Examples

### Gemini
```python
from google import genai

client = genai.Client(api_key=api_key)
response = client.models.generate_content(
    model="gemini-2.5-pro",
    contents=prompt,
)
print(response.text)
```

### Claude
```python
import anthropic

client = anthropic.Anthropic(api_key=api_key)
message = client.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=2048,
    messages=[{"role": "user", "content": prompt}]
)
print(message.content[0].text)
```

### GPT-5.1
```python
from openai import OpenAI

client = OpenAI(api_key=api_key)
result = client.responses.create(
    model="gpt-5.1",
    input=prompt,
    reasoning={"effort": "medium"},
    text={"verbosity": "medium"}
)
print(result.output_text)
```

## Cost Comparison

| Provider | Model | Input (per 1M tokens) | Output (per 1M tokens) |
|----------|-------|----------------------|------------------------|
| Gemini | gemini-2.5-pro | ~$1.25 | ~$5.00 |
| Gemini | gemini-3-pro-preview | ~$2.00 | ~$12.00 |
| Anthropic | claude-sonnet-4-5 | ~$3.00 | ~$15.00 |
| OpenAI | gpt-5.1 | ~$5.00 | ~$20.00 |

*Prices are approximate and subject to change*

## Performance Characteristics

| Provider | Model | Avg Response Time | Token Limit |
|----------|-------|-------------------|-------------|
| Gemini | gemini-2.5-pro | 2-5s | 1M input / 64k output |
| Gemini | gemini-3-pro-preview | 5-15s | 1M input / 64k output |
| Anthropic | claude-sonnet-4-5 | 3-8s | 200k input / 8k output |
| OpenAI | gpt-5.1 | 4-10s | 128k input / 16k output |

## Fallback Strategy (Future)

When implementing fallback logic:

1. **Primary**: Use the designated model for the task
2. **Secondary**: If primary fails, try Gemini (most reliable)
3. **Tertiary**: If both fail, return error with retry suggestion

## Environment Variables Summary

```bash
# Required (at least one)
GEMINI_API_KEY=your_key
ANTHROPIC_API_KEY=your_key
OPENAI_API_KEY=your_key

# Optional (for Plan Master auth)
PLAN_MASTER_API_KEYS=key1,key2,key3
```

## Health Check

The `/health` endpoint now reports which providers are configured:

```json
{
  "status": "healthy",
  "ai_providers": {
    "gemini": true,
    "anthropic": true,
    "openai": true
  },
  "valid_api_keys_count": 3,
  "version": "1.0.0"
}
```

## Deployment

When deploying to Render:

1. Add all three API keys as environment variables
2. Run `pip install -r requirements.txt` to install all SDKs
3. Test with `python3 test_all_providers.py`
4. Deploy and verify `/health` endpoint

## Troubleshooting

### "No AI API keys configured"
- Set at least one of: GEMINI_API_KEY, ANTHROPIC_API_KEY, or OPENAI_API_KEY

### "Provider not configured"
- The requested provider's API key is missing
- Check environment variables

### Rate Limits
- Each provider has different rate limits
- Implement exponential backoff for retries
- Consider caching responses for common queries

---

**Last Updated**: 2025-11-25  
**Version**: 2.0.0 (Multi-Provider Support)

