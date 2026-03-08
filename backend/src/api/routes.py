from fastapi import APIRouter, UploadFile, File, HTTPException
from typing import Optional
from .models import UploadResponse, ResultsResponse, StartOptimizationRequest
from ..config import settings
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api", tags=["api"])

# Global engine reference (set by server.py)
engine = None

@router.post("/upload", response_model=UploadResponse)
async def upload_data(file: UploadFile = File(...)):
    """Upload CSV data file"""
    try:
        if file.size > settings.MAX_UPLOAD_SIZE:
            raise HTTPException(status_code=413, detail="File too large")
        
        # Save file
        filepath = settings.UPLOAD_DIR / file.filename
        contents = await file.read()
        with open(filepath, "wb") as f:
            f.write(contents)
        
        return UploadResponse(
            filename=file.filename,
            size=len(contents),
            status="success"
        )
    
    except Exception as e:
        logger.error(f"Upload error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/start")
async def start_optimization(request: StartOptimizationRequest):
    """Start optimization or live mode"""
    try:
        return {
            "status": "simulation_started",
            "mode": request.mode,
            "strategies": request.strategies
        }
    except Exception as e:
        logger.error(f"Start error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/results", response_model=ResultsResponse)
async def get_results():
    """Get final simulation results"""
    try:
        if engine is None:
            raise HTTPException(status_code=400, detail="No active simulation")
        
        results = engine.get_results()
        return ResultsResponse(**results)
    
    except Exception as e:
        logger.error(f"Results error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "version": "1.0.0"}
