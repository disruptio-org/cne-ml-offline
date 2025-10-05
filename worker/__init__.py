"""Worker package root to ease imports across services."""

from .src import process_job  # re-export for convenience

__all__ = ["process_job"]
