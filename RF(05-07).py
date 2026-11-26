import csv
import os

CLIENTES_FILE = "clientes.csv"
BUSES_FILE = "buses.csv"
CIUDADES_FILE = "ciudades.csv"
VIAJES_FILE = "viajes.csv"
PASAJES_FILE = "pasajes.csv"

ENCODE = "utf-8-sig"

class Pasaje:
    def __init__(self, id_pasaje, id_viaje, id_cliente, id_origen, id_destino, asiento, valor, estado="VIGENTE"):
        self.id_pasaje = id_pasaje
        self.id_viaje = id_viaje
        self.id_cliente = id_cliente
        self.id_origen = id_origen
        self.id_destino = id_destino
        self.asiento = asiento
        self.valor = valor
        self.estado = estado


class PasajeGestion:
    def __init__(self):
        self.pasajes = []
        self.inicializar_archivo_pasajes()
        self.cargar_pasajes()
        
        

def inicializar_archivo_pasajes():
    """Crea pasajes.csv con su cabecera si no existe."""
    # TODO: verificar os.path.exists y crear cabecera con csv.writer
    pass


def cargar_pasajes():
    """Carga los pasajes desde pasajes.csv."""
    # TODO: leer csv con DictReader y armar lista de pasajes
    pass


def guardar_pasajes(pasajes):
    """Guarda la lista de pasajes en pasajes.csv."""
    # TODO: escribir cabecera y filas con csv.writer
    pass


def leer_csv(archivo):
    """Lee un archivo CSV y retorna sus filas como diccionarios."""
    # TODO: validar si existe y no está vacío, luego retornar list(csv.DictReader(f))
    pass


# ==========================================
# FUNCIONES AUXILIARES DE BÚSQUEDA Y CÁLCULO
# ==========================================


def buscar_cliente_por_id(id_cliente):
    """Busca si existe un cliente con ese ID."""
    # TODO: buscar en clientes.csv por id_cliente
    pass


def buscar_viaje_por_id(id_viaje):
    """Busca si existe un viaje con ese ID."""
    # TODO: buscar en viajes.csv por id_viaje
    pass


def buscar_bus_por_id(id_bus):
    """Busca un bus por su ID para consultar su capacidad."""
    # TODO: buscar en buses.csv por id_bus (similar a consultar_bus de compañera)
    pass


def buscar_ciudad_por_id(id_ciudad):
    """Busca una ciudad por su ID para obtener su posición."""
    # TODO: buscar en ciudades.csv por id_ciudad
    pass


def calcular_tarifa(tarifa_base, pos_origen, pos_destino):
    """Calcula la tarifa con descuento acumulativo del 10% por segmento no utilizado."""
    # TODO: calcular segmentos usados (5 en total) y descontar 10% por cada segmento no usado
    pass


def tramos_se_superponen(pos_a1, pos_a2, pos_b1, pos_b2):
    """Revisa si dos tramos comparten segmentos (bajar y subir en la misma ciudad no se cruza)."""
    # TODO: comparar rangos de posiciones
    pass


# ==========================================
# REQUERIMIENTOS FUNCIONALES (RF05, RF06, RF07)
# ==========================================


def reutilizacion_de_asientos_por_tramo(pasajes, id_viaje, asiento, id_origen, id_destino):
    """RF06: Valida si un asiento está libre en el tramo cruzando tramos de pasajes vigentes."""
    # TODO: revisar pasajes vigentes del mismo viaje y asiento, y comprobar si se superponen
    pass


def VentasDePasajes(pasajes, id_cliente, id_viaje, id_origen, id_destino, asiento):
    """RF05: Registra un pasaje validando cliente, viaje, capacidad, sentido, tramo y precio."""
    # TODO: validar existencia de cliente/viaje/bus, asiento dentro de capacidad, sentido del viaje,
    # reutilización del asiento (RF06), calcular tarifa y guardar pasaje VIGENTE
    pass


def anulacionDePasajes(pasajes, id_pasaje):
    """RF07: Anula un pasaje vigente por ID evitando anulaciones repetidas."""
    # TODO: buscar pasaje, verificar que no esté ANULADO, cambiar estado a ANULADO y guardar
    pass