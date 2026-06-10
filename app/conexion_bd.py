from sqlmodel import SQLmodel, session, create_engine
from typing import Annotated
from fastapi import Depends

#este es el nombre de la base de datos

nombre_bd = "bd_clientes_3407186.sqlite3"

#conexion a la base datos , con una url (direccion)

url_bd = f"sqlite:///{nombre_bd}"


#este es el motor de base de datos 
motor_db = create_engine(url_bd)

#obtener una sesion en la base de datos sqlite

def obtener_sesion():
    with session (motor_db) as mi_sesion:
        yield mi_sesion

#aca se define la dependencia , y esto registra mi sesion 

sesion_dependencia = Annotated(session, Depends(obtener_sesion))

