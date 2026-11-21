from entidades import (
    EntidadSistema,
    DatoInvalidoError,
    ServicioNoDisponibleError,
    OperacionNoPermitidaError
)
from clientes import Cliente
from servicios import Servicio

class Reserva(EntidadSistema):
    """Integra un Cliente y un Servicio con control de estados y costos."""
    def _init_(self, id_reserva: str, cliente: Cliente, servicio: Servicio, duracion: int):
        super()._init_(id_reserva)
        if not isinstance(cliente, Cliente):
            raise DatoInvalidoError("Cliente inválido para la reserva.")
        if not isinstance(servicio, Servicio):
            raise DatoInvalidoError("Servicio inválido para la reserva.")
        if not servicio.disponible:
            raise ServicioNoDisponibleError("El servicio no está disponible.")

        servicio.validar_parametros(duracion)
        self._cliente = cliente
        self._servicio = servicio
        self._duracion = duracion
        self._estado = "Pendiente"
        self._total = None

    @property
    def estado(self) -> str:
        return self._estado

    @property
    def total(self):
        return self._total

    def confirmar(self):
        if self._estado != "Pendiente":
            raise OperacionNoPermitidaError("Solo se pueden confirmar reservas pendientes.")
        self._estado = "Confirmada"

    def procesar(self, descuento: float = 0.0, impuesto: float = 0.0):
        if self._estado != "Confirmada":
            raise OperacionNoPermitidaError("La reserva debe estar confirmada antes de procesarse.")
        self._total = self._servicio.calcular_costo(self._duracion, descuento, impuesto)
        self._estado = "Procesada"

    def cancelar(self):
        if self._estado == "Procesada":
            raise OperacionNoPermitidaError("No se puede cancelar una reserva ya procesada.")
        self._estado = "Cancelada"

    def obtener_resumen(self) -> str:
        return (
            f"Reserva #{self.id} | Cliente: {self._cliente.nombre} | "
            f"Servicio: {self._servicio.nombre} | Duración: {self._duracion} | "
            f"Estado: {self._estado} | Total: {self._total}"
        )
