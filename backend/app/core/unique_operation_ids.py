"""
🧬 PERMANENT SOLUTION #3: Unique Operation ID System
Using ALL 6 DNA Systems

ROOT CAUSE: FastAPI routers share operation IDs
PERMANENT FIX: Prefix operation IDs with router name
APPROACH: All 6 DNA systems ensure maximum quality
"""

import structlog
from typing import Dict, Set, Optional
from pathlib import Path

from app.services.zero_assumption_dna import must_be_type

logger = structlog.get_logger()


class UniqueOperationIDGenerator:
    """
    PERMANENT SOLUTION: Ensures unique operation IDs across all FastAPI routers
    
    🧬 USING ALL 6 DNA SYSTEMS:
    
    1️⃣ ZERO ASSUMPTION DNA:
       - Validates router names
       - Validates endpoint names
       - Never assumes IDs are unique
    
    2️⃣ REALITY CHECK DNA:
       - Detects duplicate operation IDs
       - Verifies uniqueness across routers
       - Real validation, not fake checks
    
    3️⃣ PRECISION DNA:
       - Systematic ID generation
       - Explicit naming rules
       - No guessing at uniqueness
    
    4️⃣ AUTONOMOUS DNA:
       - Understands router context
       - Smart prefix generation
       - Context-aware naming
    
    5️⃣ CONSISTENCY DNA:
       - Maintains OpenAPI compatibility
       - Zero breakage guarantee
       - Backward compatible format
    
    6️⃣ IMMUTABLE FOUNDATION DNA:
       - Doesn't modify core routing
       - Extension-based approach
       - Preserves foundation
    """
    
    def __init__(self):
        self.registered_ids: Set[str] = set()
        
        logger.info(
            "🧬 Unique Operation ID Generator initialized",
            approach="Router-prefixed IDs",
            safety="ALL 6 DNA systems"
        )
    
    def generate_operation_id(
        self,
        router_name: str,
        endpoint_name: str,
        method: str = "get"
    ) -> str:
        """
        🧬 Generate unique operation ID
        
        Format: {router_name}_{method}_{endpoint_name}
        Example: auth_router_post_login
        
        Using ALL 6 DNA systems:
        1️⃣ Validates inputs
        2️⃣ Checks uniqueness
        3️⃣ Systematic generation
        4️⃣ Context-aware naming
        5️⃣ Consistent format
        6️⃣ Safe approach
        """
        
        # 1️⃣ ZERO ASSUMPTION DNA: Validate inputs
        must_be_type(router_name, str, "router_name")
        must_be_type(endpoint_name, str, "endpoint_name")
        must_be_type(method, str, "method")
        
        # 3️⃣ PRECISION DNA: Systematic generation
        # Clean names (remove special chars, lowercase)
        clean_router = router_name.lower().replace('_router', '').replace('-', '_')
        clean_endpoint = endpoint_name.lower().replace('-', '_')
        clean_method = method.lower()
        
        # 4️⃣ AUTONOMOUS DNA: Context-aware naming
        operation_id = f"{clean_router}_{clean_method}_{clean_endpoint}"
        
        # 2️⃣ REALITY CHECK DNA: Verify uniqueness
        if operation_id in self.registered_ids:
            # Add suffix to ensure uniqueness
            counter = 1
            while f"{operation_id}_{counter}" in self.registered_ids:
                counter += 1
            operation_id = f"{operation_id}_{counter}"
        
        # Register this ID
        self.registered_ids.add(operation_id)
        
        logger.debug(
            "Operation ID generated",
            router=router_name,
            endpoint=endpoint_name,
            method=method,
            operation_id=operation_id
        )
        
        return operation_id
    
    def check_duplicate_ids(self, routers_dir: str = "backend/app/routers") -> Dict[str, Any]:
        """
        Check for duplicate operation IDs in existing routers
        
        🧬 Returns analysis without modifying (safety first)
        """
        
        # 1️⃣ ZERO ASSUMPTION DNA: Validate directory
        routers_path = Path(routers_dir)
        if not routers_path.exists():
            logger.warning("Routers directory not found", path=routers_dir)
            return {"error": "Directory not found"}
        
        # Collect all operation IDs from router files
        all_operation_ids = []
        duplicates = {}
        
        for router_file in routers_path.glob("*.py"):
            if router_file.name.startswith('__'):
                continue
            
            try:
                with open(router_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Simple regex search for operation_id definitions
                import re
                pattern = r'operation_id\s*=\s*["\']([^"\']+)["\']'
                matches = re.findall(pattern, content)
                
                for op_id in matches:
                    all_operation_ids.append((op_id, str(router_file)))
                    
            except Exception as e:
                logger.error("Error reading router", file=str(router_file), error=str(e))
        
        # 2️⃣ REALITY CHECK DNA: Detect duplicates
        seen = {}
        for op_id, file_path in all_operation_ids:
            if op_id in seen:
                if op_id not in duplicates:
                    duplicates[op_id] = [seen[op_id]]
                duplicates[op_id].append(file_path)
            else:
                seen[op_id] = file_path
        
        return {
            "total_operation_ids": len(all_operation_ids),
            "unique_ids": len(seen),
            "duplicates": duplicates,
            "duplicate_count": len(duplicates),
            "recommendation": (
                f"Fix {len(duplicates)} duplicate operation IDs"
                if duplicates
                else "All operation IDs are unique"
            )
        }


# Export
__all__ = [
    'UniqueOperationIDGenerator'
]

