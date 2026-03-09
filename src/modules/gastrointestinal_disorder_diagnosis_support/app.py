# app.py
"""
FastAPI main application
Serves as backend API for the gastrointestinal module
Also serves frontend via Streamlit
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os
from dotenv import load_dotenv

# Import routes
from routes import symptom_router

load_dotenv()

# Create FastAPI app
app = FastAPI(
    title="GI Disorder Diagnosis API",
    description="API for gastrointestinal disorder diagnosis support",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(symptom_router)

# Health check endpoint
@app.get("/health")
def health_check():
    """Check if API is running"""
    return {"status": "API is running"}

@app.get("/")
def root():
    """Root endpoint"""
    return {"message": "GI Disorder Diagnosis API"}

if __name__ == "__main__":
    # Run: uvicorn app:app --reload
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
