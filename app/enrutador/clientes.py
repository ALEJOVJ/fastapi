from fastapi import APIRouter
from app.modelo.clientes import Clientes, ClientesCrear, ClientesEditar
from app.listas_app import lista_clientes
from app.conexion_bd import sesion_dependencia
from sqlmodel import select
from fastapi import HTTPException

ruta_clientes = APIRouter()




@ruta_clientes.get("/clientes", response_model=list[Clientes])
async def listar_clientes(sesion: sesion_dependencia):

    clientes = sesion.exec(select(Clientes)).all()

    return clientes



@ruta_clientes.get("/clientes/{id}", response_model=Clientes,)
async def obtener_cliente(id: int, mi_sesion: sesion_dependencia):
    cliente_bd = mi_sesion.get(Clientes,id)
    if not cliente_bd:
        
        return cliente_bd


@ruta_clientes.post("/clientes", response_model=Clientes)
async def crear_cliente(datos_cliente: ClientesCrear, mi_sesion: sesion_dependencia):

    cliente_val = Clientes.model_validate(
        datos_cliente.model_dump()
    )

    mi_sesion.add(cliente_val)
    mi_sesion.commit()
    mi_sesion.refresh(cliente_val)

    return cliente_val


@ruta_clientes.put("/clientes/{id}", response_model=Clientes)
async def editar_cliente(id: int, datos_cliente: ClientesEditar,mi_sesion: sesion_dependencia):
    cliente_bd = mi_sesion.get(Clientes, id)

    if not cliente_bd:
        raise HTTPException(
        status_code=404,
        detail="Cliente no encontrado"
    )

    cliente_dict = datos_cliente.model_dump(exclude_unset=True)
    cliente_bd.sqlmodel_update(cliente_dict)

    mi_sesion.add(cliente_bd)
    mi_sesion.commit()
    mi_sesion.refresh(cliente_bd)

    return cliente_bd
        


@ruta_clientes.delete("/clientes/{id}", response_model=Clientes)
async def eliminar_cliente(id: int , mi_sesion: sesion_dependencia):
    
    cliente_bd = mi_sesion.get(Clientes, id)

    if not cliente_bd:
        raise HTTPException(
        status_code=404,
        detail="Cliente no encontrado"
    )

    mi_sesion.delete(cliente_bd)
    mi_sesion.commit()

    return cliente_bd
    
    

