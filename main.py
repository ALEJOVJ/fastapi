from fastapi import FastAPI, HTTPException
from modelo.clientes import Clientes, ClientesCrear, ClientesEditar

app = FastAPI()

lista_clientes: list[Clientes] = []


@app.get("/clientes")
async def listar_clientes():
    return {"clientes": lista_clientes}


@app.get("/clientes/{id}")
async def obtener_cliente(id: int):
    for cliente in lista_clientes:
        if cliente.id == id:
            return cliente

    raise HTTPException(
        status_code=404,
        detail="Cliente no encontrado"
    )


@app.post("/clientes", response_model=Clientes)
async def crear_cliente(datos_cliente: ClientesCrear):

    cliente_val = Clientes.model_validate(
        datos_cliente.model_dump()
    )

    cliente_val.id = len(lista_clientes) + 1

    lista_clientes.append(cliente_val)

    return cliente_val


@app.put("/clientes/{id}")
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

    raise HTTPException(
        status_code=404,
        detail="Cliente no encontrado"
    )


@app.delete("/clientes/{id}")
async def eliminar_cliente(id: int):

    for cliente in lista_clientes:

        if cliente.id == id:

            lista_clientes.remove(cliente)

            return {
                "mensaje": "Cliente eliminado"
            }

    raise HTTPException(
        status_code=404,
        detail="Cliente no encontrado"
    )