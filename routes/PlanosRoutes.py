from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from models.Usuario import Usuario
from util.security import validar_usuario_logado
from util.templateFilters import formatarData


router = APIRouter()

templates = Jinja2Templates(directory="templates")

@router.on_event("startup")
async def startup_event():
    templates.env.filters["date"] = formatarData


@router.get("/planos")
async def getPlanos(request: Request, usuario: Usuario = Depends(validar_usuario_logado)):
    return templates.TemplateResponse(
        "penacova/planos.html", { "request": request, "usuario" : usuario })

@router.get("/plano1")
async def getPlano1(request: Request, usuario: Usuario = Depends(validar_usuario_logado)):
    return templates.TemplateResponse(
        "penacova/plano1.html", { "request": request, "usuario" : usuario })

@router.get("/plano2")
async def getPlano2(request: Request, usuario: Usuario = Depends(validar_usuario_logado)):
    return templates.TemplateResponse(
        "penacova/plano2.html", { "request": request, "usuario" : usuario })

@router.get("/plano3")
async def getPlano3(request: Request, usuario: Usuario = Depends(validar_usuario_logado)):
    return templates.TemplateResponse(
        "penacova/plano3.html", { "request": request, "usuario" : usuario })

@router.get("/plano1pagar")
async def getPlano3(request: Request, usuario: Usuario = Depends(validar_usuario_logado)):
    if usuario:
        return templates.TemplateResponse(
            "penacova/plano1pagar.html", { "request": request, "usuario" : usuario })
    else:
        return RedirectResponse("/login")

@router.get("/plano2pagar")
async def getPlano3(request: Request, usuario: Usuario = Depends(validar_usuario_logado)):
    if usuario:
        return templates.TemplateResponse(
            "penacova/plano2pagar.html", { "request": request, "usuario" : usuario })
    else:
        return RedirectResponse("/login")

@router.get("/plano3pagar")
async def getPlano3(request: Request, usuario: Usuario = Depends(validar_usuario_logado)):
    if usuario:
        return templates.TemplateResponse(
            "penacova/plano3pagar.html", { "request": request, "usuario" : usuario })
    else:
        return RedirectResponse("/login")