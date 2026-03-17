import random
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET", "OPTIONS"],
    allow_headers=["Content-Type"],
)


@app.get("/api/random")
def get_random():
    try:
        return {"number": random.randint(1, 100)}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
