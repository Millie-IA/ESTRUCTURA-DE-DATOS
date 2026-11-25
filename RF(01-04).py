import os
import csv

# ARCHIVOS

CLIENTES_FILE = "clientes.csv"
BUSES_FILE = "buses.csv"
CIUDADES_FILE = "ciudades.csv"
VIAJES_FILE = "viajes.csv"

ENCODE = "utf-8-sig"

# ==========================================
# 1. CLASES DE ENTIDAD
# ==========================================

class Cliente:
    def __init__(self, id_cliente: str, rut: str, nombres: str, apellido_paterno: str, apellido_materno: str, contacto: str):
        self.id_cliente = id_cliente
        self.rut = rut
        self.nombres = nombres
        self.apellido_paterno = apellido_paterno
        self.apellido_materno = apellido_materno
        self.contacto = contacto

class Bus:
    def __init__(self, id_bus: str, patente: str, capacidad: int, estado: str):
        self.id_bus = id_bus
        self.patente = patente
        self.capacidad = capacidad
        self.estado = estado # Ej: 'Disponible', 'En ruta', etc.

class Ciudad:
    def __init__(self, id_ciudad: str, nombre: str, posicion: int):
        self.id_ciudad = id_ciudad
        self.nombre = nombre
        self.posicion = posicion

class Viaje:
    def __init__(self, id_viaje: str, id_bus: str, fecha: str, hora: str, id_origen: str, id_destino: str, tarifa_base: float):
        self.id_viaje = id_viaje
        self.id_bus = id_bus
        self.fecha = fecha
        self.hora = hora
        self.id_origen = id_origen
        self.id_destino = id_destino
        self.tarifa_base = tarifa_base


# ==========================================
# 2. GESTORES 
# ==========================================

class ClienteGestion:
    def __init__(self):
        self.clientes = []
        self._inicializar_archivo()
        self.cargar_clientes()

    def _inicializar_archivo(self) -> None:
        """Verifica si el archivo clientes.csv existe; si no, lo crea con su cabecera."""
        # TODO: Implementar lógica de os.path.exists y creación con csv.writer
        
        pass

    def cargar_clientes(self) -> None:
        """Carga los clientes desde el archivo CSV a la lista en memoria self.clientes."""
        # TODO: Leer el CSV y poblar objetos Cliente
        pass

    def guardar_clientes(self) -> None:
        """Guarda la lista actual de clientes desde la memoria hacia el archivo CSV."""
        # TODO: Escribir self.clientes en el CSV
        pass

    def registrar_cliente(self, rut: str, nombres: str, apellido_paterno: str, apellido_materno: str, contacto: str) -> bool:
        """RF01: Registra un cliente validando campos obligatorios y evitando RUTs duplicados."""
        # TODO: Validar que no falten datos, verificar RUT único, generar ID automático y guardar.
        pass

    def listar_clientes(self) -> list:
        """RF01: Retorna la lista de todos los clientes registrados."""
        # TODO: Retornar self.clientes o imprimirlos ordenadamente
        pass

    def buscar_cliente_por_rut(self, rut: str) -> Cliente | None:
        """RF01: Busca y retorna un cliente según su número de RUT."""
        # TODO: Buscar en la lista y retornar el objeto o None si no existe
        pass


class BusGestion:
    def __init__(self):
        self.buses = []
        self._inicializar_archivo()
        self.cargar_buses()

    def _inicializar_archivo(self) -> None:
        """Crea el archivo buses.csv con su cabecera si no existe."""
        # TODO: Implementar
        pass

    def cargar_buses(self) -> None:
        """Carga los buses desde el archivo CSV."""
        # TODO: Implementar
        pass

    def guardar_buses(self) -> None:
        """Guarda los buses en el archivo CSV."""
        # TODO: Implementar
        pass

    def registrar_bus(self, patente: str, capacidad: int, estado: str) -> bool:
        """RF02: Registra un bus validando patente única y capacidad entera positiva."""
        # TODO: Implementar validaciones y registro
        pass

    def listar_buses(self) -> list:
        """RF02: Retorna el listado de buses."""
        # TODO: Implementar
        pass

    def consultar_bus(self, id_bus: str) -> Bus | None:
        """RF02: Consulta un bus específico por su ID."""
        # TODO: Implementar
        pass


class CiudadGestion:
    def __init__(self):
        self.ciudades = []
        self._inicializar_y_cargar_catalogo()

    def _inicializar_y_cargar_catalogo(self) -> None:
        """RF03: Carga el catálogo fijo de las 6 ciudades si el archivo no existe o está vacío."""
        # Ciudades fijas exigidas por pauta:
        # 0: Concepción, 1: Chillán, 2: Linares, 3: Talca, 4: Rancagua, 5: Santiago
        # TODO: Verificar archivo ciudades.csv, si no existe, crearlo con las 6 ciudades por defecto.
        pass

    def listar_ciudades(self) -> list:
        """RF03: Retorna el catálogo completo de ciudades con sus posiciones."""
        # TODO: Implementar
        pass


class ViajeGestion:
    def __init__(self, bus_gestion: BusGestion, ciudad_gestion: CiudadGestion):
        self.viajes = []
        self.bus_gestion = bus_gestion
        self.ciudad_gestion = ciudad_gestion
        self._inicializar_archivo()
        self.cargar_viajes()

    def _inicializar_archivo(self) -> None:
        """Crea el archivo viajes.csv con su cabecera si no existe."""
        # TODO: Implementar
        pass

    def cargar_viajes(self) -> None:
        """Carga los viajes desde el archivo CSV."""
        # TODO: Implementar
        pass

    def guardar_viajes(self) -> None:
        """Guarda los viajes en el archivo CSV."""
        # TODO: Implementar
        pass

    def programar_viaje(self, id_bus: str, fecha: str, hora: str, id_origen: str, id_destino: str, tarifa_base: float) -> bool:
        """RF04: Programa un viaje validando que el bus exista, y que la ruta sea 
        estrictamente Concepción-Santiago o Santiago-Concepción."""
        # TODO: Validar existencia del bus, validar sentido de origen/destino y registrar.
        pass

    def listar_viajes(self) -> list:
        """RF04: Retorna el listado de viajes programados."""
        # TODO: Implementar
        pass