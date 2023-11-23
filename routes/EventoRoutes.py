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
        },
    )

@router.get("/novo", response_class=HTMLResponse)
async def getNovo(request: Request):
    return templates.TemplateResponse(
        "evento/novo.html", {"request": request}
    )

@router.post("/novo")
async def postNovo(
    request: Request,
    titulo: str = Form(""),
    imagem: str = Form(""),
    descricao: str = Form(""),
):
    EventoRepo.inserir(Evento(0, titulo, imagem, descricao))
    return RedirectResponse(
        "/evento/listagem", status_code=status.HTTP_303_SEE_OTHER
    )

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