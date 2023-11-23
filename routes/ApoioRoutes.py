from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from util.templateFilters import formatarData


router = APIRouter()

templates = Jinja2Templates(directory="templates")

@router.on_event("startup")
async def startup_event():
    templates.env.filters["date"] = formatarData
    
@router.get("/apoios")
async def getApoio(request: Request):
    return templates.TemplateResponse(
        "penacova/apoios.html", { "request": request })