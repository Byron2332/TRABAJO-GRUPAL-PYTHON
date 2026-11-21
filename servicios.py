from abc import abstractmethod  # Permite declarar métodos abstractos en la clase Servicio
from entidades import (
    EntidadSistema,
    DatoInvalidoError,
    ServicioNoDisponibleError,
    CalculoInconsistenteError
)

class Servicio(EntidadSistema):
    """Clase abstracta base para los distintos tipos de servicios ofrecidos por Software FJ."""
    def _init_(self, id_servicio: str, nombre: str, tarifa_hora: float, disponible: bool = True):
        super()._init_(id_servicio)  # Inicializa el ID heredado de EntidadSistema
        if not nombre or not nombre.strip():  # Verifica que el servicio tenga nombre
            raise DatoInvalidoError("El nombre del servicio no puede estar vacío.")
        if tarifa_hora <= 0:  # Verifica que el precio base sea positivo
            raise DatoInvalidoError("La tarifa por hora debe ser mayor a cero.")
        self._nombre = nombre.strip()  # Guarda el nombre del servicio
        self._tarifa_hora = float(tarifa_hora)  # Convierte y guarda la tarifa base como decimal
        self._disponible = disponible  # Indica si el servicio está activo para reservas

    @property
    def nombre(self) -> str:
        """Devuelve el nombre del servicio."""
        return self._nombre

    @property
    def tarifa_hora(self) -> float:
        """Devuelve la tarifa base del servicio."""
        return self._tarifa_hora

    @property
    def disponible(self) -> bool:
        """Devuelve True si el servicio está disponible o False si está deshabilitado."""
        return self._disponible

    @disponible.setter
    def disponible(self, estado: bool):
        """Permite habilitar o deshabilitar el servicio dinámicamente."""
        self._disponible = bool(estado)

    @abstractmethod
    def validar_parametros(self, duracion: int):
        """Método abstracto para validar las reglas de duración específicas de cada servicio."""
        pass

    @abstractmethod
    def calcular_costo(self, duracion: int, descuento: float = 0.0, impuesto: float = 0.0) -> float:
        """Método abstracto con parámetros opcionales (sobrecarga) para calcular el precio final."""
        pass

    def _aplicar_ajustes(self, subtotal: float, descuento: float, impuesto: float) -> float:
        """Método protegido reutilizable que valida disponibilidad y aplica descuentos e impuestos."""
        if not self._disponible:  # Impide calcular costos si el servicio está deshabilitado
            raise ServicioNoDisponibleError("El servicio está deshabilitado.")
        if descuento < 0 or descuento > 1 or impuesto < 0:  # Valida rangos lógicos (0% a 100%)
            raise CalculoInconsistenteError("Porcentajes de descuento o impuesto inválidos.")
        total = subtotal * (1 - descuento) * (1 + impuesto)  # Aplica descuento e IVA sobre el subtotal
        return round(total, 2)  # Redondea el valor final a 2 decimales


class ReservaSala(Servicio):
    """Servicio especializado para el alquiler de salas de reuniones o capacitación."""
    def _init_(self, id_servicio: str, capacidad: int, tarifa_hora: float, disponible: bool = True):
        super()._init_(id_servicio, "Reserva de salas", tarifa_hora, disponible)  # Llama al padre
        if capacidad <= 0:  # Valida que la sala tenga aforo positivo
            raise DatoInvalidoError("La capacidad de la sala debe ser mayor a 0.")
        self._capacidad = capacidad  # Guarda el aforo máximo de la sala

    def validar_parametros(self, duracion: int):
        """Valida que la reserva de sala sea de mínimo 1 hora y máximo 12 horas."""
        if duracion <= 0 or duracion > 12:
            raise DatoInvalidoError("La duración de la sala debe estar entre 1 y 12 horas.")

    def calcular_costo(self, duracion: int, descuento: float = 0.0, impuesto: float = 0.0) -> float:
        """Calcula el costo total multiplicando tarifa por horas y aplicando ajustes."""
        self.validar_parametros(duracion)  # Valida reglas de duración antes de calcular
        subtotal = self.tarifa_hora * duracion  # Calcula el costo base
        return self._aplicar_ajustes(subtotal, descuento, impuesto)  # Retorna total con ajustes

    def obtener_resumen(self) -> str:
        """Devuelve la descripción específica de la sala."""
        return f"Sala | Capacidad: {self._capacidad} personas | Tarifa por hora: {self.tarifa_hora}"


class AlquilerEquipos(Servicio):
    """Servicio especializado para el préstamo de hardware o equipos tecnológicos."""
    def _init_(self, id_servicio: str, equipo: str, tarifa_diaria: float, disponible: bool = True):
        super()._init_(id_servicio, "Alquiler de equipos", tarifa_diaria, disponible)  # Llama al padre
        if not equipo or not equipo.strip():  # Valida que se especifique el nombre del equipo
            raise DatoInvalidoError("Debe especificar el tipo de equipo.")
        self._equipo = equipo.strip()  # Guarda el tipo de equipo

    def validar_parametros(self, duracion: int):
        """Valida que el alquiler sea de al menos 1 día."""
        if duracion <= 0:
            raise DatoInvalidoError("Los días de alquiler deben ser mayores a 0.")

    def calcular_costo(self, duracion: int, descuento: float = 0.0, impuesto: float = 0.0) -> float:
        """Calcula el costo por días de alquiler con posibles descuentos e impuestos."""
        self.validar_parametros(duracion)  # Verifica que los días sean válidos
        subtotal = self.tarifa_hora * duracion  # Calcula tarifa diaria por cantidad de días
        return self._aplicar_ajustes(subtotal, descuento, impuesto)  # Retorna total con ajustes

    def obtener_resumen(self) -> str:
        """Devuelve la descripción específica del equipo en alquiler."""
        return f"Equipo: {self._equipo} | Tarifa diaria: {self.tarifa_hora}"


class AsesoriaEspecializada(Servicio):
    """Servicio especializado de consultoría técnica y desarrollo de software."""
    def _init_(self, id_servicio: str, area: str, tarifa_hora: float, disponible: bool = True):
        super()._init_(id_servicio, "Asesoría especializada", tarifa_hora, disponible)  # Llama al padre
        if not area or not area.strip():  # Valida que se indique la temática de la asesoría
            raise DatoInvalidoError("Debe especificar el área de asesoría.")
        self._area = area.strip()  # Guarda el área de especialidad

    def validar_parametros(self, duracion: int):
        """Valida que la sesión de asesoría dure mínimo 1 hora."""
        if duracion < 1:
            raise DatoInvalidoError("La asesoría requiere mínimo 1 hora.")

    def calcular_costo(self, duracion: int, descuento: float = 0.0, impuesto: float = 0.0) -> float:
        """Calcula el costo total de las horas de consultoría."""
        self.validar_parametros(duracion)  # Valida la duración mínima
        subtotal = self.tarifa_hora * duracion  # Calcula tarifa por hora de consultoría
        return self._aplicar_ajustes(subtotal, descuento, impuesto)  # Retorna total con ajustes

    def obtener_resumen(self) -> str:
        """Devuelve la descripción específica de la asesoría."""
        return f"Asesoría: {self._area} | Tarifa por hora: {self.tarifa_hora}"
