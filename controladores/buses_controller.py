from typing import List, Optional
from modelos.entidades import Bus
from ruta_datos import ARCHIVO_BUSES, ENCODE


def _asegurar_archivo_buses() -> None:
    try:
        with open(ARCHIVO_BUSES, "r", encoding=ENCODE):
            return
    except FileNotFoundError:
        with open(ARCHIVO_BUSES, "w", encoding=ENCODE) as f:
            f.write("id_bus,patente,capacidad,estado\n")
    except OSError as exc:
        raise RuntimeError(f"No se pudo acceder al archivo de buses: {exc}") from exc
    

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

            bus = Bus(
                id_bus=int(partes[0].strip()),
                patente=partes[1].strip().upper(),
                capacidad=int(partes[2].strip()),
                estado=partes[3].strip().lower(),
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