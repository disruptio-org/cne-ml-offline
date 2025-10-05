"""Worker pipeline package exposing the document processing entrypoint."""

from .pipeline import process_job

__all__ = ["process_job"]
