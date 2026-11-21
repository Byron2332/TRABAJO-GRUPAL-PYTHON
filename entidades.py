from abc import ABC, abstractmethod  # Importa herramientas para crear clases y métodos abstractos
import logging  # Importa el módulo estándar para registrar eventos y errores en archivos
import os  # Importa funciones del sistema operativo para gestionar carpetas y rutas

# Crea la carpeta 'logs' en el directorio del proyecto si aún no existe
os.makedirs("logs", exist_ok=True)

# Configura el sistema de registro (logging) para guardar todo en 'logs/sistema.log'
logging.basicConfig(
    filename="logs/sistema.log",  # Ruta y nombre del archivo de salida
    level=logging.INFO,  # Nivel mínimo de registro (guarda mensajes INFO y ERROR)
    format="%(asctime)s - %(levelname)s - %(message)s",  # Estructura: Fecha/Hora - Nivel - Mensaje
    datefmt="%Y-%m-%d %H:%M:%S",  # Formato legible de fecha y hora
    encoding="utf-8"  # Permite guardar tildes y caracteres especiales en español
)

def registrar_evento(mensaje: str, es_error: bool = False, exc_info: bool = False):
    """Función auxiliar para escribir eventos normales o errores en el archivo de logs."""
    if es_error:  # Verifica si el evento corresponde a un fallo
        logging.error(mensaje, exc_info=exc_info)  # Registra el error y, si se indica, su traza técnica
    else:  # Si es una operación exitosa o informativa
        logging.info(mensaje)  # Registra el evento como información normal


# --- JERARQUÍA DE EXCEPCIONES PERSONALIZADAS ---
class ErrorSistemaFJ(Exception):
    """Excepción base de la que heredan todos los errores controlados de Software FJ."""
    pass

class DatoInvalidoError(ErrorSistemaFJ):
    """Se lanza cuando un dato ingresado no cumple con las reglas de validación."""
    pass

class EntidadNoEncontradaError(ErrorSistemaFJ):
    """Se lanza cuando se busca un ID de cliente, servicio o reserva que no existe."""
    pass

class ServicioNoDisponibleError(ErrorSistemaFJ):
    """Se lanza cuando se intenta reservar o calcular un servicio deshabilitado."""
    pass

class OperacionNoPermitidaError(ErrorSistemaFJ):
    """Se lanza al intentar realizar un cambio de estado inválido en una reserva."""
    pass

class CalculoInconsistenteError(ErrorSistemaFJ):
    """Se lanza cuando los porcentajes de descuento o impuesto son incoherentes."""
    pass


# --- CLASE ABSTRACTA BASE ---
class EntidadSistema(ABC):
    """Clase abstracta que define la estructura común para todas las entidades del sistema."""
    def __init__(self, id_entidad: str):
        # Valida que el identificador no sea nulo ni una cadena de espacios en blanco
        if not id_entidad or not str(id_entidad).strip():
            raise DatoInvalidoError("El ID de la entidad no puede estar vacío.")
        # Almacena el ID como atributo protegido limpiando espacios extremos
        self._id = str(id_entidad).strip()

    @property
    def id(self) -> str:
        """Propiedad de solo lectura para acceder de forma segura al ID protegido."""
        return self._id

    @abstractmethod
    def obtener_resumen(self) -> str:
        """Método abstracto que obliga a las clases hijas a implementar su propia descripción."""
        pass
