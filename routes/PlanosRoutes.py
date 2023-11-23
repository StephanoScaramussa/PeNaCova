from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from util.templateFilters import formatarData


router = APIRouter()

templates = Jinja2Templates(directory="templates")

@router.on_event("startup")
async def startup_event():
    templates.env.filters["date"] = formatarData


@router.get("/planos")
async def getPlanos(request: Request):
    return templates.TemplateResponse(
        "penacova/planos.html", { "request": request })

@router.get("/plano1")
async def getPlano1(request: Request):
    return templates.TemplateResponse(
        "penacova/plano1.html", { "request": request })

@router.get("/plano2")
async def getPlano2(request: Request):
    return templates.TemplateResponse(
        "penacova/plano2.html", { "request": request })

@router.get("/plano3")
async def getPlano3(request: Request):
    return templates.TemplateResponse(
        "penacova/plano3.html", { "request": request })