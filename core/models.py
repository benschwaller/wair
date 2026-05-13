from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from datetime import datetime


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
class Source:
    name: str
    url: str
    type: str
    credibility_score: float = 0.5
    last_verified: Optional[datetime] = None
    is_active: bool = True
    description: str = ""
    topics: List[str] = field(default_factory=list)


@dataclass
class Finding:
    title: str
    summary: str
    source: str
    source_url: str = ""
    tags: List[str] = field(default_factory=list)
    importance: str = ""
    agent: str = ""
    operational_impact: str = ""
    published_date: Optional[str] = None
    credibility_score: float = 0.5
    citation: str = ""