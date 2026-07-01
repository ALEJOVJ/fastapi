from fastapi import APIRouter
from app.modelo.transacciones import Transacciones, TransaccionesCrear, TransaccionesEditar
from app.listas_app import lista_transacciones, lista_facturas, lista_clientes
from app.modelo.facturas import Factura
from app.conexion_bd import sesion_dependencia
from sqlmodel import select

ruta_transacciones = APIRouter()



@ruta_transacciones.get("/transacciones", response_model=list[Transacciones])
async def listar_transacciones(sesion: sesion_dependencia):
    consulta = select(Transacciones)
    lista_transacciones = sesion.exec(consulta).all()
    return lista_transacciones


@ruta_transacciones.get("/transacciones/{id}")
async def obtener_transaccion(id: int):

    for transaccion in lista_transacciones:
        if transaccion.id == id:
            return transaccion

    return {
        "mensaje": "Transacción no encontrada"
    }


@ruta_transacciones.post("/transacciones/{factura_id}")
async def crear_transaccion(
    factura_id: int,
    cliente_id: int,
    datos_transaccion: TransaccionesCrear,
    sesion: sesion_dependencia
):

    factura_encontrada = sesion.get(Factura, factura_id)

    transaccion_dict = datos_transaccion.model_dump()
    transaccion_dict["factura_id"] = factura_id

   

    transaccion_val = Transacciones.model_validate(transaccion_dict)

    sesion.add(transaccion_val)
    sesion.commit()
    sesion.refresh(transaccion_val)

    return {
        "mensaje": "Transacción creada",
        "transaccion": transaccion_val
    }


@ruta_transacciones.put("/transacciones/{id}")
async def editar_transaccion(
    id: int,
    datos_transaccion: TransaccionesEditar
):

    for i, transaccion in enumerate(lista_transacciones):

        if transaccion.id == id:

            transaccion_val = Transacciones.model_validate(
                datos_transaccion.model_dump()
            )

            transaccion_val.id = id
            transaccion_val.factura_id = transaccion.factura_id

            lista_transacciones[i] = transaccion_val

            return {
                "mensaje": "Transacción actualizada",
                "transaccion": transaccion_val
            }

    return {
        "mensaje": "Transacción no encontrada"
    }


@ruta_transacciones.delete("/transacciones/{id}")
async def eliminar_transaccion(id: int):

    for transaccion in lista_transacciones:

        if transaccion.id == id:

            lista_transacciones.remove(transaccion)

            return {
                "mensaje": "Transacción eliminada"
            }

    return {
        "mensaje": "Transacción no encontrada"
    }