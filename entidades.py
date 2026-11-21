from abc import ABC, abstractmethod
import logging
import os

# Configuración del archivo de logs
os.makedirs("logs", exist_ok=True)
logging.basicConfig(
    filename="logs/sistema.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    encoding="utf-8"
)

def registrar_evento(mensaje: str, es_error: bool = False, exc_info: bool = False):
    """Registra eventos y errores en el archivo logs/sistema.log."""
    if es_error:
        logging.error(mensaje, exc_info=exc_info)
    else:
        logging.info(mensaje)


# --- EXCEPCIONES PERSONALIZADAS ---
class ErrorSistemaFJ(Exception):
    """Excepción base para el sistema de Software FJ."""
    pass

class DatoInvalidoError(ErrorSistemaFJ):
    """Se lanza cuando un dato de entrada no cumple las validaciones."""
    pass

class EntidadNoEncontradaError(ErrorSistemaFJ):
    """Se lanza cuando no se encuentra un cliente, servicio o reserva."""
    pass

class ServicioNoDisponibleError(ErrorSistemaFJ):
    """Se lanza cuando se intenta usar un servicio deshabilitado."""
    pass

class OperacionNoPermitidaError(ErrorSistemaFJ):
    """Se lanza ante cambios de estado o acciones inválidas en reservas."""
    pass

class CalculoInconsistenteError(ErrorSistemaFJ):
    """Se lanza cuando ocurre un error en el cálculo de costos."""
    pass


# --- CLASE ABSTRACTA BASE ---
class EntidadSistema(ABC):
    """Clase abstracta que representa las entidades generales del sistema."""
    def __init__(self, id_entidad: str):
        if not id_entidad or not str(id_entidad).strip():
            raise DatoInvalidoError("El ID de la entidad no puede estar vacío.")
        self._id = str(id_entidad).strip()

    @property
    def id(self) -> str:
        return self._id

    @abstractmethod
    def obtener_resumen(self) -> str:
        """Método abstracto obligatorio para describir la entidad."""
        pass
