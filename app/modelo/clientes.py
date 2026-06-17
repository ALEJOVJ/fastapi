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

class EliminarCliente() :
    pass
