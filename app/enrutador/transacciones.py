from fastapi import APIRouter
from app.modelo.transacciones import (Transacciones, TransaccionesCrear, TransaccionesEditar)
from app.modelo.facturas import Factura
from app.conexion_bd import sesion_dependencia
from sqlmodel import select

ruta_transacciones = APIRouter()


# listar todas las transacciones
@ruta_transacciones.get(
    "/transacciones",
    response_model=list[Transacciones]
)
async def listar_transacciones(
    sesion: sesion_dependencia
):
    consulta = select(Transacciones)
    lista_transacciones = sesion.exec(consulta).all()
    return lista_transacciones


# obtener una transacción por id
@ruta_transacciones.get("/transacciones/{id}")
async def obtener_transaccion(
    id: int,
    sesion: sesion_dependencia
):
    transaccion = sesion.get(Transacciones, id)

    if not transaccion:
        return {
            "mensaje": "Transacción no encontrada"
        }

    return transaccion


# crear una transacción
@ruta_transacciones.post("/transacciones/{factura_id}")
async def crear_transaccion(
    factura_id: int,
    datos_transaccion: TransaccionesCrear,
    sesion: sesion_dependencia
):
    # validar si existe la factura
    factura_encontrada = sesion.get(
        Factura,
        factura_id
    )

    if not factura_encontrada:
        return {
            "mensaje": "Factura no encontrada"
        }

    # convertir datos a diccionario
    transaccion_dict = datos_transaccion.model_dump()

    # agregar factura_id
    transaccion_dict["factura_id"] = factura_id

    # validar y crear modelo
    transaccion_val = Transacciones.model_validate(
        transaccion_dict
    )

    # guardar en bd
    sesion.add(transaccion_val)
    sesion.commit()
    sesion.refresh(transaccion_val)

    return {
        "mensaje": "Transacción creada",
        "transaccion": transaccion_val
    }


# editar una transacción
@ruta_transacciones.put("/transacciones/{id}")
async def editar_transaccion(
    id: int,
    datos_transaccion: TransaccionesEditar,
    sesion: sesion_dependencia
):
    transaccion = sesion.get(
        Transacciones,
        id
    )

    if not transaccion:
        return {
            "mensaje": "Transacción no encontrada"
        }

    # actualizar datos
    transaccion.cantidad = datos_transaccion.cantidad
    transaccion.vr_unitario = datos_transaccion.vr_unitario
    transaccion.descripcion = datos_transaccion.descripcion

    # guardar cambios
    sesion.add(transaccion)
    sesion.commit()
    sesion.refresh(transaccion)

    return {
        "mensaje": "Transacción actualizada",
        "transaccion": transaccion
    }


# eliminar una transacción
@ruta_transacciones.delete("/transacciones/{id}")
async def eliminar_transaccion(
    id: int,
    sesion: sesion_dependencia
):
    transaccion = sesion.get(
        Transacciones,
        id
    )

    if not transaccion:
        return {
            "mensaje": "Transacción no encontrada"
        }

    sesion.delete(transaccion)
    sesion.commit()

    return {
        "mensaje": "Transacción eliminada"
    }