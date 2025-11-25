import os
import logging
from fastapi import FastAPI, HTTPException, Header, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Optional
from dotenv import load_dotenv
import google.generativeai as genai

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

def get_gemini_model():
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        # Try looking in a .env file in the parent directory as well
        load_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env'))
        api_key = os.environ.get("GEMINI_API_KEY")
    
    if not api_key:
        raise ValueError("GEMINI_API_KEY environment variable is not set on the backend.")
    
    genai.configure(api_key=api_key)
    # Using Gemini 3.0 Pro with low thinking level for faster responses
    # For complex reasoning tasks, use thinking_level="high"
    return genai.GenerativeModel(
        'gemini-3-pro-preview',
        generation_config={
            "thinking_level": "low",  # Fast responses for planning tasks
            "temperature": 1.0  # Keep default temperature as recommended
        }
    )

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
        
        # Test Gemini API connection
        if gemini_configured:
            try:
                model = get_gemini_model()
                logger.info("Gemini API connection successful")
            except Exception as e:
                logger.error(f"Gemini API connection failed: {e}")
                raise HTTPException(
                    status_code=503,
                    detail=f"Service unhealthy - Gemini API connection failed: {str(e)}"
                )
        
        return {
            "status": "healthy",
            "gemini_api_configured": gemini_configured,
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
    model = get_gemini_model()
    
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
    
    response = model.generate_content(f"{system_prompt}\n\nFeature Request: {request.feature_description}")
    return {"result": response.text}

@app.post("/plan/clarify")
async def clarify_feature(request: ClarifyRequest, token: str = Depends(verify_api_key)):
    logger.info(f"POST /plan/clarify - Request: {request.request[:50]}...")
    # Use high thinking level for clarification as it requires deeper analysis
    api_key = os.environ.get("GEMINI_API_KEY")
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(
        'gemini-3-pro-preview',
        generation_config={
            "thinking_level": "high",  # Deep reasoning for question generation
            "temperature": 1.0
        }
    )
    
    system_prompt = """You are a Senior Product Manager and Technical Architect. Your goal is to ask clarifying questions BEFORE creating a full feature plan.
    
    Analyze the feature request and codebase context, then generate 3-7 clarifying questions that will help you create a better implementation plan.
    
    Focus on questions about:
    1. **Scope & Requirements**: What's included/excluded? Edge cases?
    2. **User Experience**: Who uses this? What's the expected flow?
    3. **Technical Decisions**: Which approach? Integration points? Data models?
    4. **Constraints**: Performance requirements? Security concerns? Backwards compatibility?
    5. **Success Criteria**: How do we measure success? What does "done" look like?
    
    IMPORTANT:
    - If the feature request is VERY clear and simple (e.g., "add a health check endpoint"), return ONLY 1-2 questions or say "No clarification needed - feature is clear."
    - If the feature is vague or complex, ask 5-7 targeted questions.
    - Make questions specific to the codebase and feature, not generic.
    - Format as a numbered list in Markdown.
    
    Example output for a clear feature:
    "No clarification needed - the feature request is clear and straightforward."
    
    Example output for a complex feature:
    "Before creating the implementation plan, please clarify:
    
    1. **Authentication**: Should the new API use the existing JWT auth in `src/auth/` or implement OAuth2?
    2. **Data Storage**: Should user preferences be stored in PostgreSQL (existing) or Redis for faster access?
    3. **Backwards Compatibility**: Do we need to support the old `/api/v1/users` endpoint or can we deprecate it?
    ..."
    """
    
    prompt = f"{system_prompt}\n\nFeature Request: {request.goal}\n\nCodebase Context:\n{request.codebase_context}"
    response = model.generate_content(prompt)
    return {"result": response.text, "needs_clarification": "No clarification needed" not in response.text}

@app.post("/plan/prd")
async def generate_prd(request: PRDRequest, token: str = Depends(verify_api_key)):
    logger.info(f"POST /plan/prd - Goal: {request.goal[:50]}...")
    model = get_gemini_model()
    
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
    response = model.generate_content(prompt)
    return {"result": response.text}

@app.post("/plan/blueprint")
async def generate_blueprint(request: BlueprintRequest, token: str = Depends(verify_api_key)):
    logger.info("POST /plan/blueprint - Generating technical blueprint")
    model = get_gemini_model()
    
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
    response = model.generate_content(prompt)
    return {"result": response.text}

@app.post("/plan/tasks")
async def generate_tasks(request: TasksRequest, token: str = Depends(verify_api_key)):
    logger.info("POST /plan/tasks - Generating actionable tasks")
    model = get_gemini_model()
    
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
    response = model.generate_content(prompt)
    return {"result": response.text}

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
    model = get_gemini_model()
    response = model.generate_content(f"Simulate a semantic code search result for query: '{request.query}'. Return 2-3 mocked file paths and snippet descriptions relevant to a typical web app.")
    return {"result": response.text}

@app.post("/repo/related")
async def get_related_files(request: RelatedRequest, token: str = Depends(verify_api_key)):
    logger.info(f"POST /repo/related - Target: {request.target}")
    # Stub implementation
    # In real life: graph_db.get_neighbors(request.target)
    return {"result": f"Dependencies for '{request.target}': [MockServiceA, MockDB, Utils]"}

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
    port = int(os.environ.get("PORT", 8000))
    logger.info(f"Starting server on port {port}")
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=port
    )
