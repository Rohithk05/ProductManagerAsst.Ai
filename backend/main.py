from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from groq import Groq
import os
from dotenv import load_dotenv
import re
import json

# Load environment variables
load_dotenv()

app = FastAPI(title="PM Assistant & API Doc Generator")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Groq client
api_key = os.getenv("GROQ_API_KEY")
print(f"✅ GROQ_API_KEY loaded: {bool(api_key)}")

client = Groq(api_key=api_key)


class PRDRequest(BaseModel):
    feature_idea: str
    target_audience: str
    problem_statement: str = ""


class PRDResponse(BaseModel):
    prd_document: str
    user_stories: list[str]
    success_metrics: list[str]
    timeline: str
    risks: list[str]


class APIDocRequest(BaseModel):
    code: str
    language: str
    project_name: str = "My API"


class APIDocResponse(BaseModel):
    openapi_spec: str
    markdown_docs: str
    code_examples: list[dict]


# ==================== LOGIN ROUTES (NEW) ====================

@app.get("/", response_class=HTMLResponse)
async def serve_login():
    """Serve login page"""
    try:
        with open("../frontend/login.html", "r", encoding='utf-8') as f:
            return HTMLResponse(content=f.read())
    except FileNotFoundError:
        return HTMLResponse(content="<h1>❌ login.html not found</h1>")


@app.get("/app", response_class=HTMLResponse)
async def serve_tool():
    """Serve the tool page after login"""
    try:
        with open("../frontend/index.html", "r", encoding='utf-8') as f:
            return HTMLResponse(content=f.read())
    except FileNotFoundError:
        return HTMLResponse(content="<h1>❌ index.html not found</h1>")

# ============================================================


@app.post("/api/generate-prd", response_model=PRDResponse)
async def generate_prd(request: PRDRequest):
    """Generate PRD for a feature idea"""
    if not request.feature_idea.strip():
        raise HTTPException(status_code=400, detail="Feature idea cannot be empty")
    
    prompt = f"""You are an expert Product Manager. Generate a comprehensive PRD (Product Requirements Document) for this feature.

FEATURE IDEA: {request.feature_idea}

TARGET AUDIENCE: {request.target_audience}

PROBLEM STATEMENT: {request.problem_statement}

Generate the following sections:

## 📋 PRD Document
[Complete PRD with:
- Overview
- Problem Statement
- Solution
- User Benefits
- Success Criteria
- Risks & Mitigation
- Implementation Timeline]

## 👤 User Stories
- As a [user], I want [feature] so that [benefit]
[3-5 user stories]

## 📊 Success Metrics
- Metric 1: [Description and target]
- Metric 2: [Description and target]
[3-5 metrics]

## ⏱️ Timeline
[Estimated weeks to implement]

## ⚠️ Risks
- Risk 1: [Description] → Mitigation: [How to handle]
[3-5 risks]

Format with clear sections separated by ---"""

    try:
        print(f"\n{'='*60}")
        print(f"📋 PRD GENERATION REQUEST")
        print(f"{'='*60}")
        print(f"Feature: {request.feature_idea[:50]}...")
        print(f"Target Audience: {request.target_audience}")
        print(f"Calling Groq API...")
        
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert Product Manager with 15+ years experience. Generate professional PRDs that are clear, actionable, and business-focused."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            model="llama-3.3-70b-versatile",
            temperature=0.3,
            max_tokens=2500,
            top_p=0.9
        )
        
        response_text = chat_completion.choices[0].message.content
        print(f"✅ PRD generated successfully!")
        print(f"{'='*60}\n")
        
        # Parse sections
        prd_doc = response_text
        user_stories = []
        success_metrics = []
        timeline = "2-4 weeks"
        risks = []
        
        # Extract user stories
        stories_match = re.search(r'## 👤 User Stories(.*?)(?=## |---|\\Z)', response_text, re.DOTALL)
        if stories_match:
            stories_text = stories_match.group(1)
            stories = re.findall(r'- (As a.*?)(?:\n|$)', stories_text)
            user_stories = [s.strip() for s in stories if s.strip()]
        
        # Extract success metrics
        metrics_match = re.search(r'## 📊 Success Metrics(.*?)(?=## |---|\\Z)', response_text, re.DOTALL)
        if metrics_match:
            metrics_text = metrics_match.group(1)
            metrics = re.findall(r'- (.*?)(?:\n|$)', metrics_text)
            success_metrics = [m.strip() for m in metrics if m.strip()]
        
        # Extract timeline
        timeline_match = re.search(r'## ⏱️ Timeline\n(.*?)(?=##|---|\\Z)', response_text, re.DOTALL)
        if timeline_match:
            timeline = timeline_match.group(1).strip()
        
        # Extract risks
        risks_match = re.search(r'## ⚠️ Risks(.*?)(?=##|---|\\Z)', response_text, re.DOTALL)
        if risks_match:
            risks_text = risks_match.group(1)
            risk_items = re.findall(r'- (.*?)(?:\n|$)', risks_text)
            risks = [r.strip() for r in risk_items if r.strip()]
        
        return PRDResponse(
            prd_document=prd_doc,
            user_stories=user_stories[:5] if user_stories else ["As a user, I want this feature so I can achieve my goals"],
            success_metrics=success_metrics[:5] if success_metrics else ["Adoption rate", "User engagement", "Time saved"],
            timeline=timeline,
            risks=risks[:5] if risks else ["Technical complexity", "User adoption", "Timeline risk"]
        )
        
    except Exception as e:
        print(f"\n❌ ERROR in generate_prd:")
        print(f"Error: {str(e)}")
        import traceback
        traceback.print_exc()
        print(f"{'='*60}\n")
        raise HTTPException(status_code=500, detail=f"Error generating PRD: {str(e)}")


