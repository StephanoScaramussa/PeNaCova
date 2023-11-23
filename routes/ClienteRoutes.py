

from fastapi import APIRouter, Depends, Form, HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from models.Cliente import Cliente
from models.Usuario import Usuario
from repositories.ClienteRepo import ClienteRepo
from util.security import gerar_token, obter_hash_senha, validar_usuario_logado, verificar_senha
from util.validators import *

from util.template import capitalizar_nome_proprio, formatarData


router = APIRouter(prefix="/cliente")
templates = Jinja2Templates(directory="templates")
#!!!!!!!!!!!!!

@router.on_event("startup")
async def startup_event():
    templates.env.filters["date"] = formatarData

@router.get("/registro", response_class=HTMLResponse)
async def getRegistro(request: Request, usuario: Usuario = Depends(validar_usuario_logado)):
    return templates.TemplateResponse(
        "cliente/registro.html",
        {"request": request, "usuario": usuario},
    )

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
    if is_cpf(cpf, "cpf", erros):
        if ClienteRepo.cpfExiste(cpf):
            add_error("cpf", "Já existe um cliente cadastrado com este cpf.", erros)
    # validação do campo email
    is_not_empty(email, "email", erros)
    if is_email(email, "email", erros):
        if ClienteRepo.emailExiste(email):
            add_error("email", "Já existe um cliente cadastrado com este e-mail.", erros)
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
            senha=obter_hash_senha(senha),
        )
    )

    # mostra página de sucesso
    # token = gerar_token()
    # cliente = ClienteRepo.obterClientePorCPF(cpf)
    # ClienteRepo.inserirToken(token, cliente.id)
    # response = RedirectResponse("/", status.HTTP_302_FOUND)
    # response.set_cookie(key="auth_token", value=token, max_age=1800, httponly=True)
    # return response
    return templates.TemplateResponse(
        "main/index.html",
        {"request": request, "usuario": usuario},
    )



@router.get("/perfil", response_class=HTMLResponse)
async def getPerfil(
    request: Request, usuario: Usuario = Depends(validar_usuario_logado)
):
    if usuario:
        cliente = ClienteRepo.obterPorId(usuario.id)
        if cliente:
            return templates.TemplateResponse(
                "cliente/perfil.html",
                {"request": request, "usuario": usuario, "cliente": cliente},
            )
        else:
            return RedirectResponse("/", status_code=status.HTTP_303_SEE_OTHER)
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


@router.get("/alterarsenha", response_class=HTMLResponse)
async def getAlterarSenha(
    request: Request, usuario: Usuario = Depends(validar_usuario_logado)
):
    if usuario:
        return templates.TemplateResponse(
            "cliente/alterarsenha.html", {"request": request, "usuario": usuario}
        )
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


@router.post("/alterarsenha", response_class=HTMLResponse)
async def postAlterarSenha(
    request: Request,
    usuario: Usuario = Depends(validar_usuario_logado),
    senhaAtual: str = Form(""),
    novaSenha: str = Form(""),
    confNovaSenha: str = Form(""),    
):
    # normalização dos dados
    senhaAtual = senhaAtual.strip()
    novaSenha = novaSenha.strip()
    confNovaSenha = confNovaSenha.strip()    

    # verificação de erros
    erros = {}
    # validação do campo senhaAtual
    is_not_empty(senhaAtual, "senhaAtual", erros)
    is_password(senhaAtual, "senhaAtual", erros)    
    # validação do campo novaSenha
    is_not_empty(novaSenha, "novaSenha", erros)
    is_password(novaSenha, "novaSenha", erros)
    # validação do campo confNovaSenha
    is_not_empty(confNovaSenha, "confNovaSenha", erros)
    is_matching_fields(confNovaSenha, "confNovaSenha", novaSenha, "Nova Senha", erros)
    
    # só verifica a senha no banco de dados se não houverem erros de validação
    if len(erros) == 0:    
        hash_senha_bd = ClienteRepo.obterSenhaDeEmail(usuario.email)
        if hash_senha_bd:
            if not verificar_senha(senhaAtual, hash_senha_bd):            
                add_error("senhaAtual", "Senha atual está incorreta.", erros)
    
    # se tem erro, mostra o formulário novamente
    if len(erros) > 0:
        valores = {}        
        return templates.TemplateResponse(
            "cliente/alterarsenha.html",
            {
                "request": request,
                "usuario": usuario,                
                "erros": erros,
                "valores": valores,
            },
        )

    # se passou pelas validações, altera a senha no banco de dados
    hash_nova_senha = obter_hash_senha(novaSenha)
    ClienteRepo.alterarSenha(usuario.id, hash_nova_senha)
    
    # mostra página de sucesso
    return templates.TemplateResponse(
        "main/index.html",
        {"request": request, "usuario": usuario},
    )

