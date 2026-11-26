from typing import List, Optional

from modelos.entidades import Ciudad
from ruta_datos import ARCHIVO_CIUDADES, ENCODE


def _verificar_archivo_ciudades() -> None:
    try:
        with open(ARCHIVO_CIUDADES, "r", encoding=ENCODE):
            return
    except FileNotFoundError as exc:
        raise RuntimeError(f"No se encontró el archivo de ciudades: {ARCHIVO_CIUDADES}") from exc
    except OSError as exc:
        raise RuntimeError(f"No se pudo acceder al archivo de ciudades: {exc}") from exc


def listar_ciudades() -> List[Ciudad]:
    _verificar_archivo_ciudades()
    ciudades: List[Ciudad] = []

    try:
        with open(ARCHIVO_CIUDADES, "r", encoding=ENCODE) as f:
            lineas = f.readlines()

        for linea in lineas[1:]:
            linea_limpia = linea.strip()
            if linea_limpia == "":
                continue
            partes = linea_limpia.split(",")
            if len(partes) < 3:
                continue

            ciudad = Ciudad(
                id_ciudad=int(partes[0].strip()),
                nombre=partes[1].strip(),
                posicion=int(partes[2].strip()),
            )
            ciudades.append(ciudad)
    except (OSError, ValueError) as exc:
        raise RuntimeError(f"Error al leer ciudades: {exc}") from exc

    return ciudades


def buscar_ciudad_por_id(id_ciudad: int) -> Optional[Ciudad]:
    ciudades: List[Ciudad] = listar_ciudades()
    for ciudad in ciudades:
        if ciudad.id_ciudad == id_ciudad:
            return ciudad
    return None


def buscar_ciudad_por_nombre(nombre: str) -> Optional[Ciudad]:
    nombre_buscado = nombre.strip().lower()
    if nombre_buscado == "":
        return None

    ciudades: List[Ciudad] = listar_ciudades()
    for ciudad in ciudades:
        if ciudad.nombre.strip().lower() == nombre_buscado:
            return ciudad
    return None