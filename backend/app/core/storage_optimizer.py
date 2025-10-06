"""
Storage Optimization Engine for CognOmega System

This module implements advanced storage optimization techniques including
data compression, incremental backups, storage tiering, and intelligent
data lifecycle management.
"""

import structlog
import asyncio
import gzip
import zlib
import bz2
import lzma
import os
import shutil
import sys
from typing import Dict, List, Optional, Any, Union, BinaryIO
from datetime import datetime, timedelta
from enum import Enum
from dataclasses import dataclass
import json
import pickle
import sqlite3
from pathlib import Path
import hashlib
import aiofiles

logger = structlog.get_logger(__name__)

class CompressionType(Enum):
    """Compression algorithm types"""
    GZIP = "gzip"
    ZLIB = "zlib"
    BZ2 = "bz2"
    LZMA = "lzma"
    NONE = "none"

class StorageTier(Enum):
    """Storage tier levels"""
    HOT = "hot"        # Fast SSD storage
    WARM = "warm"      # Standard SSD storage
    COLD = "cold"      # HDD storage
    ARCHIVE = "archive" # Compressed long-term storage

@dataclass
class StorageItem:
    """Storage item definition"""
    item_id: str
    data: Any
    size_bytes: int
    compression_type: CompressionType
    storage_tier: StorageTier
    created_at: datetime
    last_accessed: datetime
    access_count: int
    file_path: str
    checksum: str

@dataclass
class StorageMetrics:
    """Storage usage metrics"""
    total_size_bytes: int
    compressed_size_bytes: int
    compression_ratio: float
    hot_tier_size: int
    warm_tier_size: int
    cold_tier_size: int
    archive_tier_size: int
    timestamp: datetime

