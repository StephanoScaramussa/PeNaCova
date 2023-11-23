

from fastapi import APIRouter, Depends, Form, HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from models.Cliente import Cliente
from models.Usuario import Usuario
from repositories.ClienteRepo import ClienteRepo
from util.security import gerar_token, obter_hash_senha, validar_usuario_logado
from util.validators import *

from util.template import capitalizar_nome_proprio, formatarData


router = APIRouter(prefix="/cliente")
templates = Jinja2Templates(directory="templates")

@router.on_event("startup")
async def startup_event():
    templates.env.filters["date"] = formatarData

@router.get("/registro", response_class=HTMLResponse)
async def getRegistro(request: Request, usuario: Usuario = Depends(validar_usuario_logado)):
    return templates.TemplateResponse(
        "cliente/registro.html",
        {"request": request, "usuario": usuario},
    )

# @router.post("/registro_json")
# async def postRegistroJson(
#     nome: str = Form(
#         ..., min_length=3, max_length=50, regex=r"^((\b[A-zÀ-ú']{2,40}\b)\s*){2,}$"
#     ),
#     cpf: str = Form(..., min_length=11, max_length=11, regex=r"^ [0-9]+$"),
#     email: str = Form(
#         ...,
#         regex=r"^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$",
#     ),
#     telefone: str = Form(..., min_length=10, max_length=11, regex=r"^ [0-9]+$"),
#     senha: str = Form(..., min_length=6, max_length=20),
#     confSenha: str = Form(..., min_length=6, max_length=20),
# ):
#     if senha.strip() != confSenha.strip():
#         listaErros = []
#         listaErros.append(
#             {
#                 "type": "field_dont_match",
#                 "loc": ("body", "senha"),
#                 "msg": "Senhas não conferem.",
#             }
#         )
#         listaErros.append(
#             {
#                 "type": "field_dont_match",
#                 "loc": ("body", "confSenha"),
#                 "msg": "Senhas não conferem.",
#             }
#         )
#         raise RequestValidationError(listaErros)
#     ClienteRepo.inserir(
#         Cliente(
#             id=0,
#             nome=nome.strip(),
#             cpf=cpf.strip(),
#             email=email.strip(),
#             telefone=telefone.strip(),
#             senha=senha.strip(),
#         )
#     )
#     return JSONResponse({"ok": True, "returnUrl": "/"}, status_code=status.HTTP_200_OK).

@router.post("/registro")
async def postRegistro(
    request: Request,
    usuario: Usuario = Depends(validar_usuario_logado),
    nome: str = Form(""),
    cpf: str = Form (""),
    email: str = Form(""),  
    senha: str = Form(""),
    telefone: str = Form("")
):
    # normalização dos dados
    nome = capitalizar_nome_proprio(nome).strip()
    cpf = cpf.strip()
    email = email.lower().strip()
    telefone = telefone.strip()
    senha = senha.strip()

    # verificação de erros
    erros = {}
    # validação do campo nome
    is_not_empty(nome, "nome", erros)
    is_person_fullname(nome, "nome", erros)
    # validação do campo cpf
    is_not_empty(cpf, "cpf", erros)
    # validação do campo email
    is_not_empty(email, "email", erros)
    if is_email(email, "email", erros):
        if ClienteRepo.emailExiste(email):
            add_error("email", "Já existe um aluno cadastrado com este e-mail.", erros)
    # validação do campo telefone
    is_not_empty(telefone, "telefone", erros)
    # validação do campo senha
    is_not_empty(senha, "senha", erros)
    is_password(senha, "senha", erros)

    # se tem erro, mostra o formulário novamente
    if len(erros) > 0:
        valores = {}
        valores["nome"] = nome
        valores["cpf"] = cpf
        valores["email"] = email
        valores["telefone"] = telefone
        return templates.TemplateResponse(
            "cliente/registro.html",
            {
                "request": request,
                "usuario": usuario,
                "erros": erros,
                "valores": valores,
            },
        )

    # inserção no banco de dados
    ClienteRepo.inserir(
        Cliente(
            id=0,
            nome=nome,
            cpf=cpf,
            email=email,
            telefone=telefone,
            senha=senha,
        )
    )

    # mostra página de sucesso
    token = gerar_token()
    cliente = ClienteRepo.obterClientePorCPF(cpf)
    ClienteRepo.inserirToken(token, cliente.id)
    response = RedirectResponse("/", status.HTTP_302_FOUND)
    response.set_cookie(key="auth_token", value=token, max_age=1800, httponly=True)
    return response



@router.get("/perfil", response_class=HTMLResponse)
async def getPerfil(
    request: Request, usuario: Usuario = Depends(validar_usuario_logado)
):
            return templates.TemplateResponse(
                "cliente/perfil.html",
                {"request": request, "usuario": usuario},
            )