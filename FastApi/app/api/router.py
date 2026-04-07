from fastapi import APIRouter, Depends, BackgroundTasks, WebSocket, WebSocketDisconnect
from typing import List
from app.schemas.product import ProductCreate, ProductResponse
from app.core.deps import get_token_header
from app.services.actions import generate_inventory_report, calculate_sku

# 4. APIRouter: Группировка эндпоинтов
router = APIRouter(prefix="/products", tags=["Inventory"])

# Хранилище в памяти для примера
db_mock = []

@router.post("/", response_model=ProductResponse, dependencies=[Depends(get_token_header)])
async def create_product(product: ProductCreate, bg_tasks: BackgroundTasks):
    """Создание товара с фоновой задачей."""
    new_id = len(db_mock) + 1
    sku = calculate_sku(product.name, product.category)
    
    product_data = product.model_dump()
    result = {**product_data, "id": new_id, "sku": sku}
    db_mock.append(result)
    
    # 5. Background Tasks: Запуск задачи после возврата ответа пользователю
    bg_tasks.add_task(generate_inventory_report, product.name)
    return result

@router.get("/", response_model=List[ProductResponse])
async def list_products(limit: int = 10, offset: int = 0):
    return db_mock[offset : offset + limit]

# 6. WebSockets: Живой мониторинг склада
@router.websocket("/ws/monitor")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            # Имитация отправки данных о нагрузке склада каждые 2 сек
            await asyncio.sleep(2)
            await websocket.send_json({"active_items": len(db_mock), "status": "online"})
    except WebSocketDisconnect:
        print("Client disconnected from WebSocket")
