from app.models.cvae_pipeline import CVAEPipeline

loaded_models = {}


def get_model(model_path: str):
    if model_path not in loaded_models:
        loaded_models[model_path] = CVAEPipeline.load(model_path)

    return loaded_models[model_path]