@router.get("/alterarnome", response_class=HTMLResponse)
async def getAlterarNome(
    request: Request, usuario: Usuario = Depends(validar_usuario_logado)
):
    if usuario:
        return templates.TemplateResponse(
            "cliente/alterarnome.html", {"request": request, "usuario": usuario}
        )
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


@router.post("/alterarnome", response_class=HTMLResponse)
async def postAlterarNome(
    request: Request,
    usuario: Usuario = Depends(validar_usuario_logado),
    novoNome: str = Form(""),
    confNovoNome: str = Form(""),    
):
    # normalização dos dados
    novoNome = novoNome.strip()
    confNovoNome = confNovoNome.strip()    

    # verificação de erros
    erros = {}
    # validação do campo novoNome
    is_not_empty(novoNome, "novoNome", erros)
    is_person_fullname(novoNome, "novoNome", erros)
    # validação do campo confNovoNome
    is_not_empty(confNovoNome, "confNovoNome", erros)
    is_matching_fields(confNovoNome, "confNovoNome", novoNome, "Novo Nome", erros)
    
    # se tem erro, mostra o formulário novamente
    if len(erros) > 0:
        valores = {}        
        return templates.TemplateResponse(
            "cliente/alterarnome.html",
            {
                "request": request,
                "usuario": usuario,                
                "erros": erros,
                "valores": valores,
            },
        )

    # se passou pelas validações, altera a senha no banco de dados
    ClienteRepo.alterarNome(usuario.id, novoNome)
    
    # mostra página de sucesso
    return templates.TemplateResponse(
        "main/index.html",
        {"request": request, "usuario": usuario},
    )

@router.get("/alterarcpf", response_class=HTMLResponse)
async def getAlterarCPF(
    request: Request, usuario: Usuario = Depends(validar_usuario_logado)
):
    if usuario:
        return templates.TemplateResponse(
            "cliente/alterarcpf.html", {"request": request, "usuario": usuario}
        )
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


@router.post("/alterarcpf", response_class=HTMLResponse)
async def postAlterarCPF(
    request: Request,
    usuario: Usuario = Depends(validar_usuario_logado),
    novoCPF: str = Form(""),
    confNovoCPF: str = Form(""),    
):
    # normalização dos dados
    novoCPF = novoCPF.strip()
    confNovoCPF = confNovoCPF.strip()    

    # verificação de erros
    erros = {}
    # validação do campo novoCPF
    is_not_empty(novoCPF, "novoCPF", erros)
    if is_cpf(novoCPF, "novoCPF", erros):
        if ClienteRepo.cpfExiste(novoCPF):
            add_error("novoCPF", "Já existe um cliente cadastrado com este cpf.", erros)
    # validação do campo confNovoCPF
    is_not_empty(confNovoCPF, "confNovoCPF", erros)
    is_matching_fields(confNovoCPF, "confNovoCPF", novoCPF, "Novo CPF", erros)
    
    # se tem erro, mostra o formulário novamente
    if len(erros) > 0:
        valores = {}        
        return templates.TemplateResponse(
            "cliente/alterarcpf.html",
            {
                "request": request,
                "usuario": usuario,                
                "erros": erros,
                "valores": valores,
            },
        )

    # se passou pelas validações, altera a senha no banco de dados
    ClienteRepo.alterarCPF(usuario.id, novoCPF)
    
    # mostra página de sucesso
    return templates.TemplateResponse(
        "main/index.html",
        {"request": request, "usuario": usuario},
    )

