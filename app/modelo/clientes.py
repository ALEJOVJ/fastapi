from pydantic import BaseModel



class Clientesbase(BaseModel) :
    nombre :str
    edad: int
    descripcion : str | None

class ClientesCrear(Clientesbase):
    pass

class ClientesEditar(Clientesbase):
    pass

class Clientes(Clientesbase) :
    id : int | None = None

class EliminarCliente() :
    pass
