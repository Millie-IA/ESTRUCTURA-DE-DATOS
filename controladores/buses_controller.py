from typing import List, Optional

from modelos.entidades import Bus
from ruta_datos import ARCHIVO_BUSES, ENCODE

ESTADOS_VALIDOS = ("disponible", "no disponible")


def _asegurar_archivo_buses() -> None:
    try:
        with open(ARCHIVO_BUSES, "r", encoding=ENCODE):
            return
    except FileNotFoundError:
        with open(ARCHIVO_BUSES, "w", encoding=ENCODE) as f:
            f.write("id_bus,patente,capacidad,estado\n")
    except OSError as exc:
        raise RuntimeError(f"No se pudo acceder al archivo de buses: {exc}") from exc


def _limpiar_patente(patente: str) -> str:
    limpia = patente.strip().upper()
    limpia = limpia.replace("-", "").replace(" ", "").replace(".", "")
    return limpia


def _validar_patente(patente: str) -> str:
    limpia = _limpiar_patente(patente)
    if len(limpia) < 5 or len(limpia) > 8:
        raise ValueError("La patente debe tener entre 5 y 8 caracteres.")
    if not limpia.isalnum():
        raise ValueError("La patente solo puede contener letras y números.")
    return limpia


def _validar_capacidad(capacidad: int) -> int:
    if isinstance(capacidad, bool) or not isinstance(capacidad, int):
        raise ValueError("La capacidad debe ser un número entero.")
    if capacidad <= 0:
        raise ValueError("La capacidad debe ser un número entero positivo mayor que 0.")
    return capacidad


def _normalizar_estado(estado: str) -> str:
    limpio = estado.strip().lower()
    if limpio in ("disponible", "activo", "activa", "libre", "1", "si", "sí"):
        return "disponible"
    if limpio in ("no disponible", "nodisponible", "inactivo", "inactiva", "ocupado", "0", "no"):
        return "no disponible"
    raise ValueError(
        "Estado inválido. Use 'disponible' o 'no disponible'."
    )


def _obtener_siguiente_id(buses: List[Bus]) -> int:
    mayor_id = 0
    for bus in buses:
        if bus.id_bus > mayor_id:
            mayor_id = bus.id_bus
    return mayor_id + 1


def _guardar_bus(bus: Bus) -> None:
    _asegurar_archivo_buses()
    linea = f"{bus.id_bus},{bus.patente},{bus.capacidad},{bus.estado}\n"
    try:
        with open(ARCHIVO_BUSES, "a", encoding=ENCODE) as f:
            f.write(linea)
    except OSError as exc:
        raise RuntimeError(f"No se pudo guardar el bus: {exc}") from exc


def listar_buses() -> List[Bus]:
    _asegurar_archivo_buses()
    buses: List[Bus] = []
    try:
        with open(ARCHIVO_BUSES, "r", encoding=ENCODE) as f:
            lineas = f.readlines()

        for linea in lineas[1:]:
            linea_limpia = linea.strip()
            if linea_limpia == "":
                continue
            partes = linea_limpia.split(",")
            if len(partes) < 4:
                continue

            estado_csv = _normalizar_estado(partes[3])
            bus = Bus(
                id_bus=int(partes[0].strip()),
                patente=_limpiar_patente(partes[1]),
                capacidad=int(partes[2].strip()),
                estado=estado_csv,
            )
            buses.append(bus)
    except (OSError, ValueError) as exc:
        raise RuntimeError(f"Error al leer buses: {exc}") from exc

    return buses


def buscar_bus_por_id(id_bus: int) -> Optional[Bus]:
    buses: List[Bus] = listar_buses()
    for bus in buses:
        if bus.id_bus == id_bus:
            return bus
    return None


def buscar_bus_por_patente(patente: str) -> Optional[Bus]:
    patente_buscada = _limpiar_patente(patente)
    if patente_buscada == "":
        return None

    buses: List[Bus] = listar_buses()
    for bus in buses:
        patente_actual = _limpiar_patente(bus.patente)
        if patente_actual == patente_buscada:
            return bus
    return None


def registrar_bus(patente: str, capacidad: int, estado: str = "disponible") -> Bus:
    patente_valida = _validar_patente(patente)
    capacidad_valida = _validar_capacidad(capacidad)
    estado_valido = _normalizar_estado(estado)

    buses_actuales: List[Bus] = listar_buses()
    for bus_existente in buses_actuales:
        patente_existente = _limpiar_patente(bus_existente.patente)
        if patente_existente == patente_valida:
            raise ValueError(f"Ya existe un bus registrado con la patente {patente_valida}.")

    nuevo_id = _obtener_siguiente_id(buses_actuales)
    nuevo_bus = Bus(
        id_bus=nuevo_id,
        patente=patente_valida,
        capacidad=capacidad_valida,
        estado=estado_valido,
    )
    _guardar_bus(nuevo_bus)
    return nuevo_bus