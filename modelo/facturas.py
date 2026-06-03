from pydantic import BaseModel, computed_field

from modelo.clientes import Clientes
from modelo.transacciones import Transacciones


class FacturaBase(BaseModel):
    fecha: str
    cliente: Clientes
    transacciones: list[Transacciones] = []

    @computed_field
    @property
    def valor_total(self) -> float:

        factura_id_actual = getattr(self, "id", None)

        if factura_id_actual is None:
            return 0.0

        return sum(
            transaccion.cantidad * transaccion.vr_unitario
            for transaccion in self.transacciones
            if transaccion.factura_id == factura_id_actual
        )


class FacturaCrear(FacturaBase):
    pass


class FacturaEditar(FacturaBase):
    pass


class Factura(FacturaBase):
    id: int | None = None