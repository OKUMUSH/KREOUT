from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

from routes import status_routes, control_routes

app = FastAPI()

app.include_router(status_routes, prefix="/status")
app.include_router(control_routes, prefix="/control")

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})