"""
CognOmega Startup Module
Contains startup hooks and initialization routines
"""
from .self_check import run_startup_self_check, sync_run_startup_self_check
from .full_diagnostic import (
    run_startup_diagnostic,
    sync_run_startup_diagnostic,
    start_periodic_diagnostic,
    stop_periodic_diagnostic
)

__all__ = [
    'run_startup_self_check',
    'sync_run_startup_self_check',
    'run_startup_diagnostic',
    'sync_run_startup_diagnostic',
    'start_periodic_diagnostic',
    'stop_periodic_diagnostic'
]

