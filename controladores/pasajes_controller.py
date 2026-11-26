from typing import List
from modelos.entidades import Pasaje
from ruta_datos import ARCHIVO_PASAJES, ENCODE


def _asegurar_archivo_pasajes() -> None:
    try:
        with open(ARCHIVO_PASAJES, "r", encoding=ENCODE):
            return
    except FileNotFoundError:
        with open(ARCHIVO_PASAJES, "w", encoding=ENCODE) as f:
            f.write("id_pasaje,id_viaje,id_cliente,id_origen,id_destino,asiento,valor,estado\n")
    except OSError as exc:
        raise RuntimeError(f"No se pudo acceder al archivo de pasajes: {exc}") from exc


def listar_pasajes() -> List[Pasaje]:
    _asegurar_archivo_pasajes()
    pasajes: List[Pasaje] = []
    try:
        with open(ARCHIVO_PASAJES, "r", encoding=ENCODE) as f:
            lineas = f.readlines()

        for linea in lineas[1:]:
            linea_limpia = linea.strip()
            if linea_limpia == "":
                continue
            partes = linea_limpia.split(",")
            if len(partes) < 8:
                continue

            pasaje = Pasaje(
                id_pasaje=int(partes[0].strip()),
                id_viaje=int(partes[1].strip()),
                id_cliente=int(partes[2].strip()),
                id_origen=int(partes[3].strip()),
                id_destino=int(partes[4].strip()),
                asiento=int(partes[5].strip()),
                valor=int(partes[6].strip()),
                estado=partes[7].strip().lower(),
            )
            pasajes.append(pasaje)
    except (OSError, ValueError) as exc:
        raise RuntimeError(f"Error al leer pasajes: {exc}") from exc

    return pasajes