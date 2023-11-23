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
    
@router.get("/flores")
async def getFlores(request: Request, usuario: Usuario = Depends(validar_usuario_logado)):
    return templates.TemplateResponse(
        "penacova/flores.html", { "request": request, "usuario" : usuario })