import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import db
from app.routers import links, categories

app = FastAPI()

frontend_url = os.getenv("FRONTEND_URL", "http://localhost:3000")

app.add_middleware(
    CORSMiddleware,
   allow_origins=["http://localhost:3000", frontend_url],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(links.router)
app.include_router(categories.router)


@app.on_event("startup")
async def startup():
    # Test MongoDB connection
    try:
        await db.command("ping")
        print("Connected to MongoDB!")
    except Exception as e:
        print(f"MongoDB connection failed: {e}")


@app.get("/")
def read_root():
    return {"message": "Hello World"}
