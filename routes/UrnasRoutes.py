from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from util.templateFilters import formatarData


router = APIRouter()

templates = Jinja2Templates(directory="templates")

@router.on_event("startup")
async def startup_event():
    templates.env.filters["date"] = formatarData

@router.get("/urnas")
async def getUrnas(request: Request):
    return templates.TemplateResponse(
        "penacova/urnas.html", { "request": request })

@router.get("/urnabio")
async def getUrnaBio(request: Request):
    return templates.TemplateResponse(
        "penacova/urnabio.html", { "request": request })

@router.get("/urnamadeira")
async def getUrnaMadeira(request: Request):
    return templates.TemplateResponse(
        "penacova/urnamadeira.html", { "request": request })

@router.get("/urnapedra")
async def getUrnaPedra(request: Request):
    return templates.TemplateResponse(
        "penacova/urnapedra.html", { "request": request })

@router.get("/urnabronze")
async def getUrnaBronze(request: Request):
    return templates.TemplateResponse(
        "penacova/urnabronze.html", { "request": request })

@router.get("/urnainox")
async def getUrnaInox(request: Request):
    return templates.TemplateResponse(
        "penacova/urnainox.html", { "request": request })