"""
ComponentRelationship Module
Extracted from large file for better maintainability
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class ComponentRelationship(BaseModel):
    """Component relationship analysis"""
    component_id: str = Field(..., description="Unique component identifier")
    component_name: str = Field(..., description="Name of the component")
    component_type: str = Field(..., description="Type of component: class, function, module")
    file_path: str = Field(..., description="File containing the component")
    dependencies: List[str] = Field([], description="Components this depends on")
    dependents: List[str] = Field([], description="Components that depend on this")
    relationships: List[Dict[str, Any]] = Field([], description="Detailed relationship information")
    usage_frequency: int = Field(0, description="How often this component is used")
    last_modified: datetime = Field(..., description="Last modification time")