@router.get("/alteraremail", response_class=HTMLResponse)
async def getAlterarEmail(
    request: Request, usuario: Usuario = Depends(validar_usuario_logado)
):
    if usuario:
        return templates.TemplateResponse(
            "cliente/alteraremail.html", {"request": request, "usuario": usuario}
        )
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


@router.post("/alteraremail", response_class=HTMLResponse)
async def postAlterarEmail(
    request: Request,
    usuario: Usuario = Depends(validar_usuario_logado),
    novoEmail: str = Form(""),
    confNovoEmail: str = Form(""),    
):
    # normalização dos dados
    novoEmail = novoEmail.strip()
    confNovoEmail = confNovoEmail.strip()    

    # verificação de erros
    erros = {}
    # validação do campo novoEmail
    is_not_empty(novoEmail, "novoEmail", erros)
    if is_email(novoEmail, "novoEmail", erros):
        if ClienteRepo.emailExiste(novoEmail):
            add_error("novoEmail", "Já existe um cliente cadastrado com este e-mail.", erros)
    # validação do campo confNovoEmail
    is_not_empty(confNovoEmail, "confNovoEmail", erros)
    is_matching_fields(confNovoEmail, "confNovoEmail", novoEmail, "Novo Email", erros)
    
    # se tem erro, mostra o formulário novamente
    if len(erros) > 0:
        valores = {}        
        return templates.TemplateResponse(
            "cliente/alteraremail.html",
            {
                "request": request,
                "usuario": usuario,                
                "erros": erros,
                "valores": valores,
            },
        )

    # se passou pelas validações, altera a senha no banco de dados
    ClienteRepo.alterarEmail(usuario.id, novoEmail)
    
    # mostra página de sucesso
    return templates.TemplateResponse(
        "main/index.html",
        {"request": request, "usuario": usuario},
    )

@router.get("/alterartelefone", response_class=HTMLResponse)
async def getAlterarTelefone(
    request: Request, usuario: Usuario = Depends(validar_usuario_logado)
):
    if usuario:
        return templates.TemplateResponse(
            "cliente/alterartelefone.html", {"request": request, "usuario": usuario}
        )
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


@router.post("/alterartelefone", response_class=HTMLResponse)
async def postAlterarTelefone(
    request: Request,
    usuario: Usuario = Depends(validar_usuario_logado),
    novoTelefone: str = Form(""),
    confNovoTelefone: str = Form(""),    
):
    # normalização dos dados
    novoTelefone = novoTelefone.strip()
    confNovoTelefone = confNovoTelefone.strip()    

    # verificação de erros
    erros = {}
    # validação do campo novoTelefone
    is_not_empty(novoTelefone, "novoTelefone", erros)
    # validação do campo confNovoTelefone
    is_not_empty(confNovoTelefone, "confNovoTelefone", erros)
    is_matching_fields(confNovoTelefone, "confNovoTelefone", novoTelefone, "Novo Telefone", erros)
    
    # se tem erro, mostra o formulário novamente
    if len(erros) > 0:
        valores = {}        
        return templates.TemplateResponse(
            "cliente/alterartelefone.html",
            {
                "request": request,
                "usuario": usuario,                
                "erros": erros,
                "valores": valores,
            },
        )

    # se passou pelas validações, altera a senha no banco de dados
    ClienteRepo.alterarTelefone(usuario.id, novoTelefone)
    
    # mostra página de sucesso
    return templates.TemplateResponse(
        "main/index.html",
        {"request": request, "usuario": usuario},
    )