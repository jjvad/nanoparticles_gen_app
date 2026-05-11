from fastapi import APIRouter
from fastapi.responses import StreamingResponse

import io
import pandas as pd

from app.schemas.csv_export import CSVExportRequest

router = APIRouter()


def build_filename(properties: dict) -> str:
    parts = []

    for key, value in properties.items():
        parts.append(f"{key}-{value}")

    filename = "_".join(parts)

    # защита от пробелов
    filename = filename.replace(" ", "-")

    return f"{filename}.csv"


@router.post("/generate/csv")
def generate_csv(request: CSVExportRequest):

    rows = []

    for result in request.results:

        row = {
            **request.input_properties,
            **result
        }

        rows.append(row)

    df = pd.DataFrame(rows)

    stream = io.StringIO()
    df.to_csv(stream, index=False)

    filename = build_filename(
        request.input_properties
    )

    response = StreamingResponse(
        iter([stream.getvalue()]),
        media_type="text/csv"
    )

    response.headers["Content-Disposition"] = (
        f'attachment; filename="{filename}"'
    )

    return response