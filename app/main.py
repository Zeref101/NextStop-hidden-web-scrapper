from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.places_to_visit import router as placesToVisit_router

app = FastAPI()

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(placesToVisit_router)


@app.get("/")
def read_root():
    return {"Hello": "World"}