@app.post("/api/generate-api-docs", response_model=APIDocResponse)
async def generate_api_docs(request: APIDocRequest):
    """Generate API documentation from code"""
    if not request.code.strip():
        raise HTTPException(status_code=400, detail="Code cannot be empty")
    
    prompt = f"""You are an expert API documentation specialist. Generate professional API documentation from this code.

PROJECT: {request.project_name}
LANGUAGE: {request.language}

CODE:

Generate the following:

## 📚 API Documentation (Markdown)
[Professional markdown documentation with:
- Overview
- Base URL
- Authentication
- Endpoints (method, path, description, parameters, response)
- Error codes
- Rate limiting
- Examples]

## 🔗 OpenAPI Spec
[Valid OpenAPI 3.0.0 JSON spec]

## 💻 Code Examples
[Working code examples in {request.language} and JavaScript]

Format with clear sections separated by ---SEPARATOR---"""

    try:
        print(f"\n{'='*60}")
        print(f"📚 API DOCUMENTATION GENERATION")
        print(f"{'='*60}")
        print(f"Project: {request.project_name}")
        print(f"Language: {request.language}")
        print(f"Calling Groq API...")
        
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert API documentation specialist. Create clear, professional API documentation with valid OpenAPI specs and practical code examples."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            model="llama-3.3-70b-versatile",
            temperature=0.2,
            max_tokens=3000,
            top_p=0.9
        )
        
        response_text = chat_completion.choices[0].message.content
        print(f"✅ API documentation generated!")
        print(f"{'='*60}\n")
        
        # Parse sections
        markdown_docs = ""
        openapi_spec = ""
        code_examples = []
        
        # Extract markdown docs
        markdown_match = re.search(r'## 📚 API Documentation.*?\n(.*?)(?=## 🔗|---SEPARATOR---|$)', response_text, re.DOTALL)
        if markdown_match:
            markdown_docs = markdown_match.group(1).strip()
        
        # Extract OpenAPI spec
        openapi_match = re.search(r'## 🔗 OpenAPI Spec\n(.*?)(?=## 💻|---SEPARATOR---|$)', response_text, re.DOTALL)
        if openapi_match:
            openapi_spec = openapi_match.group(1).strip()
        
        # Extract code examples
        examples_match = re.search(r'## 💻 Code Examples\n(.*?)$', response_text, re.DOTALL)
        if examples_match:
            examples_text = examples_match.group(1)
            code_examples.append({
                "language": request.language,
                "code": examples_text[:500]
            })
            code_examples.append({
                "language": "JavaScript",
                "code": examples_text[500:1000] if len(examples_text) > 500 else examples_text
            })
        
        return APIDocResponse(
            openapi_spec=openapi_spec if openapi_spec else '{"openapi": "3.0.0", "info": {"title": "API"}}',
            markdown_docs=markdown_docs if markdown_docs else "# API Documentation\n\nAPI endpoints and usage information.",
            code_examples=code_examples if code_examples else [{"language": request.language, "code": "# Example usage"}]
        )
        
    except Exception as e:
        print(f"\n❌ ERROR in generate_api_docs:")
        print(f"Error: {str(e)}")
        import traceback
        traceback.print_exc()
        print(f"{'='*60}\n")
        raise HTTPException(status_code=500, detail=f"Error generating API docs: {str(e)}")


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "api_key_set": bool(os.getenv("GROQ_API_KEY"))}


if __name__ == "__main__":
    import uvicorn
    print("\n" + "="*60)
    print("📋 PM Assistant & API Doc Generator")
    print("="*60)
    print("✅ Login Page: http://localhost:8002")
    print("✅ Tool Page: http://localhost:8002/app")
    print("="*60 + "\n")
    uvicorn.run(app, host="127.0.0.1", port=8002)

