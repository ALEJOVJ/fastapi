from fastapi import FastAPI, HTTPException
from modelo.clientes import Clientes, ClientesCrear, ClientesEditar

from datetime import datetime

from modelo.facturas import Factura, FacturaCrear
from modelo.transacciones import Transacciones, TransaccionesCrear

app = FastAPI()

lista_clientes: list[Clientes] = []

lista_facturas: list[Factura] = []
lista_transacciones: list[Transacciones] = []


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






@app.get("/facturas", response_model=list[Factura])
async def listar_facturas():
    return lista_facturas


@app.post("/facturas/{cliente_id}", response_model=Factura)
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
        raise HTTPException(
            status_code=400,
            detail=f"Cliente con id {cliente_id} no existe"
        )

    factura_val = Factura.model_validate(
        datos_factura.model_dump()
    )

    factura_val.id = len(lista_facturas) + 1
    factura_val.fecha = str(datetime.now())
    factura_val.cliente = cliente_encontrado

    lista_facturas.append(factura_val)

    return factura_val


@app.get("/transacciones", response_model=list[Transacciones])
async def listar_transacciones():
    return lista_transacciones


@app.post("/transacciones/{factura_id}")
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
        raise HTTPException(
            status_code=400,
            detail=f"No existe cliente con id {cliente_id}"
        )

    factura_encontrada = None

    for factura in lista_facturas:
        if factura.id == factura_id:
            factura_encontrada = factura
            break

    if factura_encontrada:

        if factura_encontrada.cliente.id == cliente_id:

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
                "mensaje": f"Transacción agregada a factura {factura_id}",
                "factura": factura_encontrada
            }

        raise HTTPException(
            status_code=400,
            detail="La factura pertenece a otro cliente"
        )

    transaccion_val = Transacciones.model_validate(
        datos_transaccion.model_dump()
    )

    transaccion_val.id = len(lista_transacciones) + 1
    transaccion_val.factura_id = len(lista_facturas) + 1

    nueva_factura = FacturaCrear(
        fecha=str(datetime.now()),
        cliente=cliente_encontrado,
        transacciones=[transaccion_val]
    )

    factura_val = Factura.model_validate(
        nueva_factura.model_dump()
    )

    factura_val.id = len(lista_facturas) + 1

    lista_facturas.append(factura_val)
    lista_transacciones.append(transaccion_val)

    return {
        "mensaje": "No existía la factura, se creó automáticamente",
        "factura": factura_val
    }
