from sqlmodel import SQLModel, Session, create_engine
from typing import Annotated
from fastapi import FastAPI , Depends

#este es el nombre de la base de datos

nombre_bd = "bd_clientes_3407186.sqlite3"

#conexion a la base datos , con una url (direccion)

url_bd = f"sqlite:///{nombre_bd}"


#este es el motor de base de datos 
motor_bd = create_engine(url_bd)

#definir un metodo  para crear las tablas

def crear_tablas(app: FastAPI):
    SQLModel.metadata.create_all(motor_bd)
    yield

#obtener una sesion en la base de datos sqlite

def obtener_sesion():
    with Session (motor_bd) as mi_sesion:
        yield mi_sesion # retorna la session 

#aca se define la dependencia , y esto registra mi sesion 

sesion_dependencia = Annotated[Session, Depends(obtener_sesion)]

