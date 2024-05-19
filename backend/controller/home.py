from fastapi import APIRouter
from fastapi.responses import FileResponse

router = APIRouter()

@router.get("/home")
async def home():
    return FileResponse("/home/null/code/trading/frontend/index.html")