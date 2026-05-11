from pydantic import BaseModel
from typing import Any


class CSVExportRequest(BaseModel):
    model_used: str
    input_properties: dict[str, Any]
    generated_count: int
    results: list[dict[str, Any]]