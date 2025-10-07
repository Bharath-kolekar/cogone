"""
Minimal test server for Smart Coding AI status streaming
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers.smart_coding_ai_status import router as smart_coding_ai_status_router

app = FastAPI(title="Smart Coding AI Test Server")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the Smart Coding AI status router
app.include_router(smart_coding_ai_status_router, tags=["Smart Coding AI Status"])

@app.get("/")
async def root():
    return {"message": "Smart Coding AI Test Server", "status": "healthy"}

@app.get("/health")
async def health():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
