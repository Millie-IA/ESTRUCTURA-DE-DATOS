from typing import List

from controladores.ciudades_controller import buscar_ciudad_por_id
from controladores.clientes_controller import buscar_cliente_por_id
from controladores.pasajes_controller import (
    buscar_pasaje_por_id,
    listar_pasajes,
    obtener_asientos_disponibles,
    obtener_ciudades_destino_restantes,
    obtener_ciudades_origen_viaje,
    registrar_pasaje,
)
from controladores.viajes_controller import buscar_viaje_por_id
from modelos.entidades import Ciudad, Pasaje
from ui.estilos_ui import (
    leer_entero,
    limpiar_pantalla,
    mensaje_advertencia,
    mensaje_error,
    mensaje_exito,
    mensaje_info,
    mensaje_opcion,
    pausar,
    subtitulo,
    titulo_seccion,
)


def _nombre_ciudad_seguro(id_ciudad: int) -> str:
    ciudad = buscar_ciudad_por_id(id_ciudad)
    if ciudad is None:
        return f"ID {id_ciudad}"
    return ciudad.nombre


def _imprimir_pasaje(pasaje: Pasaje) -> None:
    nombre_origen = _nombre_ciudad_seguro(pasaje.id_origen)
    nombre_destino = _nombre_ciudad_seguro(pasaje.id_destino)
    mensaje_info(
        f"ID Pasaje: {pasaje.id_pasaje} | Viaje ID: {pasaje.id_viaje} | "
        f"Cliente ID: {pasaje.id_cliente} | Tramo: {nombre_origen} -> {nombre_destino} | "
        f"Asiento: {pasaje.asiento} | Valor: ${pasaje.valor} | Estado: {pasaje.estado}"
    )


def _seleccionar_ciudad(titulo: str, ciudades: List[Ciudad]) -> Ciudad:
    while True:
        subtitulo(titulo)
        for indice, ciudad in enumerate(ciudades, start=1):
            mensaje_opcion(f"{indice}. {ciudad.nombre}")

        seleccion = input("\nIngrese el número de la ciudad: ").strip()
        if seleccion.isdigit():
            indice_elegido = int(seleccion)
            if 1 <= indice_elegido <= len(ciudades):
                return ciudades[indice_elegido - 1]

        mensaje_error("Selección inválida. Ingrese uno de los números listados.")


def _opcion_registrar_pasaje() -> None:
    limpiar_pantalla()
    subtitulo("Registrar Venta de Pasaje")

    id_cliente = leer_entero("ID del cliente: ")
    id_viaje = leer_entero("ID del viaje: ")

    try:
        cliente = buscar_cliente_por_id(id_cliente)
        if cliente is None:
            mensaje_error(f"Validación: No existe un cliente registrado con el ID {id_cliente}.")
            pausar()
            return

        viaje = buscar_viaje_por_id(id_viaje)
        if viaje is None:
            mensaje_error(f"Validación: No existe un viaje programado con el ID {id_viaje}.")
            pausar()
            return

        ciudades_origen = obtener_ciudades_origen_viaje(id_viaje)
        if len(ciudades_origen) == 0:
            mensaje_error("Validación: No hay ciudades de origen disponibles para este viaje.")
            pausar()
            return

        ciudad_origen = _seleccionar_ciudad(
            "Ciudades de origen disponibles", ciudades_origen
        )

        ciudades_destino = obtener_ciudades_destino_restantes(id_viaje, ciudad_origen.id_ciudad)
        if len(ciudades_destino) == 0:
            mensaje_error(
                f"Validación: No quedan ciudades de destino siguientes después de {ciudad_origen.nombre}."
            )
            pausar()
            return

        ciudad_destino = _seleccionar_ciudad(
            f"Ciudades restantes después de {ciudad_origen.nombre}", ciudades_destino
        )

        asientos_libres = obtener_asientos_disponibles(id_viaje)
        if len(asientos_libres) == 0:
            mensaje_error("Validación: No hay asientos disponibles en este viaje.")
            pausar()
            return

        subtitulo("Asientos disponibles (ordenados)")
        texto_asientos = ", ".join(str(nro) for nro in asientos_libres)
        mensaje_info(texto_asientos)

        asiento = leer_entero("Número de asiento: ")

        pasaje_creado: Pasaje = registrar_pasaje(
            id_cliente=id_cliente,
            id_viaje=id_viaje,
            id_origen=ciudad_origen.id_ciudad,
            id_destino=ciudad_destino.id_ciudad,
            asiento=asiento,
        )
        mensaje_exito(
            f"Pasaje registrado con ID {pasaje_creado.id_pasaje} | "
            f"Tramo: {ciudad_origen.nombre} -> {ciudad_destino.nombre} | "
            f"Asiento: {pasaje_creado.asiento} | Valor: ${pasaje_creado.valor}."
        )
    except ValueError as exc:
        mensaje_error(f"Validación: {exc}")
    except RuntimeError as exc:
        mensaje_error(f"Sistema: {exc}")

    pausar()


def _opcion_consultar_pasaje_por_id() -> None:
    limpiar_pantalla()
    subtitulo("Consultar Pasaje por ID")

    id_pasaje = leer_entero("Ingrese ID del pasaje: ")

    try:
        pasaje = buscar_pasaje_por_id(id_pasaje)
        if pasaje is None:
            mensaje_advertencia("Pasaje no encontrado.")
        else:
            _imprimir_pasaje(pasaje)
    except RuntimeError as exc:
        mensaje_error(f"Sistema: {exc}")

    pausar()


def _opcion_listar_pasajes() -> None:
    limpiar_pantalla()
    subtitulo("Pasajes Registrados")

    try:
        pasajes = listar_pasajes()
        if len(pasajes) == 0:
            mensaje_advertencia("No hay pasajes registrados.")
        else:
            for pasaje in pasajes:
                _imprimir_pasaje(pasaje)
    except RuntimeError as exc:
        mensaje_error(f"Sistema: {exc}")

    pausar()


def menu_pasajes() -> None:
    while True:
        limpiar_pantalla()
        titulo_seccion("VENTA DE PASAJES")
        mensaje_opcion("1. Registrar pasaje")
        mensaje_opcion("2. Consultar pasaje por ID")
        mensaje_opcion("3. Listar pasajes")
        mensaje_opcion("0. Volver al menú principal")

        opcion = input("\nSeleccione opción: ").strip()

        if opcion == "1":
            _opcion_registrar_pasaje()
        elif opcion == "2":
            _opcion_consultar_pasaje_por_id()
        elif opcion == "3":
            _opcion_listar_pasajes()
        elif opcion == "0":
            break
        else:
            mensaje_error("Opción no válida.")
            pausar()