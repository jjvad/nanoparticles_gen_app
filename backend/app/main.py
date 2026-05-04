from fastapi import FastAPI
from app.core.model_loader import load_models
from app.api.generate import router as generate_router


app = FastAPI()

@app.on_event("startup")
def startup():
    load_models()

@app.get("/")
def root():
    return {"message": "Nanoparticles generator API"}

app.include_router(generate_router)