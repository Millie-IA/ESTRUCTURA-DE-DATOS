from typing import List, Optional

from controladores.buses_controller import buscar_bus_por_id
from controladores.ciudades_controller import (
    buscar_ciudad_por_id,
    buscar_ciudad_por_nombre,
    listar_ciudades,
)
from controladores.clientes_controller import buscar_cliente_por_id
from controladores.viajes_controller import buscar_viaje_por_id
from modelos.entidades import Ciudad, Pasaje, Viaje
from ruta_datos import ARCHIVO_PASAJES, ENCODE

CABECERA_PASAJES = "id_pasaje,id_viaje,id_cliente,id_origen,id_destino,asiento,valor,estado\n"


def _asegurar_archivo_pasajes() -> None:
    try:
        with open(ARCHIVO_PASAJES, "r", encoding=ENCODE):
            return
    except FileNotFoundError:
        with open(ARCHIVO_PASAJES, "w", encoding=ENCODE) as f:
            f.write(CABECERA_PASAJES)
    except OSError as exc:
        raise RuntimeError(f"No se pudo acceder al archivo de pasajes: {exc}") from exc


def _es_venta_vigente(pasaje: Pasaje) -> bool:
    return pasaje.estado.strip().lower() == "vigente"


def _obtener_siguiente_id(pasajes: List[Pasaje]) -> int:
    mayor_id = 0
    for pasaje in pasajes:
        if pasaje.id_pasaje > mayor_id:
            mayor_id = pasaje.id_pasaje
    return mayor_id + 1


def _obtener_ciudades_recorrido_ordenadas(viaje: Viaje) -> List[Ciudad]:
    todas_ciudades: List[Ciudad] = listar_ciudades()
    ciudad_ini = buscar_ciudad_por_nombre(viaje.ciudad_inicial)
    ciudad_fin = buscar_ciudad_por_nombre(viaje.ciudad_final)

    if ciudad_ini is None or ciudad_fin is None:
        return todas_ciudades

    min_pos = min(ciudad_ini.posicion, ciudad_fin.posicion)
    max_pos = max(ciudad_ini.posicion, ciudad_fin.posicion)
    avanza_subiendo = ciudad_fin.posicion >= ciudad_ini.posicion

    ciudades_en_rango: List[Ciudad] = []
    for ciudad in todas_ciudades:
        if min_pos <= ciudad.posicion <= max_pos:
            ciudades_en_rango.append(ciudad)

    return sorted(
        ciudades_en_rango,
        key=lambda c: c.posicion,
        reverse=not avanza_subiendo,
    )


def obtener_ciudades_origen_viaje(id_viaje: int) -> List[Ciudad]:
    viaje = buscar_viaje_por_id(id_viaje)
    if viaje is None:
        raise ValueError(f"No existe un viaje programado con el ID {id_viaje}.")

    recorrido = _obtener_ciudades_recorrido_ordenadas(viaje)
    if len(recorrido) > 1:
        return recorrido[:-1]
    return recorrido


def obtener_ciudades_destino_restantes(id_viaje: int, id_origen: int) -> List[Ciudad]:
    viaje = buscar_viaje_por_id(id_viaje)
    if viaje is None:
        raise ValueError(f"No existe un viaje programado con el ID {id_viaje}.")

    ciudad_origen = buscar_ciudad_por_id(id_origen)
    if ciudad_origen is None:
        raise ValueError(f"No existe una ciudad de origen con el ID {id_origen}.")

    ciudad_ini = buscar_ciudad_por_nombre(viaje.ciudad_inicial)
    ciudad_fin = buscar_ciudad_por_nombre(viaje.ciudad_final)
    avanza_subiendo = True
    if ciudad_ini is not None and ciudad_fin is not None:
        avanza_subiendo = ciudad_fin.posicion >= ciudad_ini.posicion

    recorrido = _obtener_ciudades_recorrido_ordenadas(viaje)
    restantes: List[Ciudad] = []
    for ciudad in recorrido:
        if avanza_subiendo and ciudad.posicion > ciudad_origen.posicion:
            restantes.append(ciudad)
        elif not avanza_subiendo and ciudad.posicion < ciudad_origen.posicion:
            restantes.append(ciudad)

    return restantes


def _rango_tramo_ordenado(id_origen: int, id_destino: int) -> Optional[tuple[int, int]]:
    ciudad_origen = buscar_ciudad_por_id(id_origen)
    ciudad_destino = buscar_ciudad_por_id(id_destino)
    if ciudad_origen is None or ciudad_destino is None:
        return None

    pos_a = ciudad_origen.posicion
    pos_b = ciudad_destino.posicion
    if pos_a == pos_b:
        return None
    return (min(pos_a, pos_b), max(pos_a, pos_b))


