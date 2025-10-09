"""
CognOmega Startup Module
Contains startup hooks and initialization routines
"""
from .self_check import run_startup_self_check, sync_run_startup_self_check

__all__ = [
    'run_startup_self_check',
    'sync_run_startup_self_check'
]

