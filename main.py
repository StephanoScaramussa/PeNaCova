from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import uvicorn
from repositories.ClienteRepo import ClienteRepo
from repositories.EventoRepo import EventoRepo
from routes.MainRoutes import router as mainRouter
from routes.EventoRoutes import router as eventoRouter
from routes.PlanosRoutes import router as planosRouter
from routes.UrnasRoutes import router as urnasRouter
from routes.FloresRoutes import router as floresRouter
from routes.ApoioRoutes import router as apoioRouter
from routes.ClienteRoutes import router as clienteRouter

#ClienteRepo.criarTabela()
#ClienteRepo.criarUsuarioAdmin()
#EventoRepo.criarTabela()

app = FastAPI()

app.mount(path="/static", app=StaticFiles(directory="static"), name="static")

app.include_router(mainRouter)
app.include_router(eventoRouter)
app.include_router(planosRouter)
app.include_router(floresRouter)
app.include_router(urnasRouter)
app.include_router(apoioRouter)
app.include_router(clienteRouter)

# if __name__ == "__main__":
#     uvicorn.run(app="main:app", reload=True) #!!!!!!!!!!!!!!!!!!!!!!!!