def _tramos_se_cruzan(
    origen_1: int,
    destino_1: int,
    origen_2: int,
    destino_2: int,
) -> bool:
    rango_1 = _rango_tramo_ordenado(origen_1, destino_1)
    rango_2 = _rango_tramo_ordenado(origen_2, destino_2)

    if rango_1 is None or rango_2 is None:
        return True

    inicio_cruce = max(rango_1[0], rango_2[0])
    fin_cruce = min(rango_1[1], rango_2[1])
    return inicio_cruce < fin_cruce


def obtener_asientos_disponibles(
    id_viaje: int,
    id_origen: Optional[int] = None,
    id_destino: Optional[int] = None,
) -> List[int]:
    viaje = buscar_viaje_por_id(id_viaje)
    if viaje is None:
        raise ValueError(f"No existe un viaje programado con el ID {id_viaje}.")

    bus = buscar_bus_por_id(viaje.id_bus)
    if bus is None:
        raise ValueError(f"No se encontró el bus asociado al viaje (ID {viaje.id_bus}).")

    pasajes_actuales: List[Pasaje] = listar_pasajes()
    ocupados: List[int] = []

    for pasaje in pasajes_actuales:
        if pasaje.id_viaje != id_viaje:
            continue
        if not _es_venta_vigente(pasaje):
            continue

        if id_origen is not None and id_destino is not None:
            if _tramos_se_cruzan(id_origen, id_destino, pasaje.id_origen, pasaje.id_destino):
                ocupados.append(pasaje.asiento)
        else:
            ocupados.append(pasaje.asiento)

    disponibles: List[int] = []
    for numero_asiento in range(1, bus.capacidad + 1):
        esta_ocupado = False
        for asiento_ocupado in ocupados:
            if asiento_ocupado == numero_asiento:
                esta_ocupado = True
                break
        if not esta_ocupado:
            disponibles.append(numero_asiento)

    disponibles.sort()
    return disponibles


def _validar_tramo_en_viaje(viaje: Viaje, id_origen: int, id_destino: int) -> tuple[Ciudad, Ciudad]:
    if id_origen == id_destino:
        raise ValueError("El origen y el destino del pasajero deben ser distintos.")

    ciudad_origen = buscar_ciudad_por_id(id_origen)
    if ciudad_origen is None:
        raise ValueError(f"No existe una ciudad de origen con el ID {id_origen}.")

    ciudad_destino = buscar_ciudad_por_id(id_destino)
    if ciudad_destino is None:
        raise ValueError(f"No existe una ciudad de destino con el ID {id_destino}.")

    ciudad_ini = buscar_ciudad_por_nombre(viaje.ciudad_inicial)
    ciudad_fin = buscar_ciudad_por_nombre(viaje.ciudad_final)

    if ciudad_ini is not None and ciudad_fin is not None:
        sentido_viaje = ciudad_fin.posicion - ciudad_ini.posicion
        sentido_tramo = ciudad_destino.posicion - ciudad_origen.posicion

        if sentido_viaje > 0:
            if (
                sentido_tramo <= 0
                or ciudad_origen.posicion < ciudad_ini.posicion
                or ciudad_destino.posicion > ciudad_fin.posicion
            ):
                raise ValueError(
                    f"El tramo {ciudad_origen.nombre} -> {ciudad_destino.nombre} no respeta "
                    f"el sentido del viaje ({viaje.ciudad_inicial} -> {viaje.ciudad_final})."
                )
        elif sentido_viaje < 0:
            if (
                sentido_tramo >= 0
                or ciudad_origen.posicion > ciudad_ini.posicion
                or ciudad_destino.posicion < ciudad_fin.posicion
            ):
                raise ValueError(
                    f"El tramo {ciudad_origen.nombre} -> {ciudad_destino.nombre} no respeta "
                    f"el sentido del viaje ({viaje.ciudad_inicial} -> {viaje.ciudad_final})."
                )

    return ciudad_origen, ciudad_destino


