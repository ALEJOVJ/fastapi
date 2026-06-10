from fastapi import FastAPI
from fastapi.responses import JSONResponse
from app.modelo.clientes import Clientes, ClientesCrear, ClientesEditar
from app.modelo.facturas import Factura, FacturaCrear, FacturaEditar
from app.modelo.transacciones import Transacciones, TransaccionesCrear, TransaccionesEditar
from app.enrutador import clientes, facturas, transacciones
from .listas_app import lista_clientes, lista_facturas, lista_transacciones

app = FastAPI()

app.include_router(clientes.ruta_clientes, tags=["clientes"])
app.include_router(facturas.ruta_facturas, tags=["facturas"])
app.include_router(transacciones.ruta_transacciones, tags=["transacciones"])










