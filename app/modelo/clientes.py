from pydantic import BaseModel
from sqlmodel import SQLModel, Field, Relationship




class Clientesbase(SQLModel) :
    nombre :str = Field(default=None)
    edad: int = Field(default=None)
    descripcion : str | None = Field(default=None)

class ClientesCrear(Clientesbase):
    pass

class ClientesEditar(Clientesbase):
    pass

class Clientes(Clientesbase, table=True) :
    id : int | None = Field(default=None, primary_key=True)
    #relacion virutal con factura
    factura: list["Factura"] = Relationship(back_populates="cliente")

class Clienteleer(Clientesbase):
    id: int

class EliminarCliente():
    pass
