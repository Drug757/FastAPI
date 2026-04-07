import asyncio

# 3. BackgroundTasks: Имитация тяжелой операции (генерация отчета)
async def generate_inventory_report(product_name: str):
    await asyncio.sleep(5) # Имитация долгой работы
    print(f"[REPORT] Отчет для товара '{product_name}' готов и отправлен в архив.")

def calculate_sku(name: str, category: str) -> str:
    return f"{category[:3].upper()}-{name[:3].upper()}-001"
