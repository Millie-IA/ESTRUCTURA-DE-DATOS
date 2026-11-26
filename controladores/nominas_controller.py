
# Archivo creado por ALEJANDRO JARPA
# Este archivo controla todo lo que tiene que ver con la nomina de viajes, consumiendo datos desde los archivos
# Temporalmente en uso, se reescribirá para mejorar la legibilidad y la estructura del código.

import os
from ruta_datos import *


def listaViajes() -> list: # transcrita 
    viajes = []
    f = open(ARCHIVO_VIAJES, "r", encoding=ENCODE)
    lineas = f.readlines()
    f.close()

    for linea in lineas[1:]:
        linea_limpia = linea.strip()
        if linea_limpia == "":
            continue
        partes = linea_limpia.split(",")
        fila = [
            int(partes[0]),  # id_viaje
            int(partes[1]),  # id_bus
            partes[2],       # fecha
            partes[3],       # hora
            int(partes[4]),  # id_origen
            int(partes[5]),  # id_destino
            int(partes[6]),  # tarifa_base
        ]
        viajes.append(fila)

    return viajes

def obtenerBusDeViaje(id_bus_buscado: str) -> list: #transcrita

    f = open(ARCHIVO_BUSES, "r", encoding=ENCODE)
    lineas = f.readlines()
    f.close()

    for linea in lineas[1:]:
        linea_limpia = linea.strip()
        if linea_limpia == "":
            continue

        campos = linea_limpia.split(",")
        if campos[0].strip() == id_bus_buscado:
            return [
                int(campos[0]), # id_bus
                campos[1],      # patente
                int(campos[2]), # capacidad
                campos[3],      # estado
            ]

    return []


def obtenerPasajesDeViaje(viaje: list) -> list: 
    id_viaje_buscado = str(viaje[0]).strip()
    pasajes_viaje = []

    f = open(ARCHIVO_PASAJES, "r", encoding=ENCODE)
    lineas = f.readlines()
    f.close()

    for linea in lineas[1:]:
        linea_limpia = linea.strip()
        if linea_limpia == "":
            continue

        campos = linea_limpia.split(",")
        if campos[1].strip() == id_viaje_buscado:
            pasajes_viaje.append([
                int(campos[0]),  # id_pasaje
                int(campos[1]),  # id_viaje
                int(campos[2]),  # id_cliente
                int(campos[3]),  # id_origen
                int(campos[4]),  # id_destino
                int(campos[5]),  # asiento
                int(campos[6]),  # valor
                campos[7].strip(), # estado
            ])

    return pasajes_viaje


def obtenerClientePorId(id_cliente_buscado: int) -> list: #transcrita
    id_buscado = str(id_cliente_buscado).strip()

    f = open(ARCHIVO_CLIENTES, "r", encoding=ENCODE)
    lineas = f.readlines()
    f.close()

    for linea in lineas[1:]:
        linea_limpia = linea.strip()
        if linea_limpia == "":
            continue

        campos = linea_limpia.split(",")
        if campos[0].strip() == id_buscado:
            return [
                int(campos[0]),   # id_cliente
                campos[1].strip(), # rut
                campos[2].strip(), # nombres
                campos[3].strip(), # apellido_paterno
                campos[4].strip(), # apellido_materno
                campos[5].strip(), # contacto
            ]

    return []


def obtenerPasajerosDeViaje(viaje: list) -> list:
    pasajes = obtenerPasajesDeViaje(viaje)
    pasajeros = []

    for pasaje in pasajes:
        estado = pasaje[7].lower()
        if estado != "emitido":
            continue

        id_cliente = pasaje[2]
        cliente = obtenerClientePorId(id_cliente)
        if len(cliente) > 0:
            pasajeros.append(cliente)

    return pasajeros

def obtenerNombreCiudadPorId(id_ciudad_buscado: int) -> str:
    id_buscado = str(id_ciudad_buscado).strip()

    f = open(ARCHIVO_CIUDADES, "r", encoding=ENCODE)
    lineas = f.readlines()
    f.close()

    for linea in lineas[1:]:
        linea_limpia = linea.strip()
        if linea_limpia == "":
            continue

        campos = linea_limpia.split(",")
        if campos[0].strip() == id_buscado:
            return campos[1].strip()

    return ""

def _claveOrdenPasajero(pasajero: dict, orden: str):
    if orden == "a":
        return (
            pasajero["apellido_paterno"].lower(),
            pasajero["nombres"].lower(),
            pasajero["asiento"],
        )
    if orden == "b":
        return (
            pasajero["nombres"].lower(),
            pasajero["apellido_paterno"].lower(),
            pasajero["asiento"],
        )
    if orden == "c":
        return (
            pasajero["asiento"],
            pasajero["apellido_paterno"].lower(),
            pasajero["nombres"].lower(),
        )
    raise ValueError("Tipo de ordenamiento no válido. Use 'a', 'b' o 'c'.")

def obtenerNomina(viaje: list, orden: str = "c") -> dict:
    orden_limpio = orden.strip().lower()
    if orden_limpio not in ("a", "b", "c"):
        raise ValueError("Tipo de ordenamiento no válido. Use 'a', 'b' o 'c'.")

    bus = obtenerBusDeViaje(viaje)
    pasajes = obtenerPasajesDeViaje(viaje)

    origen_viaje = obtenerNombreCiudadPorId(viaje[4])
    destino_viaje = obtenerNombreCiudadPorId(viaje[5])

    datos_viaje = {
        "id_viaje": viaje[0],
        "id_bus": viaje[1],
        "fecha": viaje[2],
        "hora": viaje[3],
        "id_origen": viaje[4],
        "origen": origen_viaje,
        "id_destino": viaje[5],
        "destino": destino_viaje,
        "tarifa_base": viaje[6],
    }

    datos_bus = {
        "id_bus": bus[0] if len(bus) > 0 else viaje[1],
        "patente": bus[1] if len(bus) > 1 else "",
        "capacidad": bus[2] if len(bus) > 2 else 0,
        "estado": bus[3] if len(bus) > 3 else "",
    }

    pasajeros_nomina = []
    for pasaje in pasajes:
        if pasaje[7].lower() != "emitido":
            continue

        cliente = obtenerClientePorId(pasaje[2])
        if len(cliente) == 0:
            continue

        ciudad_embarque = obtenerNombreCiudadPorId(pasaje[3])
        destino_final = obtenerNombreCiudadPorId(pasaje[4])

        pasajeros_nomina.append({
            "asiento": int(pasaje[5]),
            "apellido_paterno": cliente[3],
            "apellido_materno": cliente[4],
            "nombres": cliente[2],
            "ciudad_embarque": ciudad_embarque,
            "destino_final": destino_final,
            "rut": cliente[1],
            "estado_pasaje": pasaje[7],
        })

    pasajeros_nomina.sort(key=lambda p: _claveOrdenPasajero(p, orden_limpio))

    return {
        "orden": orden_limpio,
        "viaje": datos_viaje,
        "bus": datos_bus,
        "pasajeros": pasajeros_nomina,
    }

