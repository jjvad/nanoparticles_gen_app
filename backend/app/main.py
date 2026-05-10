from fastapi import FastAPI
from app.api.generate import router as generate_router


app = FastAPI()

@app.get("/")
def root():
    return {"message": "Nanoparticles generator API"}

app.include_router(generate_router)