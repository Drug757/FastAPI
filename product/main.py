from fastapi import FastAPI
from database import engine, Base
from routes import products

# Создание таблиц в БД
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Products API",
    description="API для управления каталогом продуктов",
    version="1.0.0"
)

app.include_router(products.router)

@app.get("/")
def root():
    return {"message": "Уалейкума салам", "docs": "/docs"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)