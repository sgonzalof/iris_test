from dataclasses import dataclass
from typing import Optional

@dataclass(frozen=True)
class SearchResult:
    title: str
    description: Optional[str]
    url: str