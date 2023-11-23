from fastapi import APIRouter, Depends, Form, HTTPException, Request, status, Path
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from models.Evento import Evento
from models.Usuario import Usuario
from repositories.EventoRepo import EventoRepo
from util.security import validar_usuario_logado
from util.template import formatarData


router = APIRouter(prefix="/evento")
templates = Jinja2Templates(directory="templates")

@router.on_event("startup")
async def startup_event():
    templates.env.filters["date"] = formatarData

@router.get("/listagem", response_class=HTMLResponse)
async def getListagem(
    request: Request,
    pa: int = 1,
    tp: int = 3,
    usuario: Usuario = Depends(validar_usuario_logado)
):
    
    eventos = EventoRepo.obterPagina(pa, tp)
    totalPaginas = EventoRepo.obterQtdePaginas(tp)
    return templates.TemplateResponse(
        "evento/listagem.html",
        {
            "request": request,
            "eventos": eventos,
            "totalPaginas": totalPaginas,
            "paginaAtual": pa,
            "tamanhoPagina": tp,
            "usuario": usuario,
        },
    )

@router.get("/novo", response_class=HTMLResponse)
async def getNovo(request: Request, usuario: Usuario = Depends(validar_usuario_logado)):
    if usuario:
        if usuario.admin:
            return templates.TemplateResponse(
                "evento/novo.html", {"request": request, "usuario": usuario}
            )
        else:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    
@router.post("/novo")
async def postNovo(
    request: Request,
    titulo: str = Form(""),
    imagem: str = Form(""),
    descricao: str = Form(""),
    usuario: Usuario = Depends(validar_usuario_logado)
):
    if usuario:
        if usuario.admin:
            EventoRepo.inserir(Evento(0, titulo, imagem, descricao))
            return RedirectResponse(
                "/evento/listagem", status_code=status.HTTP_303_SEE_OTHER
            )
        else:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

@router.get("/excluir/{id:int}", response_class=HTMLResponse)
async def getExcluir(
    request: Request,
    id: int = Path(),
):

    evento = EventoRepo.obterPorId(id)
    return templates.TemplateResponse(
        "evento/excluir.html",
        {"request": request, "evento": evento},
    )


@router.post("/excluir", response_class=HTMLResponse)
async def postExcluir(
    request: Request,
    id: int = Form(0),
):
    if EventoRepo.excluir(id):
        return RedirectResponse(
            "/evento/listagem", status_code=status.HTTP_303_SEE_OTHER
        )
    else:
        raise Exception("Não foi possível excluir o evento.")