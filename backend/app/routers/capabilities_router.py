"""
200 Revolutionary Capabilities Router
Exposes the Smart Coding AI capability management system
"""

import structlog
from fastapi import APIRouter, HTTPException
from typing import Dict, List, Optional, Any

from app.services.smart_coding_ai_optimized import smart_coding_ai_optimized

logger = structlog.get_logger()

router = APIRouter(prefix="/capabilities", tags=["AI Capabilities"])


@router.get("/overview")
async def get_capabilities_overview():
    """
    Get overview of all 200 Revolutionary Capabilities
    
    Returns statistics including:
    - Total capabilities
    - Implemented count
    - Pending count
    - Implementation percentage
    - Breakdown by category
    """
    try:
        overview = await smart_coding_ai_optimized.get_capabilities_overview()
        return {
            "success": True,
            "data": overview
        }
    except Exception as e:
        logger.error("Get capabilities overview failed", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/all")
async def get_all_capabilities():
    """Get list of all 200 capabilities with their status"""
    try:
        from app.services.smart_coding_ai_capabilities import CAPABILITIES
        
        capabilities_list = [
            {
                "id": cap.id,
                "name": cap.name,
                "description": cap.description,
                "category": cap.category.value,
                "implemented": cap.implemented,
                "priority": cap.priority
            }
            for cap in CAPABILITIES
        ]
        
        return {
            "success": True,
            "total": len(capabilities_list),
            "data": capabilities_list
        }
    except Exception as e:
        logger.error("Get all capabilities failed", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{capability_id}")
async def get_capability_details(capability_id: int):
    """Get details of a specific capability by ID"""
    try:
        details = await smart_coding_ai_optimized.get_capability_details(capability_id)
        
        if details:
            return {
                "success": True,
                "data": details
            }
        else:
            raise HTTPException(status_code=404, detail=f"Capability {capability_id} not found")
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Get capability details failed", capability_id=capability_id, error=str(e))
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/category/{category_name}")
async def get_capabilities_by_category(category_name: str):
    """Get all capabilities in a specific category"""
    try:
        capabilities = await smart_coding_ai_optimized.get_capabilities_by_category(category_name)
        
        return {
            "success": True,
            "category": category_name,
            "count": len(capabilities),
            "data": capabilities
        }
    except Exception as e:
        logger.error("Get capabilities by category failed", category=category_name, error=str(e))
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/implemented")
async def get_implemented_capabilities():
    """Get list of all currently implemented capabilities"""
    try:
        capabilities = await smart_coding_ai_optimized.get_implemented_capabilities()
        
        return {
            "success": True,
            "count": len(capabilities),
            "data": capabilities
        }
    except Exception as e:
        logger.error("Get implemented capabilities failed", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/categories")
async def get_all_categories():
    """Get list of all capability categories"""
    try:
        from app.services.smart_coding_ai_capabilities import CapabilityCategory
        
        categories = [
            {
                "value": cat.value,
                "name": cat.value.replace('_', ' ').title()
            }
            for cat in CapabilityCategory
        ]
        
        return {
            "success": True,
            "count": len(categories),
            "data": categories
        }
    except Exception as e:
        logger.error("Get categories failed", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))


__all__ = ['router']

