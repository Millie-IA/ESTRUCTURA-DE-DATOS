from controladores.viajes_controller import (
    buscar_viaje_por_id,
    listar_viajes,
    programar_viaje,
)
from modelos.entidades import Viaje
from ui.estilos_ui import (
    leer_entero,
    leer_texto_no_vacio,
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


def _imprimir_viaje(viaje: Viaje) -> None:
    mensaje_info(
        f"ID: {viaje.id_viaje} | Bus ID: {viaje.id_bus} | "
        f"Fecha: {viaje.fecha} | Hora: {viaje.hora} | "
        f"Ruta: {viaje.ciudad_inicial} -> {viaje.ciudad_final} | "
        f"Tarifa base: ${viaje.tarifa_base}"
    )


def _leer_direccion_viaje() -> int:
    while True:
        subtitulo("Dirección del viaje")
        mensaje_opcion("1. Concepción -> Santiago")
        mensaje_opcion("2. Santiago -> Concepción")
        opcion = input("\nSeleccione dirección (1 o 2): ").strip()

        if opcion == "1":
            return 1
        if opcion == "2":
            return 2
        mensaje_error("Dirección inválida. Seleccione 1 o 2.")


def _opcion_programar_viaje() -> None:
    limpiar_pantalla()
    subtitulo("Programar Viaje")

    id_bus = leer_entero("ID del bus: ")
    fecha = leer_texto_no_vacio("Fecha (AAAA-MM-DD): ")
    hora = leer_texto_no_vacio("Hora (HH:MM): ")
    direccion = _leer_direccion_viaje()
    tarifa_base = leer_entero("Tarifa base: ")

    try:
        viaje_creado: Viaje = programar_viaje(
            id_bus=id_bus,
            fecha=fecha,
            hora=hora,
            direccion=direccion,
            tarifa_base=tarifa_base,
        )
        mensaje_exito(
            f"Viaje programado con ID {viaje_creado.id_viaje}: "
            f"{viaje_creado.ciudad_inicial} -> {viaje_creado.ciudad_final} "
            f"({viaje_creado.fecha} {viaje_creado.hora})."
        )
    except ValueError as exc:
        mensaje_error(f"Validación: {exc}")
    except RuntimeError as exc:
        mensaje_error(f"Sistema: {exc}")

    pausar()


def _opcion_listar_viajes() -> None:
    limpiar_pantalla()
    subtitulo("Listado de Viajes")

    try:
        viajes = listar_viajes()
        if len(viajes) == 0:
            mensaje_advertencia("No hay viajes programados.")
        else:
            for viaje in viajes:
                _imprimir_viaje(viaje)
    except RuntimeError as exc:
        mensaje_error(f"Sistema: {exc}")

    pausar()


def _opcion_consultar_viaje_por_id() -> None:
    limpiar_pantalla()
    subtitulo("Consultar Viaje por ID")

    id_viaje = leer_entero("Ingrese ID del viaje: ")

    try:
        viaje = buscar_viaje_por_id(id_viaje)
        if viaje is None:
            mensaje_advertencia("Viaje no encontrado.")
        else:
            _imprimir_viaje(viaje)
    except RuntimeError as exc:
        mensaje_error(f"Sistema: {exc}")

    pausar()


def menu_viajes() -> None:
    while True:
        limpiar_pantalla()
        titulo_seccion("MENU DE VIAJES")
        mensaje_opcion("1. Programar viaje")
        mensaje_opcion("2. Listar viajes")
        mensaje_opcion("3. Consultar viaje por ID")
        mensaje_opcion("0. Volver al menú principal")

        opcion = input("\nSeleccione opción: ").strip()

        if opcion == "1":
            _opcion_programar_viaje()
        elif opcion == "2":
            _opcion_listar_viajes()
        elif opcion == "3":
            _opcion_consultar_viaje_por_id()
        elif opcion == "0":
            break
        else:
            mensaje_error("Opción no válida.")
            pausar()