import os
import logging
from fastapi import FastAPI, HTTPException, Header, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Optional, Literal
from dotenv import load_dotenv
from google import genai
from google.genai import types
import anthropic
from openai import OpenAI

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Load environment variables from .env file if present
load_dotenv()

app = FastAPI(
    title="Plan Master Backend API",
    description="AI-powered feature planning and codebase analysis API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load API keys from environment variable (comma-separated)
# For production, set PLAN_MASTER_API_KEYS="key1,key2,key3" in Render
# Default admin key for internal use (backend code is private, not exposed to users)
API_KEYS_ENV = os.environ.get("PLAN_MASTER_API_KEYS", "pm_admin_7k9mX2nQ8pL4vR6wY3jT5hB1cN0zF")
VALID_API_KEYS = set(key.strip() for key in API_KEYS_ENV.split(",") if key.strip())

logger.info(f"Backend initialized with {len(VALID_API_KEYS)} valid API key(s)")

def get_ai_clients():
    """Get all available AI client instances"""
    clients = {}
    
    # Gemini
    gemini_key = os.environ.get("GEMINI_API_KEY")
    if gemini_key:
        clients['gemini'] = genai.Client(api_key=gemini_key)
        logger.info("✅ Gemini client initialized")
    
    # Anthropic (Claude)
    anthropic_key = os.environ.get("ANTHROPIC_API_KEY")
    if anthropic_key:
        clients['anthropic'] = anthropic.Anthropic(api_key=anthropic_key)
        logger.info("✅ Anthropic client initialized")
    
    # OpenAI (GPT)
    openai_key = os.environ.get("OPENAI_API_KEY")
    if openai_key:
        clients['openai'] = OpenAI(api_key=openai_key)
        logger.info("✅ OpenAI client initialized")
    
    if not clients:
        raise ValueError("No AI API keys configured. Set at least one: GEMINI_API_KEY, ANTHROPIC_API_KEY, or OPENAI_API_KEY")
    
    return clients

def generate_with_ai(
    prompt: str, 
    provider: Literal["gemini", "anthropic", "openai"] = "gemini",
    model: str = None,
    config: dict = None
):
    """
    Universal AI generation function supporting multiple providers
    
    Provider & Model Selection Strategy:
    
    GEMINI (Google):
    - gemini-2.5-pro (default): Best for most tasks, balanced performance
    - gemini-3-pro-preview: Advanced reasoning for complex decisions
    
    ANTHROPIC (Claude):
    - claude-sonnet-4-5: Excellent reasoning, great for complex planning
    
    OPENAI (GPT):
    - gpt-5.1: Latest GPT model with configurable reasoning
    
    Args:
        prompt: The prompt to send
        provider: AI provider ("gemini", "anthropic", "openai")
        model: Model name (uses provider default if None)
        config: Optional generation config
    
    Returns:
        Generated text response
    """
    try:
        clients = get_ai_clients()
        
        if provider == "gemini":
            if provider not in clients:
                raise ValueError("Gemini API key not configured")
            
            model = model or "gemini-2.5-pro"
            client = clients['gemini']
            
            if config:
                response = client.models.generate_content(
                    model=model,
                    contents=prompt,
                    config=types.GenerateContentConfig(**config)
                )
            else:
                response = client.models.generate_content(
                    model=model,
                    contents=prompt,
                )
            return response.text
        
        elif provider == "anthropic":
            if provider not in clients:
                raise ValueError("Anthropic API key not configured")
            
            model = model or "claude-sonnet-4-5"
            client = clients['anthropic']
            
            max_tokens = config.get('max_tokens', 4096) if config else 4096
            
            message = client.messages.create(
                model=model,
                max_tokens=max_tokens,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )
            return message.content[0].text
        
        elif provider == "openai":
            if provider not in clients:
                raise ValueError("OpenAI API key not configured")
            
            model = model or "gpt-5.1"
            client = clients['openai']
            
            # GPT-5 uses the new responses API
            reasoning_effort = config.get('reasoning_effort', 'low') if config else 'low'
            verbosity = config.get('verbosity', 'medium') if config else 'medium'
            
            result = client.responses.create(
                model=model,
                input=prompt,
                reasoning={"effort": reasoning_effort},
                text={"verbosity": verbosity}
            )
            return result.output_text
        
        else:
            raise ValueError(f"Unknown provider: {provider}")
    
    except Exception as e:
        logger.error(f"Error generating content with {provider}/{model}: {e}")
        raise

class FileContext(BaseModel):
    path: str
    content: str

class AnalysisRequest(BaseModel):
    structure: str
    important_files: List[FileContext]

class FeatureRequest(BaseModel):
    feature_description: str

class PRDRequest(BaseModel):
    goal: str
    codebase_context: str
    additional_context: str

class BlueprintRequest(BaseModel):
    prd_content: str
    codebase_context: str
    additional_context: str

class TasksRequest(BaseModel):
    blueprint_content: str
    additional_context: str

class IndexRequest(BaseModel):
    structure: str
    important_files: List[FileContext]

class SearchRequest(BaseModel):
    query: str

class RelatedRequest(BaseModel):
    target: str

class EmbedRequest(BaseModel):
    text: str

class MemoryRequest(BaseModel):
    content: str
    key: Optional[str] = None

class ClarifyRequest(BaseModel):
    goal: str
    codebase_context: str

def verify_api_key(authorization: str = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing Authorization header")
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid Authorization header format")
    token = authorization.split(" ")[1]
    if token not in VALID_API_KEYS:
        raise HTTPException(status_code=401, detail="Invalid API key")
    return token

@app.get("/", tags=["health"])
async def root():
    """Root endpoint - health check"""
    logger.info("GET / - Root health check")
    return {
        "message": "Plan Master Backend API is running",
        "status": "healthy",
        "version": "1.0.0",
        "docs": "/docs",
        "gemini_model": "gemini-3-pro-preview"
    }

@app.get("/health", tags=["health"])
async def health_check():
    """Detailed health check endpoint"""
    logger.info("GET /health - Health check requested")
    try:
        gemini_configured = bool(os.environ.get("GEMINI_API_KEY"))
        
        # Test AI API connections
        try:
            clients = get_ai_clients()
            available_providers = list(clients.keys())
            logger.info(f"AI providers available: {available_providers}")
        except Exception as e:
            logger.error(f"AI API connection failed: {e}")
            raise HTTPException(
                status_code=503,
                detail=f"Service unhealthy - No AI providers configured: {str(e)}"
            )
        
        # Check which AI providers are configured
        ai_providers = {
            "gemini": bool(os.environ.get("GEMINI_API_KEY")),
            "anthropic": bool(os.environ.get("ANTHROPIC_API_KEY")),
            "openai": bool(os.environ.get("OPENAI_API_KEY"))
        }
        
        return {
            "status": "healthy",
            "ai_providers": ai_providers,
            "valid_api_keys_count": len(VALID_API_KEYS),
            "version": "1.0.0"
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(
            status_code=503,
            detail="Service unhealthy"
        )

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc: HTTPException):
    """Custom HTTP exception handler"""
    logger.error(f"HTTP exception: {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail, "status_code": exc.status_code}
    )

@app.exception_handler(Exception)
async def general_exception_handler(request, exc: Exception):
    """General exception handler"""
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error", "details": str(exc)}
    )

@app.post("/analyze/categorize")
async def categorize_feature(request: FeatureRequest, token: str = Depends(verify_api_key)):
    logger.info(f"POST /analyze/categorize - Feature: {request.feature_description[:50]}...")
    
    system_prompt = """You are a Senior Product Manager. Categorize the following feature request into one of these categories:
    - Landing pages
    - UI components
    - APIs
    - Performance
    - Analytics
    - Auth
    - Data management
    - Integrations
    
    Provide a confidence score and a brief explanation of why it fits this category.
    Also list 3-5 key technical considerations for this specific category.
    """
    
    # Use gemini-2.5-pro for categorization (simple classification task)
    result = generate_with_ai(
        f"{system_prompt}\n\nFeature Request: {request.feature_description}",
        provider="gemini",
        model="gemini-2.5-pro"
    )
    return {"result": result}

@app.post("/plan/clarify")
async def clarify_feature(request: ClarifyRequest, token: str = Depends(verify_api_key)):
    logger.info(f"POST /plan/clarify - Request: {request.goal[:50]}...")
    
    system_prompt = """You are a Senior Product Manager and Technical Architect. Your goal is to determine if clarifying questions are needed BEFORE creating a full feature plan.

    Analyze the feature request and codebase context carefully.
    
    CRITICAL DECISION CRITERIA:
    - If the feature request is CLEAR, SPECIFIC, and has SUFFICIENT DETAIL → Say "No clarification needed"
    - If the feature request is VAGUE, AMBIGUOUS, or MISSING CRITICAL INFORMATION → Ask 3-5 targeted questions
    
    Examples of CLEAR requests (no questions needed):
    - "Add a health check endpoint at /health that returns 200 OK"
    - "Create a dark mode toggle in the settings page using localStorage"
    - "Add JWT authentication to the API using the existing User model"
    
    Examples of UNCLEAR requests (questions needed):
    - "Add authentication" (Which type? Where? For what?)
    - "Improve performance" (What specifically? Which part?)
    - "Add user management" (CRUD? Roles? Permissions?)
    
    Focus questions on:
    1. **Scope & Requirements**: What's included/excluded? Edge cases?
    2. **User Experience**: Who uses this? What's the expected flow?
    3. **Technical Decisions**: Which approach? Integration points? Data models?
    4. **Constraints**: Performance requirements? Security concerns? Backwards compatibility?
    5. **Success Criteria**: How do we measure success? What does "done" look like?
    
    IMPORTANT OUTPUT FORMAT:
    - For clear features: MUST start with exactly "No clarification needed - the feature request is clear and straightforward."
    - For unclear features: Start with "Before creating the implementation plan, please clarify:" then list 3-5 numbered questions in Markdown.
    - Keep questions specific to the codebase and feature, not generic.
    - NEVER ask questions if the request is already clear enough to implement.
    """
    
    prompt = f"{system_prompt}\n\nFeature Request: {request.goal}\n\nCodebase Context:\n{request.codebase_context}"
    
    # Use Claude 4.5 for clarification (excellent at reasoning and asking insightful questions)
    result = generate_with_ai(
        prompt,
        provider="anthropic",
        model="claude-sonnet-4-5",
        config={"max_tokens": 2048}
    )
    return {"result": result, "needs_clarification": "No clarification needed" not in result}

@app.post("/plan/prd")
async def generate_prd(request: PRDRequest, token: str = Depends(verify_api_key)):
    logger.info(f"POST /plan/prd - Goal: {request.goal[:50]}...")
    
    system_prompt = """You are a Senior Product Manager. Your goal is to create a Product Requirements Document (PRD) for a new feature or tool.
    
    IMPORTANT: Scale your response to match the project complexity. For small/simple projects, keep it concise (20-40 lines). For complex projects, be more detailed.
    
    The PRD should include:
    1. Overview & Vision (1-2 paragraphs)
    2. Problem Statement (1 paragraph)
    3. Target Users (1-2 sentences)
    4. Success Metrics (2-4 bullet points)
    5. Functional Requirements (3-5 user stories)
    6. Non-Functional Requirements (2-4 bullet points)
    7. User Flow (brief description or simple list)
    
    Be specific and reference the existing codebase structure where relevant. If the codebase is minimal or empty, keep the PRD lightweight and focused.
    Output in Markdown format.
    """
    
    prompt = f"{system_prompt}\n\nGoal: {request.goal}\n\nCodebase Context:\n{request.codebase_context}\n\nAdditional Context:\n{request.additional_context}"
    
    # Use GPT-5.1 for PRD generation (excellent at structured documents)
    result = generate_with_ai(
        prompt,
        provider="openai",
        model="gpt-5.1",
        config={"reasoning_effort": "medium", "verbosity": "medium"}
    )
    return {"result": result}

@app.post("/plan/blueprint")
async def generate_blueprint(request: BlueprintRequest, token: str = Depends(verify_api_key)):
    logger.info("POST /plan/blueprint - Generating technical blueprint")
    
    system_prompt = """You are a Senior Software Architect. Your goal is to create a Technical Implementation Blueprint based on the PRD and existing codebase.
    
    IMPORTANT: Scale your response to match the project complexity. For small/simple projects (1-5 files), keep it concise (40-80 lines). For complex projects, be more detailed.
    
    The Blueprint should include:
    1. Current vs Target Architecture Analysis.
       CRITICAL: This section MUST include two Mermaid JS graphs enclosed in ```mermaid code blocks:
       - Graph 1: Current Architecture (Files, Classes, Dependencies relevant to the feature). Keep it SIMPLE for small projects.
       - Graph 2: Target Architecture (How the system looks after the feature). Highlight NEW components.
       
       MERMAID SYNTAX RULES (CRITICAL - FOLLOW EXACTLY):
       - Use simple graph types: "graph LR" (left-to-right) or "graph TD" (top-down)
       - Node labels with special characters (/, -, :, etc.) MUST be wrapped in double quotes: D["Health Check Endpoint"]
       - Style declarations MUST come AFTER all node and edge definitions
       - Keep graphs simple: 3-7 nodes maximum for small projects
       - Use these node shapes: [Square], (Round), ((Circle)), {"Diamond"}
       - Example of correct syntax:
         ```mermaid
         graph LR
             A["main.py"] --> B["Flask App"]
             B --> C["Requests"]
             B --> D["Health Endpoint"]
             style B fill:#f9f,stroke:#333,stroke-width:2px
             style D fill:#ccf,stroke:#333,stroke-width:2px
         ```
       
    2. Component Design (List files to create/modify with brief descriptions)
    3. Implementation Steps (High-level, 3-7 steps)
    4. Testing Strategy (Brief, 2-4 points)
    
    For minimal codebases, focus on what needs to be created rather than complex architectural patterns.
    Strictly follow existing patterns and architecture found in the Codebase Analysis.
    Output in Markdown format.
    """
    
    prompt = f"{system_prompt}\n\nPRD:\n{request.prd_content}\n\nCodebase Analysis:\n{request.codebase_context}\n\nAdditional Context:\n{request.additional_context}"
    
    # Use Claude 4.5 for blueprint (excellent at system design and architecture)
    result = generate_with_ai(
        prompt,
        provider="anthropic",
        model="claude-sonnet-4-5",
        config={"max_tokens": 4096}
    )
    return {"result": result}

@app.post("/plan/tasks")
async def generate_tasks(request: TasksRequest, token: str = Depends(verify_api_key)):
    logger.info("POST /plan/tasks - Generating actionable tasks")
    
    system_prompt = """You are a Technical Lead. Your goal is to break down the Technical Blueprint into a series of actionable, atomic tasks.
    
    IMPORTANT: Scale the number of tasks to match project complexity. For simple features, generate 5-15 tasks. For complex features, generate 20-40 tasks.
    
    Each task should:
    1. Be clearly defined (e.g., "Create src/auth/service.py with login function")
    2. Reference specific files and functions from the blueprint
    3. Be ordered logically (dependencies first)
    4. Include a brief "Definition of Done" (1 sentence)
    
    Format the output as a Markdown Task List (checkboxes) grouped by Phase/Component (2-4 phases max for simple projects).
    Keep tasks atomic and actionable. Avoid over-engineering for simple projects.
    """
    
    prompt = f"{system_prompt}\n\nTechnical Blueprint:\n{request.blueprint_content}\n\nAdditional Context:\n{request.additional_context}"
    
    # Use gemini-2.5-pro for task generation (structured output, good balance)
    result = generate_with_ai(
        prompt,
        provider="gemini",
        model="gemini-2.5-pro"
    )
    return {"result": result}

@app.post("/repo/index")
async def index_codebase(request: IndexRequest, token: str = Depends(verify_api_key)):
    logger.info(f"POST /repo/index - Indexing {len(request.important_files)} files")
    # In a real implementation, this would:
    # 1. Parse the structure and files
    # 2. Generate embeddings for file content using Gemini
    # 3. Store in a vector database (e.g., Chroma, Pinecone)
    # 4. Build a code graph
    
    # For now, we just acknowledge receipt
    summary = f"Indexed {len(request.important_files)} files from structure."
    return {"result": summary}

@app.post("/repo/search")
async def search_code(request: SearchRequest, token: str = Depends(verify_api_key)):
    logger.info(f"POST /repo/search - Query: {request.query[:50]}...")
    # Stub implementation
    # In real life: vector_db.search(request.query)
    
    # Use gemini-2.5-pro for search simulation (fast, simple task)
    result = generate_with_ai(
        f"Simulate a semantic code search result for query: '{request.query}'. Return 2-3 mocked file paths and snippet descriptions relevant to a typical web app.",
        provider="gemini",
        model="gemini-2.5-pro"
    )
    return {"result": result}

@app.post("/repo/related")
async def get_related_files(request: RelatedRequest, token: str = Depends(verify_api_key)):
    logger.info(f"POST /repo/related - Target: {request.target}")
    # Stub implementation
    # In real life: graph_db.get_neighbors(request.target)
    return {"result": f"Dependencies for '{request.target}': [MockServiceA, MockDB, Utils]"}

@app.post("/repo/embed")
async def embed_text(request: EmbedRequest, token: str = Depends(verify_api_key)):
    logger.info(f"POST /repo/embed - Length: {len(request.text)}")
    try:
        clients = get_ai_clients()
        if 'openai' not in clients:
             raise HTTPException(status_code=503, detail="OpenAI API not configured on backend")
        
        client = clients['openai']
        response = client.embeddings.create(
            model="text-embedding-3-small",
            input=request.text
        )
        return {"embedding": response.data[0].embedding}
    except Exception as e:
        logger.error(f"Embedding generation failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/memory/append")
async def append_memory(request: MemoryRequest, token: str = Depends(verify_api_key)):
    logger.info(f"POST /memory/append - Key: {request.key or 'default'}")
    # Stub: Append to project memory in DB
    return {"result": "Memory updated."}

@app.post("/memory/read")
async def read_memory(request: MemoryRequest, token: str = Depends(verify_api_key)):
    logger.info(f"POST /memory/read - Key: {request.key or 'default'}")
    # Stub: Read from project memory
    return {"result": "Project Memory: [Feature X implemented], [Refactor Y pending]."}

if __name__ == "__main__":
    import uvicorn
    # Render provides the PORT environment variable
    # Default to 10000 if not set (standard Render behavior)
    port = int(os.environ.get("PORT", 10000))
    logger.info(f"🚀 Starting Plan Master Backend...")
    logger.info(f"listening on http://0.0.0.0:{port}")
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=port,
        log_level="info"
    )
