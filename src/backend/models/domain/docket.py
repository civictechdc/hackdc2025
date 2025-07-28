"""This module defines the Docket model used in the regulations-llm application."""

from dataclasses import dataclass
from typing import Optional


@dataclass
class Docket:
    """Represents a docket with its ID, title, summary, and optional keywords."""
    docket_id: int
    title: str
    summary: str
    keywords: Optional[set[str]] = None
