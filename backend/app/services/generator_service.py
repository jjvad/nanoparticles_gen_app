from app.core.model_loader import get_model

def generate(properties: dict):
    # пока у тебя одна модель
    model = get_model("cvae")

    if model is None:
        raise ValueError("Model not loaded")

    result = model.generate(properties)

    return result