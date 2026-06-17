from fastapi import APIRouter
from app.modelo.clientes import Clientes, ClientesCrear, ClientesEditar
from app.listas_app import lista_clientes
from app.conexion_bd import sesion_dependencia
from sqlmodel import select

ruta_clientes = APIRouter()




@ruta_clientes.get("/clientes", response_model=list[Clientes])
async def listar_clientes(sesion: sesion_dependencia):

    clientes = sesion.exec(select(Clientes)).all()

    return clientes



@ruta_clientes.get("/clientes/{id}", response_model=Clientes,)
async def obtener_cliente(id: int, mi_sesion: sesion_dependencia):
    for cliente in lista_clientes:
        if cliente.id == id:
            return cliente

    return {
        "mensaje": "Cliente no encontrado"
    }


@ruta_clientes.post("/clientes", response_model=Clientes)
async def crear_cliente(datos_cliente: ClientesCrear, mi_sesion: sesion_dependencia):

    cliente_val = Clientes.model_validate(
        datos_cliente.model_dump()
    )

    mi_sesion.add(cliente_val)
    mi_sesion.commit()
    mi_sesion.refresh(cliente_val)

    return cliente_val


@ruta_clientes.put("/clientes/{id}")
async def editar_cliente(id: int, datos_cliente: ClientesEditar):

    for i, cliente in enumerate(lista_clientes):

        if cliente.id == id:

            cliente_val = Clientes.model_validate(
                datos_cliente.model_dump()
            )

            cliente_val.id = id

            lista_clientes[i] = cliente_val

            return {
                "mensaje": "Cliente actualizado",
                "cliente": cliente_val
            }

    return {
        "mensaje": "Cliente no encontrado"
    }


@ruta_clientes.delete("/clientes/{id}")
async def eliminar_cliente(id: int):

    for cliente in lista_clientes:

        if cliente.id == id:

            lista_clientes.remove(cliente)

            return {
                "mensaje": "Cliente eliminado"
            }

    return {
        "mensaje": "Cliente no encontrado"
    }