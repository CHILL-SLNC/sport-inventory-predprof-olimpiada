from fastapi import FastAPI
from src.routers.auth_router import auth_router
from src.routers.inventory_router import router as inventory_router
from src.routers.user_router import router as user_router
from src.routers.admin_router import router as admin_router
from fastapi.middleware.cors import CORSMiddleware
from src.config import settings

# Инициализация Fastapi-приложения и добавления эндпоинтов из файла inventory_router.py.
app = FastAPI()

app.include_router(auth_router)
app.include_router(inventory_router)
app.include_router(user_router)
app.include_router(admin_router)


# Преодоление ошибки CORS.
frontPort = settings.FRONT_PORT

origins = [
    f"http://127.0.0.1:{frontPort}",
    f"http://localhost:{frontPort}",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
