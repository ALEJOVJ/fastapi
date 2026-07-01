from pydantic import BaseModel, computed_field
from sqlmodel import SQLModel, Field, Relationship
from app.modelo.clientes import Clientes , Clienteleer
from app.modelo.transacciones import Transacciones
from datetime import datetime


class FacturaBase(SQLModel):
    fecha: str = Field(default=datetime.now())
    #cliente: Clientes
    #transacciones: list[Transacciones] = []



        #return sum(
        #    transaccion.cantidad * transaccion.vr_unitario
        #    for transaccion in self.transacciones
        #    if transaccion.factura_id == factura_id_actual
        #)

        


class FacturaCrear(FacturaBase):
    pass


class FacturaEditar(FacturaBase):
    pass


class Factura(FacturaBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    Cliente_id: int = Field(default=None, foreign_key="clientes.id")
    #crear relaciones virtuales con cliente, transacciones - no en la bd 
    cliente : Clientes = Relationship(back_populates="factura")
    transacciones: list[Transacciones] = Relationship(back_populates="factura")

    @computed_field
    @property
    def valor_total(self) -> float:

        #factura_id_actual = getattr(self, "id", None)

        #if factura_id_actual is None:
        #    return 0.0
        total_factura = 0.0
        if self.transacciones == None:
            return total_factura
        
        for transaccion in self.transacciones:
            total_factura += (
            transaccion.vr_unitario *
            transaccion.cantidad)
        return total_factura
    


    #crear modelo para mostrar el usuario o el cliente

class Facturaleer(FacturaBase):
        id: int
        cliente: Clienteleer
        valor_total: float

class Facturaleercompuesta(Facturaleer):
    transacciones: list[Transacciones] = []     
