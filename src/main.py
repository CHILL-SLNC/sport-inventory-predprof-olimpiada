from fastapi import FastAPI
from asyncio import run
from src.router import router as my_router
from fastapi.middleware.cors import CORSMiddleware
from src.config import settings

# Инициализация Fastapi-приложения и добавления эндпоинтов из файла router.py.
app = FastAPI()

app.include_router(my_router)

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
