from fastapi import FastAPI
from modelo.clientes import Clientes , ClientesCrear , ClientesEditar , EliminarCliente




app = FastAPI()

lista_clientes : list [Clientes] =[]

@app.get("/clientes")

async def listar_clientes():
    return {"cliente": lista_clientes}

@app.get("/clientes/{id}")
async def lista_clientes(id:int):
    for clientes in lista_clientes:
        if clientes.id == id :
            return clientes




@app.post("/clientes" , response_model=Clientes)

async def crear_cliente(datos_clientes:ClientesCrear):
    clientes_val = Clientes.model_validate(datos_clientes.model_dump())

    clientes_val.id = len(lista_clientes)+1

    lista_clientes.append(clientes_val)


    #return {"cliente": "Cliente creado"}
    return clientes_val 

@app.put("/clientes/{id}")
async def editar_cliente(id : int,datos_cliente: ClientesEditar):
    for i, obj_cliente.id in enumerate (lista_clientes):
        if obj_cliente.id == id :
            cliente_val = cliente.model_validate(datos_cliente.model_dump())
            cliente_Val.id = id
            lista_clientes [i] = clientes_val

    return {"mensaje": "se acutalizo","cliente": cliente_val}

@app.delete("/clientes")
async def eliminar_cliente(id : int):
    for cliente in lista_clientes :
        if cliente.id == id:
            lista_clientes.remove(cliente)

    return {"clientes": "Cliente eliminado"}