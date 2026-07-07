import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import db
from app.controllers import link_controller, category_controller

app = FastAPI()

frontend_url = os.getenv("FRONTEND_URL", "http://localhost:3000")

app.add_middleware(
    CORSMiddleware,
   allow_origins=["http://localhost:3000", frontend_url],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include controllers
app.include_router(link_controller.router)
app.include_router(category_controller.router)


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
