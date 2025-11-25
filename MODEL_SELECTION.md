# Model Selection Strategy

This document explains when and why we use different Gemini models in the Plan Master backend.

## Available Models

### 1. **gemini-2.5-pro** (Default)
- **Use Case**: General-purpose tasks, balanced performance
- **Strengths**: 
  - Fast response times
  - Good quality output
  - Cost-effective
  - Reliable and stable
- **Best For**:
  - PRD generation
  - Task breakdown
  - Code search simulation
  - Feature categorization
  - Most standard planning tasks

### 2. **gemini-3-pro-preview** (Advanced Reasoning)
- **Use Case**: Complex reasoning and architecture decisions
- **Strengths**:
  - Advanced reasoning capabilities
  - Deep context understanding
  - Better at complex technical decisions
- **Best For**:
  - Clarifying questions (requires understanding nuance)
  - Technical blueprint generation (architecture decisions)
  - Complex system design
  - Multi-step reasoning tasks

### 3. **gemini-2.0-flash-exp** (Fast & Light)
- **Use Case**: Simple, quick responses
- **Strengths**:
  - Extremely fast
  - Low cost
  - Good for simple tasks
- **Best For**:
  - Health checks
  - Simple queries
  - Quick categorizations
  - *Currently not used but available if needed*

## Current Endpoint Mapping

| Endpoint | Model | Reasoning |
|----------|-------|-----------|
| `/analyze/categorize` | gemini-2.5-pro | Simple classification task |
| `/plan/clarify` | gemini-3-pro-preview | Requires deep reasoning to ask intelligent questions |
| `/plan/prd` | gemini-2.5-pro | Structured output, good balance of quality and speed |
| `/plan/blueprint` | gemini-3-pro-preview | Complex architecture decisions require advanced reasoning |
| `/plan/tasks` | gemini-2.5-pro | Structured breakdown, standard complexity |
| `/repo/search` | gemini-2.5-pro | Simple simulation task |

## Cost Considerations

- **gemini-2.5-pro**: Most cost-effective for production use
- **gemini-3-pro-preview**: Higher cost but necessary for complex reasoning
- Use gemini-3 only when the task truly benefits from advanced reasoning

## Performance Considerations

- **gemini-2.5-pro**: ~2-5 seconds response time
- **gemini-3-pro-preview**: ~5-15 seconds (uses dynamic thinking)
- Balance user experience with quality requirements

## Future Optimization

As models evolve:
1. Monitor response quality and adjust model selection
2. Consider A/B testing different models for specific endpoints
3. Add caching for common queries
4. Implement fallback logic if gemini-3 is unavailable

