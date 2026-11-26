
# archivo creado por ALEJANDRO JARPA
# Temporalmente en uso, se reescribirá para mejorar la legibilidad y la estructura del código.
# haciendo uso del archivo estilos_ui.py para centralizar los estilos de la interfaz de usuario y mejorar la consistencia en toda la aplicación.


import os
from colorama import Fore, Style, init
from controladores.nominas_controller import listaViajes, obtenerNombreCiudadPorId, obtenerNomina

init(autoreset=True)


def limpiar_pantalla():
    os.system("cls")


def _mostrar_lista_viajes(viajes: list):
    print(Fore.CYAN + Style.BRIGHT + "=" * 78)
    print(Fore.CYAN + Style.BRIGHT + "LISTA DE VIAJES DISPONIBLES".center(78))
    print(Fore.CYAN + Style.BRIGHT + "=" * 78)

    if not viajes:
        print(Fore.MAGENTA + "No hay viajes registrados.")
        print(Fore.CYAN + "=" * 78)
        return

    for v in viajes:
        id_viaje = v[0]
        id_bus = v[1]
        fecha = v[2]
        hora = v[3]
        origen = obtenerNombreCiudadPorId(v[4]) or f"ID {v[4]}"
        destino = obtenerNombreCiudadPorId(v[5]) or f"ID {v[5]}"
        tarifa = v[6]

        print(
            Fore.YELLOW + Style.BRIGHT + f"ID Viaje: {id_viaje}" + Style.RESET_ALL
            + f" | Bus ID: {id_bus}"
            + f" | Fecha: {fecha}"
            + f" | Hora: {hora}"
        )
        print(f"   Ruta: {origen} -> {destino} | Tarifa base: ${tarifa}")
        print(Fore.WHITE + "-" * 78)


def _mostrar_nomina_formateada(nomina: dict):
    viaje = nomina["viaje"]
    bus = nomina["bus"]
    pasajeros = nomina["pasajeros"]
    orden = nomina["orden"]

    textos_orden = {
        "a": "Apellido paterno (A-Z)",
        "b": "Nombres (A-Z)",
        "c": "Número de asiento (ascendente)",
    }

    print(Fore.CYAN + Style.BRIGHT + "=" * 86)
    print(Fore.CYAN + Style.BRIGHT + "RUTASUR TRANSPORTES - NÓMINA DE PASAJEROS".center(86))
    print(Fore.CYAN + Style.BRIGHT + "=" * 86)

    print(
        Fore.YELLOW + Style.BRIGHT
        + f"BUS: [{bus['patente']}] (ID {bus['id_bus']}) | "
        + f"Capacidad: {bus['capacidad']} | Estado: {bus['estado']}"
    )
    print(
        Fore.GREEN + Style.BRIGHT
        + f"VIAJE #{viaje['id_viaje']} | Fecha: {viaje['fecha']} | Hora: {viaje['hora']} | "
        + f"Tarifa base: ${viaje['tarifa_base']}"
    )
    print(f"Ruta del viaje: {viaje['origen']} -> {viaje['destino']}")
    print(f"Orden aplicado: {textos_orden.get(orden, orden)}")
    print(Fore.CYAN + "-" * 86)

    if not pasajeros:
        print(Fore.MAGENTA + "No hay pasajeros emitidos para este viaje.")
        print(Fore.CYAN + "=" * 86)
        return

    encabezado = (
        f"{'ASIENTO':<8} | {'APELLIDO PATERNO':<18} | {'APELLIDO MATERNO':<18} | "
        f"{'NOMBRES':<20} | {'EMBARQUE -> DESTINO'}"
    )
    print(Fore.WHITE + Style.BRIGHT + encabezado)
    print(Fore.WHITE + "-" * 86)

    for p in pasajeros:
        asiento = str(p["asiento"]).ljust(8)
        ap_pat = str(p["apellido_paterno"])[:18].ljust(18)
        ap_mat = str(p["apellido_materno"])[:18].ljust(18)
        nombres = str(p["nombres"])[:20].ljust(20)
        tramo = f"{p['ciudad_embarque']} -> {p['destino_final']}"

        print(f"{asiento} | {ap_pat} | {ap_mat} | {nombres} | {tramo}")

    print(Fore.CYAN + "-" * 86)
    print(
        Fore.GREEN + Style.BRIGHT
        + f"Total pasajeros: {len(pasajeros)} / {bus['capacidad']}"
    )
    print(Fore.CYAN + "=" * 86)


def _pedir_orden_viaje(viaje_seleccionado: list) -> str:
    while True:
        limpiar_pantalla()
        print(Fore.CYAN + Style.BRIGHT + f"VIAJE SELECCIONADO: #{viaje_seleccionado[0]}")
        print(Fore.CYAN + Style.BRIGHT + "SELECCIONE TIPO DE ORDENAMIENTO")
        print(Fore.CYAN + "-" * 45)
        print(Fore.WHITE + "(a) Apellido paterno alfabético ascendente")
        print(Fore.WHITE + "(b) Nombres alfabético ascendente")
        print(Fore.WHITE + "(c) Número de asiento numérico ascendente")
        print(Fore.RED + "(0) Volver a elegir viaje")

        op = input("Seleccione opción (a/b/c/0): ").strip().lower()

        if op in ("a", "b", "c", "0"):
            return op

        limpiar_pantalla()
        print(Fore.RED + Style.BRIGHT + "Opción inválida. Ingrese a, b, c o 0.")
        op = input("Presione Enter para continuar...")


def opcion_5_nomina():
    while True:
        limpiar_pantalla()
        viajes = listaViajes()
        _mostrar_lista_viajes(viajes)

        print(Fore.WHITE + "\nIngrese el ID del viaje (o '0' para volver al menú principal):")
        op = input("ID del viaje: ").strip()

        if op == "0":
            return

        viaje_seleccionado = None
        for v in viajes:
            if str(v[0]).strip() == op:
                viaje_seleccionado = v
                break

        if viaje_seleccionado is None:
            limpiar_pantalla()
            print(Fore.RED + Style.BRIGHT + f"No se encontró un viaje con ID '{op}'.")
            op = input("Presione Enter para reintentar...")
            continue

        orden = _pedir_orden_viaje(viaje_seleccionado)
        if orden == "0":
            continue

        while True:
            nomina = obtenerNomina(viaje_seleccionado, orden)
            limpiar_pantalla()
            _mostrar_nomina_formateada(nomina)

            print(Fore.YELLOW + "\n¿Qué desea hacer ahora?")
            print(Fore.WHITE + "(1) Reordenar la nómina de este viaje")
            print(Fore.WHITE + "(2) Buscar otro viaje")
            print(Fore.RED + "(0) Salir al menú principal")

            op = input("Seleccione una opción: ").strip()

            if op == "1":
                nuevo_orden = _pedir_orden_viaje(viaje_seleccionado)
                if nuevo_orden != "0":
                    orden = nuevo_orden
            elif op == "2":
                break
            elif op == "0":
                return
            else:
                limpiar_pantalla()
                print(Fore.RED + Style.BRIGHT + "Opción inválida.")
                op = input("Presione Enter para continuar...")