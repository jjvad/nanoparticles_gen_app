from pydantic import BaseModel
from typing import Dict, Any, List

class GenerateRequest(BaseModel):
    properties: Dict[str, Any]

class GenerateResponse(BaseModel):
    results: List[Dict[str, Any]]
    model_used: str