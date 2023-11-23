from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates
from models.Usuario import Usuario
from util.security import validar_usuario_logado
from util.templateFilters import formatarData


router = APIRouter()

templates = Jinja2Templates(directory="templates")

@router.on_event("startup")
async def startup_event():
    templates.env.filters["date"] = formatarData

@router.get("/urnas")
async def getUrnas(request: Request, usuario: Usuario = Depends(validar_usuario_logado)):
    return templates.TemplateResponse(
        "penacova/urnas.html", { "request": request, "usuario": usuario,})

@router.get("/urnabio")
async def getUrnaBio(request: Request, usuario: Usuario = Depends(validar_usuario_logado)):
    return templates.TemplateResponse(
        "penacova/urnabio.html", { "request": request, "usuario": usuario, })

@router.get("/urnamadeira")
async def getUrnaMadeira(request: Request, usuario: Usuario = Depends(validar_usuario_logado)):
    return templates.TemplateResponse(
        "penacova/urnamadeira.html", { "request": request, "usuario": usuario, })

@router.get("/urnapedra")
async def getUrnaPedra(request: Request, usuario: Usuario = Depends(validar_usuario_logado)):
    return templates.TemplateResponse(
        "penacova/urnapedra.html", { "request": request, "usuario": usuario, })

@router.get("/urnabronze")
async def getUrnaBronze(request: Request, usuario: Usuario = Depends(validar_usuario_logado)):
    return templates.TemplateResponse(
        "penacova/urnabronze.html", { "request": request, "usuario": usuario, })

@router.get("/urnainox")
async def getUrnaInox(request: Request, usuario: Usuario = Depends(validar_usuario_logado)):
    return templates.TemplateResponse(
        "penacova/urnainox.html", { "request": request, "usuario": usuario, })