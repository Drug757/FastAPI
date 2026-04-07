import time
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.api.router import router

# 7. Lifespan: Управление ресурсами при старте и выключении
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("[STARTUP] Подключение к виртуальной БД...")
    yield
    print("[SHUTDOWN] Очистка ресурсов...")

app = FastAPI(title="AsyncWarehouse API", lifespan=lifespan)

# 8. Middleware: Замер времени обработки каждого запроса
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response

# 9. Custom Exception Handler
@app.exception_handler(ValueError)
async def value_error_handler(request: Request, exc: ValueError):
    return JSONResponse(
        status_code=400,
        content={"message": f"Ошибка валидации данных: {str(exc)}"},
    )

app.include_router(router)
