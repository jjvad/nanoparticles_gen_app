from app.models.cvae_pipeline import CVAEPipeline

models = {}

def load_models():
    models["cvae"] = CVAEPipeline.load("/models/cvae_3")

def get_model(name: str):
    return models.get(name)