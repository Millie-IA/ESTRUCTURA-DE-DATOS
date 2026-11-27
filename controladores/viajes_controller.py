from typing import List, Optional

from controladores.buses_controller import buscar_bus_por_id
from modelos.entidades import Viaje
from ruta_datos import ARCHIVO_VIAJES, ENCODE


def _asegurar_archivo_viajes() -> None:
    try:
        with open(ARCHIVO_VIAJES, "r", encoding=ENCODE):
            return
    except FileNotFoundError:
        with open(ARCHIVO_VIAJES, "w", encoding=ENCODE) as f:
            f.write("id_viaje,id_bus,fecha,hora,ciudad_inicial,ciudad_final,tarifa_base\n")
    except OSError as exc:
        raise RuntimeError(f"No se pudo acceder al archivo de viajes: {exc}") from exc


def _obtener_ciudades_por_direccion(direccion: int) -> tuple[str, str]:
    if direccion == 1:
        return "Concepción", "Santiago"
    if direccion == 2:
        return "Santiago", "Concepción"
    raise ValueError("Dirección inválida. Use 1 para Concepción -> Santiago o 2 para Santiago -> Concepción.")


def _validar_fecha(fecha: str) -> str:
    limpia = fecha.strip()
    partes = limpia.split("-")
    if len(partes) != 3:
        raise ValueError("La fecha debe tener el formato AAAA-MM-DD (ej: 2026-12-01).")

    anio_str, mes_str, dia_str = partes[0].strip(), partes[1].strip(), partes[2].strip()
    if len(anio_str) != 4 or len(mes_str) != 2 or len(dia_str) != 2:
        raise ValueError("La fecha debe tener el formato AAAA-MM-DD (ej: 2026-12-01).")

    if not (anio_str.isdigit() and mes_str.isdigit() and dia_str.isdigit()):
        raise ValueError("La fecha solo puede contener dígitos y guiones (AAAA-MM-DD).")

    anio = int(anio_str)
    mes = int(mes_str)
    dia = int(dia_str)

    if anio < 2020 or anio > 2100:
        raise ValueError("Año de fecha fuera de rango.")
    if mes < 1 or mes > 12:
        raise ValueError("El mes debe estar entre 01 y 12.")

    dias_por_mes = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    es_bisiesto = (anio % 4 == 0 and anio % 100 != 0) or (anio % 400 == 0)
    if es_bisiesto:
        dias_por_mes[1] = 29

    max_dias = dias_por_mes[mes - 1]
    if dia < 1 or dia > max_dias:
        raise ValueError(f"El día {dia:02d} no es válido para el mes {mes:02d}.")

    return f"{anio:04d}-{mes:02d}-{dia:02d}"


def _validar_hora(hora: str) -> str:
    limpia = hora.strip()
    partes = limpia.split(":")
    if len(partes) != 2:
        raise ValueError("La hora debe tener el formato HH:MM (ej: 08:30).")

    hh_str, mm_str = partes[0].strip(), partes[1].strip()
    if len(hh_str) != 2 or len(mm_str) != 2:
        raise ValueError("La hora debe tener el formato HH:MM (ej: 08:30).")

    if not (hh_str.isdigit() and mm_str.isdigit()):
        raise ValueError("La hora solo puede contener dígitos y dos puntos (HH:MM).")

    hh = int(hh_str)
    mm = int(mm_str)

    if hh < 0 or hh > 23:
        raise ValueError("La hora debe estar entre 00 y 23.")
    if mm < 0 or mm > 59:
        raise ValueError("Los minutos deben estar entre 00 y 59.")

    return f"{hh:02d}:{mm:02d}"


def _validar_tarifa_base(tarifa_base: int) -> int:
    if isinstance(tarifa_base, bool) or not isinstance(tarifa_base, int):
        raise ValueError("La tarifa base debe ser un número entero.")
    if tarifa_base <= 0:
        raise ValueError("La tarifa base debe ser mayor que 0.")
    return tarifa_base


def _obtener_siguiente_id(viajes: List[Viaje]) -> int:
    mayor_id = 0
    for viaje in viajes:
        if viaje.id_viaje > mayor_id:
            mayor_id = viaje.id_viaje
    return mayor_id + 1


def _guardar_viaje(viaje: Viaje) -> None:
    _asegurar_archivo_viajes()
    linea = (
        f"{viaje.id_viaje},{viaje.id_bus},{viaje.fecha},{viaje.hora},"
        f"{viaje.ciudad_inicial},{viaje.ciudad_final},{viaje.tarifa_base}\n"
    )
    try:
        with open(ARCHIVO_VIAJES, "a", encoding=ENCODE) as f:
            f.write(linea)
    except OSError as exc:
        raise RuntimeError(f"No se pudo guardar el viaje: {exc}") from exc


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
                ciudad_inicial=partes[4].strip(),
                ciudad_final=partes[5].strip(),
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


def programar_viaje(
    id_bus: int,
    fecha: str,
    hora: str,
    direccion: int,
    tarifa_base: int,
) -> Viaje:
    if isinstance(id_bus, bool) or not isinstance(id_bus, int) or id_bus <= 0:
        raise ValueError("El ID del bus debe ser un entero positivo.")

    bus = buscar_bus_por_id(id_bus)
    if bus is None:
        raise ValueError(f"No existe un bus registrado con el ID {id_bus}.")
    if bus.estado != "disponible":
        raise ValueError(f"El bus con ID {id_bus} no está disponible (estado: {bus.estado}).")

    fecha_valida = _validar_fecha(fecha)
    hora_valida = _validar_hora(hora)
    ciudad_inicial, ciudad_final = _obtener_ciudades_por_direccion(direccion)
    tarifa_valida = _validar_tarifa_base(tarifa_base)

    viajes_actuales: List[Viaje] = listar_viajes()
    for viaje_existente in viajes_actuales:
        if (
            viaje_existente.id_bus == id_bus
            and viaje_existente.fecha == fecha_valida
            and viaje_existente.hora == hora_valida
        ):
            raise ValueError(
                f"El bus ID {id_bus} ya tiene un viaje programado el {fecha_valida} a las {hora_valida}."
            )

    nuevo_id = _obtener_siguiente_id(viajes_actuales)
    nuevo_viaje = Viaje(
        id_viaje=nuevo_id,
        id_bus=id_bus,
        fecha=fecha_valida,
        hora=hora_valida,
        ciudad_inicial=ciudad_inicial,
        ciudad_final=ciudad_final,
        tarifa_base=tarifa_valida,
    )
    _guardar_viaje(nuevo_viaje)
    return nuevo_viaje