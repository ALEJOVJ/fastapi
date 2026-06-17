from fastapi import FastAPI
from app.enrutador.clientes import ruta_clientes
from app.enrutador.facturas import ruta_facturas
from app.enrutador.transacciones import ruta_transacciones
from.conexion_bd import crear_tablas

from .listas_app import lista_clientes, lista_facturas, lista_transacciones

app = FastAPI(lifespan=crear_tablas)

app.include_router(ruta_clientes, tags=["clientes"])
app.include_router(ruta_facturas, tags=["facturas"])
app.include_router(ruta_transacciones, tags=["transacciones"])










