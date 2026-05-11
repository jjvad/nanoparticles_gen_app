from fastapi import APIRouter

from app.schemas.generate import (
    GenerateRequest,
    GenerateResponse
)

from app.services.generator_service import generate

router = APIRouter()


@router.post(
    "/generate",
    response_model=GenerateResponse
)
def generate_endpoint(request: GenerateRequest):

    result = generate(
        request.properties,
        request.n_samples
    )

    return result