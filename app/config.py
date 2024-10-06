
import os
PRODUCTOS_SERVICE_URL = "http://localhost:8000/productos"
PEDIDOS_SERVICE_URL = "http://localhost:8080/pedido"
RESENIAS_SERVICE_URL = "http://localhost:8003/resenias"



PORT = int(os.getenv("PORT", 8001))
HOST = os.getenv("HOST", "0.0.0.0")