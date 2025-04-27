

from fastapi import APIRouter, Request, HTTPException, Depends
from fastapi.responses import JSONResponse
from auth import verify_token

router = APIRouter()

# In-memory store (you can replace with database later)
proxy_data_store = {}

@router.post("/proxy/update")
async def update_proxy_metrics(request: Request, token: str = Depends(verify_token)):
    try:
        data = await request.json()
        proxy_name = data.get("proxy", "default")
        proxy_data_store[proxy_name] = data
        return {"status": "received"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/proxy/data")
async def get_proxy_data(token: str = Depends(verify_token)):
    return JSONResponse(content=proxy_data_store)