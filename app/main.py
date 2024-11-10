from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from app.routes.places_to_visit import router as placesToVisit_router
from app.routes.food import router as food_router
from app.routes.best_time import router as best_time_router

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
app.include_router(food_router)
app.include_router(best_time_router)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    print("Server has started, waiting for requests...")
    print(f"Incoming request: {request.method} {request.url}")
    response = await call_next(request)
    return response


@app.get("/")
def read_root():
    return {"Hello": "World"}
