from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.endpoints import vision_mentor, knowledge_curator, creative_artisan, user_profile

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Set all CORS enabled origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(vision_mentor.router, prefix=f"{settings.API_V1_STR}/vision", tags=["Vision Mentor"])
app.include_router(knowledge_curator.router, prefix=f"{settings.API_V1_STR}/knowledge", tags=["Knowledge Curator"])
app.include_router(creative_artisan.router, prefix=f"{settings.API_V1_STR}/creative", tags=["Creative Artisan"])
app.include_router(user_profile.router, prefix=f"{settings.API_V1_STR}/user", tags=["User Profile"])

@app.get("/")
def root():
    return {"message": "Welcome to Digital Inheritor API"}
