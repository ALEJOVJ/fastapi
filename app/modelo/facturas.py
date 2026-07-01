from pydantic import BaseModel, computed_field
from sqlmodel import SQLModel, Field, Relationship
from app.modelo.clientes import Clientes
from app.modelo.transacciones import Transacciones
from datetime import datetime


class FacturaBase(SQLModel):
    fecha: str = Field(default=datetime.now())
    #cliente: Clientes
    #transacciones: list[Transacciones] = []

    @computed_field
    @property
    def valor_total(self) -> float:

        #factura_id_actual = getattr(self, "id", None)

        #if factura_id_actual is None:
        #    return 0.0

        #return sum(
        #    transaccion.cantidad * transaccion.vr_unitario
        #    for transaccion in self.transacciones
        #    if transaccion.factura_id == factura_id_actual
        #)

        return 0.0


class FacturaCrear(FacturaBase):
    pass


class FacturaEditar(FacturaBase):
    pass


class Factura(FacturaBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    Cliente_id: int = Field(default=None, foreign_key="clientes.id")
