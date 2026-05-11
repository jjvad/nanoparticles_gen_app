from pydantic import BaseModel
from typing import Dict, Any, List

class GenerateRequest(BaseModel):
    properties: dict
    n_samples: int = 1

class GenerateResponse(BaseModel):
    model_used: str
    input_properties: dict
    generated_count: int
    results: list[dict[str, Any]]