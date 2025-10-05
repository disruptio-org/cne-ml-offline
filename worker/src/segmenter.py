"""Segmentation step: split OCR text into candidate line segments."""
from __future__ import annotations

from typing import Iterable, List

from .types import OCRPage


def segment_pages(pages: Iterable[OCRPage]) -> List[str]:
    segments: List[str] = []
    for page in pages:
        for raw_line in page.text.splitlines():
            line = raw_line.strip()
            if line:
                segments.append(line)
    return segments
