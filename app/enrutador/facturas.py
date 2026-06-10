from fastapi import APIRouter
from datetime import datetime
from app.modelo.facturas import Factura, FacturaCrear, FacturaEditar
from app.listas_app import lista_facturas, lista_clientes , lista_transacciones

ruta_facturas = APIRouter()


@ruta_facturas.get("/facturas", response_model=list[Factura])
async def listar_facturas():
    return lista_facturas


@ruta_facturas.get("/facturas/{id}")
async def obtener_factura(id: int):

    for factura in lista_facturas:
        if factura.id == id:
            return factura

    return {
        "mensaje": "Factura no encontrada"
    }


@ruta_facturas.post("/facturas/{cliente_id}", response_model=Factura)
async def crear_factura(
    cliente_id: int,
    datos_factura: FacturaCrear
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

    factura_val = Factura.model_validate(
        datos_factura.model_dump()
    )

    factura_val.id = len(lista_facturas) + 1
    factura_val.fecha = str(datetime.now())
    factura_val.cliente = cliente_encontrado

    lista_facturas.append(factura_val)

    return factura_val


@ruta_facturas.put("/facturas/{id}")
async def editar_factura(
    id: int,
    datos_factura: FacturaEditar
):

    for i, factura in enumerate(lista_facturas):

        if factura.id == id:

            factura_val = Factura.model_validate(
                datos_factura.model_dump()
            )

            factura_val.id = id
            factura_val.cliente = factura.cliente

            lista_facturas[i] = factura_val

            return {
                "mensaje": "Factura actualizada",
                "factura": factura_val
            }

    return {
        "mensaje": "Factura no encontrada"
    }


@ruta_facturas.delete("/facturas/{id}")
async def eliminar_factura(id: int):

    for factura in lista_facturas:

        if factura.id == id:

            lista_transacciones[:] = [
                transaccion
                for transaccion in lista_transacciones
                if transaccion.factura_id != id
            ]

            lista_facturas.remove(factura)

            return {
                "mensaje": "Factura eliminada"
            }

    return {
        "mensaje": "Factura no encontrada"
    }