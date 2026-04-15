from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Optional


class Category(str, Enum):
    ALGORITHM = "algorithm"
    PATTERN = "pattern"
    CS = "cs"


class Subject(str, Enum):
    SW_DESIGN = "sw_design"
    DATABASE = "database"
    OPERATING_SYSTEM = "operating_system"
    NETWORK = "network"
    SECURITY = "security"


class CodeLanguage(str, Enum):
    PYTHON = "python"
    DART = "dart"


@dataclass
class KnowledgeItem:
    id: int
    category: Category
    subject: Optional[Subject]
    title: str
    summary: str
    code_snippet: Optional[str]
    code_language: Optional[CodeLanguage]
    needs_review: bool
