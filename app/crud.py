import httpx
from fastapi import HTTPException
from app.config import PEDIDOS_SERVICE_URL, RESENIAS_SERVICE_URL, PRODUCTOS_SERVICE_URL
from app import schemas

async def create_pedido_producto(pedido: schemas.Pedido):
    async with httpx.AsyncClient() as client:
        lista = []
        for p in pedido.productos:
            product_response = await client.get(f"{PRODUCTOS_SERVICE_URL}/{p.id}")

            if product_response.status_code == 200:
                producto_data = product_response.json()
                producto_schema = schemas.Producto(
                    id=producto_data['id'],
                    nombre=producto_data['nombre'],
                    descripcion=producto_data.get('descripcion'),
                    precio=float(producto_data['precio']),
                    cantidad=p.cantidad
                )
                lista.append(producto_schema)
            else:
                raise HTTPException(status_code=404, detail=f"Producto con id {p.id} no encontrado.")

        pedido.productos = lista

        pedido_response = await client.post(PEDIDOS_SERVICE_URL, json=pedido.dict())

        if pedido_response.status_code != 201:
            raise HTTPException(status_code=pedido_response.status_code, detail="Error al procesar el pedido.")

        return {
            "message": "Pedido agregado exitosamente",
            "pedido": pedido_response.json()
        }

async def update_pedido_producto(pedido_id: str, producto: schemas.Producto):
    async with httpx.AsyncClient() as client:
        pedido_response = await client.get(f"{PEDIDOS_SERVICE_URL}/{pedido_id}")
        if pedido_response.status_code != 200:
            raise HTTPException(status_code=pedido_response.status_code, detail="Error al procesar el pedido.")

        product_response = await client.get(f"{PRODUCTOS_SERVICE_URL}/{producto.id}")
        if product_response.status_code != 200:
            raise HTTPException(status_code=404, detail=f"Producto con id {producto.id} no encontrado.")

        productos_actuales = pedido_response.json().get("productos", [])
        producto_data = product_response.json()

        existing_product = next((p for p in productos_actuales if p['id'] == producto_data['id']), None)

        if existing_product:
            existing_product['cantidad'] += producto.cantidad
        else:
            producto_schema = schemas.Producto(
                id=producto_data['id'],
                nombre=producto_data['nombre'],
                descripcion=producto_data.get('descripcion'),
                precio=float(producto_data['precio']),
                cantidad=producto.cantidad
            )
            productos_actuales.append(producto_schema.dict())

        update_response = await client.patch(f"{PEDIDOS_SERVICE_URL}/{pedido_id}/productos", json= productos_actuales)

        if update_response.status_code != 200:
            raise HTTPException(status_code=update_response.status_code, detail="Error al actualizar los productos del pedido.")

        return {
            "message": "Productos actualizados exitosamente",
            "pedido": update_response.json()
        }


async def update_pedido(pedido_id: str, pedido: schemas.Pedido):
    async with httpx.AsyncClient() as client:
        lista = []
        for p in pedido.productos:
            product_response = await client.get(f"{PRODUCTOS_SERVICE_URL}/{p.id}")

            if product_response.status_code == 200:
                producto_data = product_response.json()
                producto_schema = schemas.Producto(
                    id=producto_data['id'],
                    nombre=producto_data['nombre'],
                    descripcion=producto_data.get('descripcion'),
                    precio=float(producto_data['precio']),
                    cantidad=p.cantidad
                )
                lista.append(producto_schema)
            else:
                raise HTTPException(status_code=404, detail=f"Producto con id {p.id} no encontrado.")

        pedido.productos = lista

        pedido_response = await client.put(f"{PEDIDOS_SERVICE_URL}/{pedido_id}", json=pedido.dict())

        if pedido_response.status_code != 200:
            raise HTTPException(status_code=pedido_response.status_code, detail="Error al procesar el pedido.")

        return {
            "message": "Pedido actualizado exitosamente",
            "pedido": pedido_response.json()
        }