from fastapi import APIRouter
from app.modelo.transacciones import Transacciones, TransaccionesCrear, TransaccionesEditar
from app.listas_app import lista_transacciones, lista_facturas, lista_clientes

ruta_transacciones = APIRouter()



@ruta_transacciones.get("/transacciones", response_model=list[Transacciones])
async def listar_transacciones():
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
    datos_transaccion: TransaccionesCrear
):

    cliente_encontrado = None

    for cliente in lista_clientes:
        if cliente.id == cliente_id:
            cliente_encontrado = cliente
            break

    if not cliente_encontrado:
        return {
            "mensaje": "Cliente no encontrado"
        }

    factura_encontrada = None

    for factura in lista_facturas:
        if factura.id == factura_id:
            factura_encontrada = factura
            break

    if not factura_encontrada:
        return {
            "mensaje": "Factura no encontrada"
        }

    if factura_encontrada.cliente.id != cliente_id:
        return {
            "mensaje": "La factura pertenece a otro cliente"
        }

    transaccion_val = Transacciones.model_validate(
        datos_transaccion.model_dump()
    )

    transaccion_val.id = len(lista_transacciones) + 1
    transaccion_val.factura_id = factura_id

    lista_transacciones.append(transaccion_val)

    factura_encontrada.transacciones.append(
        transaccion_val
    )

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