def _validar_asiento(
    viaje: Viaje,
    asiento: int,
    id_origen: int,
    id_destino: int,
    pasajes_existentes: List[Pasaje],
) -> int:
    if isinstance(asiento, bool) or not isinstance(asiento, int):
        raise ValueError("El número de asiento debe ser un entero.")

    bus = buscar_bus_por_id(viaje.id_bus)
    if bus is None:
        raise ValueError(f"No se encontró el bus asociado al viaje (ID {viaje.id_bus}).")

    if asiento < 1 or asiento > bus.capacidad:
        raise ValueError(
            f"El asiento {asiento} está fuera de la capacidad del bus (1 a {bus.capacidad})."
        )

    for pasaje in pasajes_existentes:
        if (
            pasaje.id_viaje == viaje.id_viaje
            and pasaje.asiento == asiento
            and _es_venta_vigente(pasaje)
            and _tramos_se_cruzan(id_origen, id_destino, pasaje.id_origen, pasaje.id_destino)
        ):
            raise ValueError(
                f"El asiento {asiento} ya está ocupado en un tramo superpuesto del viaje {viaje.id_viaje}."
            )

    return asiento


def calcular_valor_pasaje(viaje: Viaje, ciudad_origen: Ciudad, ciudad_destino: Ciudad) -> int:
    ciudad_ini = buscar_ciudad_por_nombre(viaje.ciudad_inicial)
    ciudad_fin = buscar_ciudad_por_nombre(viaje.ciudad_final)

    if ciudad_ini is not None and ciudad_fin is not None:
        distancia_viaje = abs(ciudad_fin.posicion - ciudad_ini.posicion)
        distancia_tramo = abs(ciudad_destino.posicion - ciudad_origen.posicion)
        if distancia_viaje > 0 and distancia_tramo < distancia_viaje:
            proporcion = distancia_tramo / distancia_viaje
            return max(1, int(round(viaje.tarifa_base * proporcion)))

    return int(viaje.tarifa_base)


def _guardar_pasaje(pasaje: Pasaje) -> None:
    _asegurar_archivo_pasajes()
    linea = (
        f"{pasaje.id_pasaje},{pasaje.id_viaje},{pasaje.id_cliente},"
        f"{pasaje.id_origen},{pasaje.id_destino},{pasaje.asiento},{pasaje.valor},{pasaje.estado}\n"
    )
    try:
        with open(ARCHIVO_PASAJES, "a", encoding=ENCODE) as f:
            f.write(linea)
    except OSError as exc:
        raise RuntimeError(f"No se pudo guardar el pasaje: {exc}") from exc


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
                estado=partes[7].strip(),
            )
            pasajes.append(pasaje)
    except (OSError, ValueError) as exc:
        raise RuntimeError(f"Error al leer pasajes: {exc}") from exc

    return pasajes


def buscar_pasaje_por_id(id_pasaje: int) -> Optional[Pasaje]:
    pasajes: List[Pasaje] = listar_pasajes()
    for pasaje in pasajes:
        if pasaje.id_pasaje == id_pasaje:
            return pasaje
    return None


def registrar_pasaje(
    id_cliente: int,
    id_viaje: int,
    id_origen: int,
    id_destino: int,
    asiento: int,
) -> Pasaje:
    if isinstance(id_cliente, bool) or not isinstance(id_cliente, int) or id_cliente <= 0:
        raise ValueError("El ID del cliente debe ser un entero positivo.")
    if isinstance(id_viaje, bool) or not isinstance(id_viaje, int) or id_viaje <= 0:
        raise ValueError("El ID del viaje debe ser un entero positivo.")

    cliente = buscar_cliente_por_id(id_cliente)
    if cliente is None:
        raise ValueError(f"No existe un cliente registrado con el ID {id_cliente}.")

    viaje = buscar_viaje_por_id(id_viaje)
    if viaje is None:
        raise ValueError(f"No existe un viaje programado con el ID {id_viaje}.")

    ciudad_origen, ciudad_destino = _validar_tramo_en_viaje(viaje, id_origen, id_destino)

    pasajes_actuales: List[Pasaje] = listar_pasajes()
    asiento_valido = _validar_asiento(
        viaje,
        asiento,
        ciudad_origen.id_ciudad,
        ciudad_destino.id_ciudad,
        pasajes_actuales,
    )
    valor_calculado = calcular_valor_pasaje(viaje, ciudad_origen, ciudad_destino)

    nuevo_id = _obtener_siguiente_id(pasajes_actuales)
    nuevo_pasaje = Pasaje(
        id_pasaje=nuevo_id,
        id_viaje=id_viaje,
        id_cliente=id_cliente,
        id_origen=ciudad_origen.id_ciudad,
        id_destino=ciudad_destino.id_ciudad,
        asiento=asiento_valido,
        valor=valor_calculado,
        estado="vigente",
    )
    _guardar_pasaje(nuevo_pasaje)
    return nuevo_pasaje