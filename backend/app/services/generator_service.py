from app.core.model_selector import select_model_path
from app.core.model_loader import get_model


def generate(properties: dict, n_samples: int):
    model_path = select_model_path(properties)

    model = get_model(model_path)

    result = model.generate(
        properties,
        n_samples=n_samples
    )

    return {
        "model_used": model_path,
        "input_properties": properties,
        "generated_count": n_samples,
        "results": result
    }