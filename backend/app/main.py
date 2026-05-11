from fastapi import FastAPI
from app.api.generate import router as generate_router
from app.api.generate_csv import router as csv_router
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Nanoparticles generator API"}

app.include_router(generate_router)
app.include_router(csv_router)