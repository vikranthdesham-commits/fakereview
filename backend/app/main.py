from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.database import engine, Base
from app.routes import review_routes, restaurant_routes, analytics_routes, health_routes
from seed_data import seed_database

# Initialize database tables & seed data on startup
Base.metadata.create_all(bind=engine)
try:
    seed_database()
except Exception as e:
    print(f"Startup Seed Notice: {e}")

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="TrustGuard AI - Full-Stack Investigation System for Detecting Fake Reviews using Explainable AI"
)

# Configure CORS
origins = [o.strip() for o in settings.CORS_ORIGINS.split(",") if o.strip()]
if "*" in origins or not origins:
    origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_routes.router)
app.include_router(review_routes.router)
app.include_router(restaurant_routes.router)
app.include_router(analytics_routes.router)

@app.get("/")
def root():
    return {
        "message": "Welcome to TrustGuard AI - Fake Review Detection Engine",
        "docs": "/docs",
        "status": "operational"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
