from fastapi import FastAPI
from app import schemas
from app.config import HOST, PORT
from app.crud import create_pedido_producto, update_pedido_producto, update_pedido

app = FastAPI()


@app.post("/create/pedido/")
async def crear_pedido(pedido: schemas.Pedido):
    return await create_pedido_producto(pedido)

@app.put("/update/pedido/{pedido_id}")
async def actualizar_pedido(pedido_id:str, pedido: schemas.Pedido):
    return await update_pedido(pedido_id, pedido)
@app.patch("/update/pedido/producto/{pedido_id}")
async def agregar_producto_a_pedido(pedido_id: str, producto: schemas.Producto):
    return await update_pedido_producto(pedido_id, producto)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=HOST, port=PORT)