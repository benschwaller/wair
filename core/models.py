from dataclasses import dataclass, field
from typing import List, Dict, Any


@dataclass
class Agent:
    name: str
    role: str
    model: str
    mission: str
    skills: List[str] = field(default_factory=list)
    sources: List[str] = field(default_factory=list)
    output: str = ""


@dataclass
class Finding:
    title: str
    summary: str
    source: str
    tags: List[str]
    importance: str
    agent: str
    operational_impact: str = ""