from fastapi import FastAPI
from .routes import router
# from .scheduler import init_scheduler


def create_app() -> FastAPI:
    app = FastAPI(title="Google Trends API", version="0.1.0")

    # inclui as rotas
    app.include_router(router)

    # inicia agendador de tarefas
    # init_scheduler(app)

    return app
