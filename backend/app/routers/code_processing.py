"""
Code Processing Router for Voice-to-App SaaS Platform
Handles code editing, suggestions, and change processing
"""

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import structlog
import asyncio
from datetime import datetime

from app.core.config import settings
from app.services.ai_service import AIService
from app.routers.auth import AuthDependencies
from app.models.user import User

logger = structlog.get_logger()
router = APIRouter()


class CodeChangeRequest(BaseModel):
    code: str
    language: str
    context: Optional[str] = None
    description: Optional[str] = None


class CodeChangeResponse(BaseModel):
    modifiedCode: str
    description: str
    confidence: float
    changes: List[Dict[str, Any]]


class CodeSuggestionRequest(BaseModel):
    code: str
    language: str


class CodeSuggestionResponse(BaseModel):
    suggestions: List[Dict[str, Any]]


class CodeValidationRequest(BaseModel):
    code: str
    language: str


class CodeValidationResponse(BaseModel):
    isValid: bool
    errors: List[Dict[str, Any]]


@router.post("/change", response_model=CodeChangeResponse)
async def process_code_change(
    request: CodeChangeRequest,
    current_user: User = Depends(AuthDependencies.get_current_user)
):
    """Process code change request using AI"""
    try:
        ai_service = AIService()
        
        # Try local processing first if enabled
        if settings.ALLOW_LOCAL_LLM:
            try:
                result = await ai_service.process_code_change_local(
                    code=request.code,
                    language=request.language,
                    context=request.context,
                    description=request.description
                )
                method = "local"
            except Exception as e:
                logger.warning("Local code processing failed, falling back to cloud", error=str(e))
                result = await ai_service.process_code_change_cloud(
                    code=request.code,
                    language=request.language,
                    context=request.context,
                    description=request.description
                )
                method = "cloud"
        else:
            result = await ai_service.process_code_change_cloud(
                code=request.code,
                language=request.language,
                context=request.context,
                description=request.description
            )
            method = "cloud"
        
        logger.info(
            "Code change processed successfully",
            user_id=current_user.id,
            method=method,
            language=request.language,
            confidence=result.confidence
        )
        
        return CodeChangeResponse(
            modifiedCode=result.modifiedCode,
            description=result.description,
            confidence=result.confidence,
            changes=result.changes
        )
        
    except Exception as e:
        logger.error("Code change processing failed", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/suggestions", response_model=CodeSuggestionResponse)
async def get_code_suggestions(
    request: CodeSuggestionRequest,
    current_user: User = Depends(AuthDependencies.get_current_user)
):
    """Get AI-powered code suggestions"""
    try:
        ai_service = AIService()
        
        # Try local processing first if enabled
        if settings.ALLOW_LOCAL_LLM:
            try:
                suggestions = await ai_service.get_code_suggestions_local(
                    code=request.code,
                    language=request.language
                )
                method = "local"
            except Exception as e:
                logger.warning("Local code suggestions failed, falling back to cloud", error=str(e))
                suggestions = await ai_service.get_code_suggestions_cloud(
                    code=request.code,
                    language=request.language
                )
                method = "cloud"
        else:
            suggestions = await ai_service.get_code_suggestions_cloud(
                code=request.code,
                language=request.language
            )
            method = "cloud"
        
        logger.info(
            "Code suggestions generated successfully",
            user_id=current_user.id,
            method=method,
            language=request.language,
            suggestion_count=len(suggestions)
        )
        
        return CodeSuggestionResponse(suggestions=suggestions)
        
    except Exception as e:
        logger.error("Code suggestions failed", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/validate", response_model=CodeValidationResponse)
async def validate_code(
    request: CodeValidationRequest,
    current_user: User = Depends(AuthDependencies.get_current_user)
):
    """Validate code for syntax and best practices"""
    try:
        ai_service = AIService()
        
        # Try local validation first if enabled
        if settings.ALLOW_LOCAL_LLM:
            try:
                result = await ai_service.validate_code_local(
                    code=request.code,
                    language=request.language
                )
                method = "local"
            except Exception as e:
                logger.warning("Local code validation failed, falling back to cloud", error=str(e))
                result = await ai_service.validate_code_cloud(
                    code=request.code,
                    language=request.language
                )
                method = "cloud"
        else:
            result = await ai_service.validate_code_cloud(
                code=request.code,
                language=request.language
            )
            method = "cloud"
        
        logger.info(
            "Code validation completed",
            user_id=current_user.id,
            method=method,
            language=request.language,
            is_valid=result.isValid,
            error_count=len(result.errors)
        )
        
        return CodeValidationResponse(
            isValid=result.isValid,
            errors=result.errors
        )
        
    except Exception as e:
        logger.error("Code validation failed", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/languages")
async def get_supported_languages():
    """Get list of supported programming languages"""
    return {
        "languages": [
            {"name": "JavaScript", "value": "javascript", "extensions": [".js", ".jsx", ".ts", ".tsx"]},
            {"name": "Python", "value": "python", "extensions": [".py"]},
            {"name": "Java", "value": "java", "extensions": [".java"]},
            {"name": "C++", "value": "cpp", "extensions": [".cpp", ".cc", ".cxx"]},
            {"name": "C#", "value": "csharp", "extensions": [".cs"]},
            {"name": "Go", "value": "go", "extensions": [".go"]},
            {"name": "Rust", "value": "rust", "extensions": [".rs"]},
            {"name": "PHP", "value": "php", "extensions": [".php"]},
            {"name": "Ruby", "value": "ruby", "extensions": [".rb"]},
            {"name": "Swift", "value": "swift", "extensions": [".swift"]},
            {"name": "Kotlin", "value": "kotlin", "extensions": [".kt"]},
            {"name": "TypeScript", "value": "typescript", "extensions": [".ts", ".tsx"]},
            {"name": "HTML", "value": "html", "extensions": [".html", ".htm"]},
            {"name": "CSS", "value": "css", "extensions": [".css"]},
            {"name": "SQL", "value": "sql", "extensions": [".sql"]},
            {"name": "JSON", "value": "json", "extensions": [".json"]},
            {"name": "YAML", "value": "yaml", "extensions": [".yml", ".yaml"]},
            {"name": "Markdown", "value": "markdown", "extensions": [".md"]},
        ]
    }


@router.get("/templates/{language}")
async def get_code_templates(
    language: str,
    current_user: User = Depends(AuthDependencies.get_current_user)
):
    """Get code templates for a specific language"""
    templates = {
        "javascript": [
            {
                "name": "React Component",
                "description": "Basic React functional component",
                "code": """import React from 'react';

const MyComponent = ({ title, children }) => {
  return (
    <div className="component">
      <h2>{title}</h2>
      {children}
    </div>
  );
};

export default MyComponent;"""
            },
            {
                "name": "Express.js API Route",
                "description": "Basic Express.js API endpoint",
                "code": """const express = require('express');
const router = express.Router();

router.get('/api/data', async (req, res) => {
  try {
    // Your logic here
    const data = await getData();
    res.json({ success: true, data });
  } catch (error) {
    res.status(500).json({ success: false, error: error.message });
  }
});

module.exports = router;"""
            }
        ],
        "python": [
            {
                "name": "FastAPI Endpoint",
                "description": "Basic FastAPI endpoint",
                "code": """from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    description: str = None

@app.post("/items/")
async def create_item(item: Item):
    return {"message": "Item created", "item": item}"""
            },
            {
                "name": "Flask Route",
                "description": "Basic Flask route",
                "code": """from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/api/data', methods=['GET'])
def get_data():
    return jsonify({'message': 'Hello World'})"""
            }
        ]
    }
    
    return {
        "language": language,
        "templates": templates.get(language, [])
    }
