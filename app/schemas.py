from typing import Optional, List

from pydantic import BaseModel

class Producto(BaseModel):
    id: int
    nombre: str
    descripcion:Optional[str]=None
    precio: float
    cantidad: int

class Cliente(BaseModel):
    nombre: str
    correoElectronico: str
    telefono: str

class Pedido(BaseModel):
    descripcion: str
    productos: List[Producto]
    cliente: Cliente