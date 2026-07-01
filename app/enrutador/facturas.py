from fastapi import APIRouter
from datetime import datetime
from app.modelo.facturas import Factura, FacturaCrear, FacturaEditar
from app.listas_app import lista_facturas, lista_clientes , lista_transacciones
from app.conexion_bd import sesion_dependencia
from sqlmodel import select
from app.modelo.clientes import Clientes

ruta_facturas = APIRouter()


@ruta_facturas.get("/facturas", response_model=list[Factura])
async def listar_facturas(sesion: sesion_dependencia):
    #select from * factura
    consulta = select(Factura)
    lista_facturas = sesion.exec(consulta).all()
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
    datos_factura: FacturaCrear,
    sesion: sesion_dependencia
):



    cliente_encontrado = sesion.get(Clientes, cliente_id)

    if not cliente_encontrado:
        return {
            "mensaje": "Cliente no encontrado"
        }


    factura_dict = datos_factura.model_dump()
    factura_dict["Cliente_id"] = cliente_id
    factura_val = Factura.model_validate(factura_dict)

    sesion.add(factura_val)
    sesion.commit()
    sesion.refresh(factura_val)

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