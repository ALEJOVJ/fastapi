from fastapi import APIRouter
from app.modelo.clientes import Clientes, ClientesCrear, ClientesEditar
from app.listas_app import lista_clientes

ruta_clientes = APIRouter()




@ruta_clientes.get("/clientes")
async def listar_clientes():
    return {"clientes": lista_clientes}


@ruta_clientes.get("/clientes/{id}")
async def obtener_cliente(id: int):
    for cliente in lista_clientes:
        if cliente.id == id:
            return cliente

    return {
        "mensaje": "Cliente no encontrado"
    }


@ruta_clientes.post("/clientes", response_model=Clientes)
async def crear_cliente(datos_cliente: ClientesCrear):

    cliente_val = Clientes.model_validate(
        datos_cliente.model_dump()
    )

    cliente_val.id = len(lista_clientes) + 1

    lista_clientes.append(cliente_val)

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