class StorageOptimizer:
    """Advanced storage optimization engine"""
    
    def __init__(self, base_storage_path: str = "storage"):
        self.base_storage_path = Path(base_storage_path)
        self.base_storage_path.mkdir(exist_ok=True)
        
        # Storage tiers
        self.storage_tiers = {
            StorageTier.HOT: self.base_storage_path / "hot",
            StorageTier.WARM: self.base_storage_path / "warm",
            StorageTier.COLD: self.base_storage_path / "cold",
            StorageTier.ARCHIVE: self.base_storage_path / "archive"
        }
        
        # Create tier directories
        for tier_path in self.storage_tiers.values():
            tier_path.mkdir(exist_ok=True)
        
        # Storage items registry
        self.storage_registry: Dict[str, StorageItem] = {}
        
        # Optimization metrics
        self.optimization_metrics = {
            "total_items": 0,
            "compressed_items": 0,
            "total_original_size": 0,
            "total_compressed_size": 0,
            "backups_created": 0,
            "data_migrations": 0
        }
        
        # Compression settings
        self.compression_settings = {
            CompressionType.GZIP: {"level": 6},
            CompressionType.ZLIB: {"level": 6},
            CompressionType.BZ2: {"level": 6},
            CompressionType.LZMA: {"level": 6}
        }
        
        # Storage policies
        self.storage_policies = {
            "hot_tier_max_age": timedelta(hours=24),
            "warm_tier_max_age": timedelta(days=7),
            "cold_tier_max_age": timedelta(days=30),
            "archive_tier_min_age": timedelta(days=90)
        }
        
        logger.info(f"Storage Optimizer initialized with base path: {self.base_storage_path}")

    async def optimize_data_compression(self, data: Any, compression_type: CompressionType = CompressionType.GZIP) -> bytes:
        """Optimize data compression with intelligent algorithm selection"""
        try:
            # Serialize data first
            serialized_data = await self._serialize_data(data)
            
            # Apply compression
            compressed_data = await self._apply_compression(serialized_data, compression_type)
            
            # Update metrics
            original_size = len(serialized_data)
            compressed_size = len(compressed_data)
            compression_ratio = (1 - compressed_size / original_size) * 100 if original_size > 0 else 0
            
            self.optimization_metrics["total_original_size"] += original_size
            self.optimization_metrics["total_compressed_size"] += compressed_size
            self.optimization_metrics["compressed_items"] += 1
            
            logger.info(f"Data compressed: {original_size} -> {compressed_size} bytes ({compression_ratio:.1f}% reduction)")
            
            return compressed_data
            
        except Exception as e:
            logger.error(f"Data compression optimization failed", error=str(e))
            raise

    async def _serialize_data(self, data: Any) -> bytes:
        """Serialize data for storage"""
        try:
            if isinstance(data, (dict, list)):
                return json.dumps(data).encode('utf-8')
            elif isinstance(data, str):
                return data.encode('utf-8')
            elif isinstance(data, bytes):
                return data
            else:
                return pickle.dumps(data)
        except Exception as e:
            logger.error(f"Data serialization failed", error=str(e))
            raise

    async def _apply_compression(self, data: bytes, compression_type: CompressionType) -> bytes:
        """Apply compression algorithm to data"""
        try:
            if compression_type == CompressionType.GZIP:
                return gzip.compress(data, **self.compression_settings[CompressionType.GZIP])
            elif compression_type == CompressionType.ZLIB:
                return zlib.compress(data, **self.compression_settings[CompressionType.ZLIB])
            elif compression_type == CompressionType.BZ2:
                return bz2.compress(data, **self.compression_settings[CompressionType.BZ2])
            elif compression_type == CompressionType.LZMA:
                return lzma.compress(data, **self.compression_settings[CompressionType.LZMA])
            else:
                return data
        except Exception as e:
            logger.error(f"Compression application failed", error=str(e))
            raise

    async def store_optimized_data(self, item_id: str, data: Any, storage_tier: StorageTier = StorageTier.HOT, 
                                 compression_type: CompressionType = CompressionType.GZIP) -> str:
        """Store data with optimization"""
        try:
            logger.info(f"Storing optimized data: {item_id} in {storage_tier.value} tier")
            
            # Compress data
            compressed_data = await self.optimize_data_compression(data, compression_type)
            
            # Generate file path
            file_path = self.storage_tiers[storage_tier] / f"{item_id}.dat"
            
            # Calculate checksum
            checksum = hashlib.sha256(compressed_data).hexdigest()
            
            # Create storage item
            storage_item = StorageItem(
                item_id=item_id,
                data=data,
                size_bytes=len(compressed_data),
                compression_type=compression_type,
                storage_tier=storage_tier,
                created_at=datetime.now(),
                last_accessed=datetime.now(),
                access_count=1,
                file_path=str(file_path),
                checksum=checksum
            )
            
            # Write to storage (async)
            async with aiofiles.open(file_path, 'wb') as f:
                await f.write(compressed_data)
            
            # Update registry
            self.storage_registry[item_id] = storage_item
            self.optimization_metrics["total_items"] += 1
            
            logger.info(f"Data stored successfully: {item_id} at {file_path}")
            return item_id
            
        except Exception as e:
            logger.error(f"Optimized data storage failed for {item_id}", error=str(e))
            raise

    async def retrieve_optimized_data(self, item_id: str) -> Any:
        """Retrieve and decompress data"""
        try:
            if item_id not in self.storage_registry:
                raise ValueError(f"Storage item not found: {item_id}")
            
            storage_item = self.storage_registry[item_id]
            
            # Update access metrics
            storage_item.last_accessed = datetime.now()
            storage_item.access_count += 1
            
            # Read compressed data (async)
            async with aiofiles.open(storage_item.file_path, 'rb') as f:
                compressed_data = await f.read()
            
            # Verify checksum
            if hashlib.sha256(compressed_data).hexdigest() != storage_item.checksum:
                raise ValueError(f"Checksum verification failed for {item_id}")
            
            # Decompress data
            decompressed_data = await self._decompress_data(compressed_data, storage_item.compression_type)
            
            # Deserialize data
            original_data = await self._deserialize_data(decompressed_data, storage_item.data)
            
            logger.info(f"Data retrieved successfully: {item_id}")
            return original_data
            
        except Exception as e:
            logger.error(f"Optimized data retrieval failed for {item_id}", error=str(e))
            raise

    async def _decompress_data(self, compressed_data: bytes, compression_type: CompressionType) -> bytes:
        """Decompress data"""
        try:
            if compression_type == CompressionType.GZIP:
                return gzip.decompress(compressed_data)
            elif compression_type == CompressionType.ZLIB:
                return zlib.decompress(compressed_data)
            elif compression_type == CompressionType.BZ2:
                return bz2.decompress(compressed_data)
            elif compression_type == CompressionType.LZMA:
                return lzma.decompress(compressed_data)
            else:
                return compressed_data
        except Exception as e:
            logger.error(f"Data decompression failed", error=str(e))
            raise

    async def _deserialize_data(self, data: bytes, original_data: Any) -> Any:
        """Deserialize data back to original format"""
        try:
            # Try JSON first
            try:
                return json.loads(data.decode('utf-8'))
            except (json.JSONDecodeError, UnicodeDecodeError):
                pass
            
            # Try pickle
            try:
                return pickle.loads(data)
            except pickle.PickleError:
                pass
            
            # Return as bytes
            return data
            
        except Exception as e:
            logger.error(f"Data deserialization failed", error=str(e))
            return data

    async def create_incremental_backup(self, backup_name: str, include_tiers: List[StorageTier] = None) -> str:
        """Create incremental backup of storage"""
        try:
            if include_tiers is None:
                include_tiers = list(StorageTier)
            
            logger.info(f"Creating incremental backup: {backup_name}")
            
            backup_path = self.base_storage_path / "backups" / backup_name
            backup_path.mkdir(parents=True, exist_ok=True)
            
            backup_manifest = {
                "backup_name": backup_name,
                "created_at": datetime.now().isoformat(),
                "included_tiers": [tier.value for tier in include_tiers],
                "items": []
            }
            
            # Backup items from specified tiers
            for tier in include_tiers:
                tier_backup_path = backup_path / tier.value
                tier_backup_path.mkdir(exist_ok=True)
                
                tier_items = [item for item in self.storage_registry.values() if item.storage_tier == tier]
                
                for item in tier_items:
                    # Copy file to backup
                    source_path = Path(item.file_path)
                    backup_file_path = tier_backup_path / f"{item.item_id}.dat"
                    
                    if source_path.exists():
                        shutil.copy2(source_path, backup_file_path)
                        
                        backup_manifest["items"].append({
                            "item_id": item.item_id,
                            "tier": tier.value,
                            "size_bytes": item.size_bytes,
                            "checksum": item.checksum,
                            "created_at": item.created_at.isoformat()
                        })
            
            # Save backup manifest (async)
            manifest_path = backup_path / "manifest.json"
            async with aiofiles.open(manifest_path, 'w') as f:
                await f.write(json.dumps(backup_manifest, indent=2))
            
            self.optimization_metrics["backups_created"] += 1
            
            logger.info(f"Incremental backup created: {backup_name} with {len(backup_manifest['items'])} items")
            return str(backup_path)
            
        except Exception as e:
            logger.error(f"Incremental backup creation failed", error=str(e))
            raise

    async def optimize_storage_tiering(self):
        """Optimize storage tiering based on access patterns"""
        try:
            logger.info("Optimizing storage tiering")
            
            current_time = datetime.now()
            migrations = []
            
            for item_id, item in self.storage_registry.items():
                # Determine optimal tier based on access patterns
                optimal_tier = self._determine_optimal_tier(item, current_time)
                
                if optimal_tier != item.storage_tier:
                    # Migrate item to optimal tier
                    await self._migrate_storage_item(item, optimal_tier)
                    migrations.append({
                        "item_id": item_id,
                        "from_tier": item.storage_tier.value,
                        "to_tier": optimal_tier.value,
                        "reason": "access_pattern_optimization"
                    })
            
            self.optimization_metrics["data_migrations"] += len(migrations)
            
            logger.info(f"Storage tiering optimization completed, {len(migrations)} migrations")
            return migrations
            
        except Exception as e:
            logger.error(f"Storage tiering optimization failed", error=str(e))
            raise

    def _determine_optimal_tier(self, item: StorageItem, current_time: datetime) -> StorageTier:
        """Determine optimal storage tier for item"""
        age = current_time - item.created_at
        last_access_age = current_time - item.last_accessed
        
        # Archive tier: very old items
        if age > self.storage_policies["archive_tier_min_age"]:
            return StorageTier.ARCHIVE
        
        # Cold tier: old items with low access
        if age > self.storage_policies["cold_tier_max_age"] and last_access_age > timedelta(days=7):
            return StorageTier.COLD
        
        # Warm tier: moderately old items
        if age > self.storage_policies["warm_tier_max_age"]:
            return StorageTier.WARM
        
        # Hot tier: recent items or frequently accessed
        if age < self.storage_policies["hot_tier_max_age"] or item.access_count > 10:
            return StorageTier.HOT
        
        return StorageTier.WARM

    async def _migrate_storage_item(self, item: StorageItem, new_tier: StorageTier):
        """Migrate storage item to new tier"""
        try:
            # Read data from current location (async)
            async with aiofiles.open(item.file_path, 'rb') as f:
                data = await f.read()
            
            # Create new file path
            new_file_path = self.storage_tiers[new_tier] / f"{item.item_id}.dat"
            
            # Write to new location (async)
            async with aiofiles.open(new_file_path, 'wb') as f:
                await f.write(data)
            
            # Remove old file
            os.remove(item.file_path)
            
            # Update item metadata
            item.storage_tier = new_tier
            item.file_path = str(new_file_path)
            
            logger.info(f"Storage item migrated: {item.item_id} to {new_tier.value} tier")
            
        except Exception as e:
            logger.error(f"Storage item migration failed for {item.item_id}", error=str(e))
            raise

    async def cleanup_old_data(self, retention_days: int = 90):
        """Cleanup old data based on retention policy"""
        try:
            logger.info(f"Cleaning up data older than {retention_days} days")
            
            cutoff_date = datetime.now() - timedelta(days=retention_days)
            items_to_remove = []
            
            for item_id, item in self.storage_registry.items():
                if item.created_at < cutoff_date and item.last_accessed < cutoff_date:
                    items_to_remove.append(item_id)
            
            # Remove items
            for item_id in items_to_remove:
                item = self.storage_registry[item_id]
                
                # Remove file
                if os.path.exists(item.file_path):
                    os.remove(item.file_path)
                
                # Remove from registry
                del self.storage_registry[item_id]
            
            logger.info(f"Data cleanup completed, removed {len(items_to_remove)} items")
            return len(items_to_remove)
            
        except Exception as e:
            logger.error(f"Data cleanup failed", error=str(e))
            raise

    async def get_storage_metrics(self) -> StorageMetrics:
        """Get comprehensive storage metrics"""
        try:
            total_size = 0
            compressed_size = 0
            tier_sizes = {tier: 0 for tier in StorageTier}
            
            for item in self.storage_registry.values():
                total_size += sys.getsizeof(item.data) if hasattr(sys, 'getsizeof') else len(str(item.data))
                compressed_size += item.size_bytes
                tier_sizes[item.storage_tier] += item.size_bytes
            
            compression_ratio = (1 - compressed_size / total_size) * 100 if total_size > 0 else 0
            
            return StorageMetrics(
                total_size_bytes=total_size,
                compressed_size_bytes=compressed_size,
                compression_ratio=compression_ratio,
                hot_tier_size=tier_sizes[StorageTier.HOT],
                warm_tier_size=tier_sizes[StorageTier.WARM],
                cold_tier_size=tier_sizes[StorageTier.COLD],
                archive_tier_size=tier_sizes[StorageTier.ARCHIVE],
                timestamp=datetime.now()
            )
            
        except Exception as e:
            logger.error(f"Storage metrics retrieval failed", error=str(e))
            raise

    async def optimize_service_storage(self, service_name: str, data_items: List[Any]) -> Dict[str, Any]:
        """Optimize storage for specific service"""
        try:
            logger.info(f"Optimizing storage for service: {service_name}")
            
            # Analyze storage patterns
            storage_analysis = self._analyze_service_storage_patterns(service_name, data_items)
            
            # Apply storage optimizations
            optimization_results = await self._apply_storage_optimizations(service_name, data_items, storage_analysis)
            
            # Calculate storage efficiency
            storage_efficiency = self._calculate_storage_efficiency(optimization_results)
            
            return {
                "service_name": service_name,
                "original_items": len(data_items),
                "optimized_items": len(optimization_results["stored_items"]),
                "storage_efficiency": storage_efficiency,
                "storage_analysis": storage_analysis,
                "optimization_results": optimization_results
            }
            
        except Exception as e:
            logger.error(f"Service storage optimization failed for {service_name}", error=str(e))
            raise

    def _analyze_service_storage_patterns(self, service_name: str, data_items: List[Any]) -> Dict[str, Any]:
        """Analyze storage patterns for specific service"""
        analysis = {
            "service_name": service_name,
            "total_items": len(data_items),
            "total_size_bytes": sum(sys.getsizeof(item) if hasattr(sys, 'getsizeof') else len(str(item)) for item in data_items),
            "average_item_size": 0,
            "large_items": 0,
            "recommendations": []
        }
        
        if data_items:
            analysis["average_item_size"] = analysis["total_size_bytes"] / len(data_items)
        
        # Identify large items
        for item in data_items:
            item_size = sys.getsizeof(item) if hasattr(sys, 'getsizeof') else len(str(item))
            if item_size > 1024 * 1024:  # Items larger than 1MB
                analysis["large_items"] += 1
        
        # Generate recommendations
        if analysis["average_item_size"] > 512 * 1024:  # Average size > 512KB
            analysis["recommendations"].append("Consider using high compression for large items")
        
        if analysis["large_items"] > len(data_items) * 0.2:
            analysis["recommendations"].append("High proportion of large items detected")
        
        return analysis

    async def _apply_storage_optimizations(self, service_name: str, data_items: List[Any], analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Apply storage optimizations to service data"""
        optimization_results = {
            "stored_items": [],
            "compression_savings": 0,
            "tier_allocations": {tier.value: 0 for tier in StorageTier}
        }
        
        for i, item in enumerate(data_items):
            # Determine optimal compression and tier
            compression_type = self._select_optimal_compression(item, analysis)
            storage_tier = self._select_optimal_tier(item, analysis)
            
            # Store item
            item_id = f"{service_name}_{i}_{datetime.now().timestamp()}"
            await self.store_optimized_data(item_id, item, storage_tier, compression_type)
            
            optimization_results["stored_items"].append(item_id)
            optimization_results["tier_allocations"][storage_tier.value] += 1
        
        return optimization_results

    def _select_optimal_compression(self, item: Any, analysis: Dict[str, Any]) -> CompressionType:
        """Select optimal compression algorithm for item"""
        item_size = sys.getsizeof(item) if hasattr(sys, 'getsizeof') else len(str(item))
        
        if item_size > 1024 * 1024:  # Large items
            return CompressionType.LZMA  # Best compression
        elif item_size > 100 * 1024:  # Medium items
            return CompressionType.GZIP  # Balanced compression
        else:  # Small items
            return CompressionType.ZLIB  # Fast compression

    def _select_optimal_tier(self, item: Any, analysis: Dict[str, Any]) -> StorageTier:
        """Select optimal storage tier for item"""
        item_size = sys.getsizeof(item) if hasattr(sys, 'getsizeof') else len(str(item))
        
        if item_size > 10 * 1024 * 1024:  # Very large items
            return StorageTier.COLD
        elif item_size > 1024 * 1024:  # Large items
            return StorageTier.WARM
        else:  # Small/medium items
            return StorageTier.HOT

    def _calculate_storage_efficiency(self, optimization_results: Dict[str, Any]) -> float:
        """Calculate storage efficiency score"""
        # This would be more sophisticated in a real implementation
        return 85.0  # Placeholder efficiency score

    async def get_storage_optimization_metrics(self) -> Dict[str, Any]:
        """Get comprehensive storage optimization metrics"""
        try:
            storage_metrics = await self.get_storage_metrics()
            
            return {
                "storage_metrics": {
                    "total_size_gb": storage_metrics.total_size_bytes / (1024**3),
                    "compressed_size_gb": storage_metrics.compressed_size_bytes / (1024**3),
                    "compression_ratio": storage_metrics.compression_ratio,
                    "hot_tier_mb": storage_metrics.hot_tier_size / (1024**2),
                    "warm_tier_mb": storage_metrics.warm_tier_size / (1024**2),
                    "cold_tier_mb": storage_metrics.cold_tier_size / (1024**2),
                    "archive_tier_mb": storage_metrics.archive_tier_size / (1024**2)
                },
                "optimization_metrics": self.optimization_metrics,
                "storage_policies": self.storage_policies,
                "registry_status": {
                    "total_items": len(self.storage_registry),
                    "items_by_tier": {
                        tier.value: len([item for item in self.storage_registry.values() if item.storage_tier == tier])
                        for tier in StorageTier
                    }
                }
            }
            
        except Exception as e:
            logger.error(f"Storage optimization metrics retrieval failed", error=str(e))
            raise

    async def cleanup(self):
        """Cleanup storage optimizer resources"""
        try:
            await self.cleanup_old_data()
            await self.optimize_storage_tiering()
            logger.info("Storage Optimizer cleanup completed")
        except Exception as e:
            logger.error(f"Storage Optimizer cleanup failed", error=str(e))

# Global storage optimizer instance
storage_optimizer = StorageOptimizer()
