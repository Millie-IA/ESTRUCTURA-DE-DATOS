
# Este archivo controla todo lo que tiene que ver con los viajes como entidad

from typing import List
from modelos.entidades import Viaje
from ruta_datos import ARCHIVO_VIAJES, ENCODE


def _asegurar_archivo_viajes() -> None:
    try:
        with open(ARCHIVO_VIAJES, "r", encoding=ENCODE):
            return
    except FileNotFoundError:
        with open(ARCHIVO_VIAJES, "w", encoding=ENCODE) as f:
            f.write("id_viaje,id_bus,fecha,hora,id_origen,id_destino,tarifa_base\n")
    except OSError as exc:
        raise RuntimeError(f"No se pudo acceder al archivo de viajes: {exc}") from exc


def listar_viajes() -> List[Viaje]:
    _asegurar_archivo_viajes()
    viajes: List[Viaje] = []
    try:
        with open(ARCHIVO_VIAJES, "r", encoding=ENCODE) as f:
            lineas = f.readlines()

        for linea in lineas[1:]:
            linea_limpia = linea.strip()
            if linea_limpia == "":
                continue
            partes = linea_limpia.split(",")
            if len(partes) < 7:
                continue

            viaje = Viaje(
                id_viaje=int(partes[0].strip()),
                id_bus=int(partes[1].strip()),
                fecha=partes[2].strip(),
                hora=partes[3].strip(),
                id_origen=int(partes[4].strip()),
                id_destino=int(partes[5].strip()),
                tarifa_base=int(partes[6].strip()),
            )
            viajes.append(viaje)
    except (OSError, ValueError) as exc:
        raise RuntimeError(f"Error al leer viajes: {exc}") from exc

    return viajes

def buscar_viaje_por_id(id_viaje: int) -> Optional[Viaje]:
    viajes: List[Viaje] = listar_viajes()
    for viaje in viajes:
        if viaje.id_viaje == id_viaje:
            return viaje
    return None