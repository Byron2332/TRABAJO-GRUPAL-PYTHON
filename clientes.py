import re  # Importa el módulo de expresiones regulares para validar el formato del correo
from entidades import EntidadSistema, DatoInvalidoError  # Importa la clase base y la excepción de datos

class Cliente(EntidadSistema):
    """Clase que representa a un cliente aplicando encapsulación y validaciones estrictas."""
    def __init__(self, id_cliente: str, nombre: str, correo: str):
        super().__init__(id_cliente)  # Llama al constructor de la clase padre (EntidadSistema)
        self.nombre = nombre  # Asigna el nombre pasando automáticamente por el setter de validación
        self.correo = correo  # Asigna el correo pasando automáticamente por el setter de validación

    @property
    def nombre(self) -> str:
        """Getter que devuelve el nombre encapsulado del cliente."""
        return self._nombre

    @nombre.setter
    def nombre(self, valor: str):
        """Setter que valida que el nombre no esté vacío y tenga al menos 3 letras."""
        if not valor or len(valor.strip()) < 3:
            raise DatoInvalidoError("El nombre del cliente debe tener al menos 3 caracteres.")
        self._nombre = valor.strip()  # Guarda el nombre limpio en el atributo protegido

    @property
    def correo(self) -> str:
        """Getter que devuelve el correo electrónico encapsulado del cliente."""
        return self._correo

    @correo.setter
    def correo(self, valor: str):
        """Setter que valida mediante expresión regular que el correo tenga formato usuario@dominio.ext."""
        patron = r"^[\w\.-]+@[\w\.-]+\.\w+$"  # Define el patrón estándar de un correo válido
        if not valor or not re.match(patron, valor.strip()):
            raise DatoInvalidoError("El correo electrónico no es válido.")
        self._correo = valor.strip()  # Guarda el correo válido en el atributo protegido

    def obtener_resumen(self) -> str:
        """Implementación polimórfica del resumen con los datos principales del cliente."""
        return f"Cliente: {self.nombre} | ID: {self.id} | Correo: {self.correo}"
