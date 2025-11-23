import os
from fastapi import FastAPI, HTTPException, Header, Depends
from pydantic import BaseModel
from typing import List, Optional
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables from .env file if present
load_dotenv()

app = FastAPI()

# In a real scenario, you'd use a database for API keys
VALID_API_KEYS = {"test-key-123", "dev-key-456"}

def get_gemini_model():
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        # Try looking in a .env file in the parent directory as well
        load_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env'))
        api_key = os.environ.get("GEMINI_API_KEY")
    
    if not api_key:
        raise ValueError("GEMINI_API_KEY environment variable is not set on the backend.")
    
    genai.configure(api_key=api_key)
    return genai.GenerativeModel('gemini-2.0-flash-exp') # Or gemini-1.5-pro

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

def verify_api_key(authorization: str = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing Authorization header")
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid Authorization header format")
    token = authorization.split(" ")[1]
    if token not in VALID_API_KEYS:
        raise HTTPException(status_code=401, detail="Invalid API key")
    return token

@app.post("/analyze/categorize")
async def categorize_feature(request: FeatureRequest, token: str = Depends(verify_api_key)):
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

@app.post("/plan/prd")
async def generate_prd(request: PRDRequest, token: str = Depends(verify_api_key)):
    model = get_gemini_model()
    
    system_prompt = """You are a Senior Product Manager. Your goal is to create a detailed Product Requirements Document (PRD) for a new feature or tool.
    The PRD should include:
    1. Overview & Vision
    2. Problem Statement
    3. Target Users
    4. Success Metrics
    5. Functional Requirements (User Stories)
    6. Non-Functional Requirements
    7. User Flow
    
    Be specific and reference the existing codebase structure where relevant.
    Output in Markdown format.
    """
    
    prompt = f"{system_prompt}\n\nGoal: {request.goal}\n\nContext:\n{request.codebase_context}\n\nAdditional Context:\n{request.additional_context}"
    response = model.generate_content(prompt)
    return {"result": response.text}

@app.post("/plan/blueprint")
async def generate_blueprint(request: BlueprintRequest, token: str = Depends(verify_api_key)):
    model = get_gemini_model()
    
    system_prompt = """You are a Senior Software Architect. Your goal is to create a Technical Implementation Blueprint based on the PRD and existing codebase.
    The Blueprint should include:
    1. Current vs Target Architecture Analysis
    2. Component Design (Endpoints, Services, Models)
    3. Data Flow Diagrams (Description)
    4. Database Schema Changes
    5. API Specifications
    6. Security Considerations
    7. Testing Strategy
    
    Strictly follow existing patterns and architecture found in the Codebase Analysis.
    Output in Markdown format.
    """
    
    prompt = f"{system_prompt}\n\nPRD:\n{request.prd_content}\n\nCodebase Analysis:\n{request.codebase_context}\n\nAdditional Context:\n{request.additional_context}"
    response = model.generate_content(prompt)
    return {"result": response.text}

@app.post("/plan/tasks")
async def generate_tasks(request: TasksRequest, token: str = Depends(verify_api_key)):
    model = get_gemini_model()
    
    system_prompt = """You are a Technical Lead. Your goal is to break down the Technical Blueprint into a series of actionable, atomic tasks.
    
    Each task should:
    1. Be clearly defined (e.g., "Create src/auth/service.py with login function")
    2. Reference specific files and functions from the blueprint
    3. Be ordered logically (dependencies first)
    4. Include a brief "Definition of Done"
    
    Format the output as a Markdown Task List (checkboxes) grouped by Phase/Component.
    """
    
    prompt = f"{system_prompt}\n\nTechnical Blueprint:\n{request.blueprint_content}\n\nAdditional Context:\n{request.additional_context}"
    response = model.generate_content(prompt)
    return {"result": response.text}

@app.post("/repo/index")
async def index_codebase(request: IndexRequest, token: str = Depends(verify_api_key)):
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
    # Stub implementation
    # In real life: vector_db.search(request.query)
    model = get_gemini_model()
    response = model.generate_content(f"Simulate a semantic code search result for query: '{request.query}'. Return 2-3 mocked file paths and snippet descriptions relevant to a typical web app.")
    return {"result": response.text}

@app.post("/repo/related")
async def get_related_files(request: RelatedRequest, token: str = Depends(verify_api_key)):
    # Stub implementation
    # In real life: graph_db.get_neighbors(request.target)
    return {"result": f"Dependencies for '{request.target}': [MockServiceA, MockDB, Utils]"}

@app.post("/memory/append")
async def append_memory(request: MemoryRequest, token: str = Depends(verify_api_key)):
    # Stub: Append to project memory in DB
    return {"result": "Memory updated."}

@app.post("/memory/read")
async def read_memory(request: MemoryRequest, token: str = Depends(verify_api_key)):
    # Stub: Read from project memory
    return {"result": "Project Memory: [Feature X implemented], [Refactor Y pending]."}
