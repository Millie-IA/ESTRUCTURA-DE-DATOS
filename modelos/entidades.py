from dataclasses import dataclass


@dataclass
class Cliente:
    id_cliente: int
    rut: str
    nombres: str
    apellido_paterno: str
    apellido_materno: str
    contacto: str


@dataclass
class Bus:
    id_bus: int
    patente: str
    capacidad: int
    estado: str


@dataclass
class Ciudad:
    id_ciudad: int
    nombre: str
    posicion: int


@dataclass
class Viaje:
    id_viaje: int
    id_bus: int
    fecha: str
    hora: str
    id_origen: int
    id_destino: int
    tarifa_base: int


@dataclass
class Pasaje:
    id_pasaje: int
    id_viaje: int
    id_cliente: int
    id_origen: int
    id_destino: int
    asiento: int
    valor: int
    estado: str