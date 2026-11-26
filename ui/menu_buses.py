from controladores.buses_controller import (
    buscar_bus_por_id,
    buscar_bus_por_patente,
    listar_buses,
    registrar_bus,
)
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
from modelos.entidades import Bus


def _imprimir_bus(bus: Bus) -> None:
    mensaje_info(
        f"ID: {bus.id_bus} | Patente: {bus.patente} | "
        f"Capacidad: {bus.capacidad} pasajeros | Estado: {bus.estado}"
    )


def _opcion_registrar_bus() -> None:
    limpiar_pantalla()
    subtitulo("Registrar Bus")

    patente = leer_texto_no_vacio("Patente: ")
    capacidad = leer_entero("Capacidad de pasajeros: ")
    estado = leer_texto_no_vacio("Estado (disponible / no disponible): ")

    try:
        bus_creado: Bus = registrar_bus(
            patente=patente,
            capacidad=capacidad,
            estado=estado,
        )
        mensaje_exito(
            f"Bus registrado: Patente {bus_creado.patente} (ID {bus_creado.id_bus}) - "
            f"Estado: {bus_creado.estado}."
        )
    except ValueError as exc:
        mensaje_error(f"Validación: {exc}")
    except RuntimeError as exc:
        mensaje_error(f"Sistema: {exc}")

    pausar()


def _opcion_listar_buses() -> None:
    limpiar_pantalla()
    subtitulo("Listado de Buses")

    try:
        buses = listar_buses()
        if len(buses) == 0:
            mensaje_advertencia("No hay buses registrados.")
        else:
            for bus in buses:
                _imprimir_bus(bus)
    except RuntimeError as exc:
        mensaje_error(f"Sistema: {exc}")

    pausar()


def _opcion_buscar_por_id() -> None:
    limpiar_pantalla()
    subtitulo("Buscar Bus por ID")

    id_bus = leer_entero("Ingrese ID del bus: ")

    try:
        bus = buscar_bus_por_id(id_bus)
        if bus is None:
            mensaje_advertencia("Bus no encontrado.")
        else:
            _imprimir_bus(bus)
    except RuntimeError as exc:
        mensaje_error(f"Sistema: {exc}")

    pausar()


def _opcion_buscar_por_patente() -> None:
    limpiar_pantalla()
    subtitulo("Buscar Bus por Patente")

    patente = leer_texto_no_vacio("Ingrese patente del bus: ")

    try:
        bus = buscar_bus_por_patente(patente)
        if bus is None:
            mensaje_advertencia("Bus no encontrado.")
        else:
            _imprimir_bus(bus)
    except RuntimeError as exc:
        mensaje_error(f"Sistema: {exc}")

    pausar()


def menu_buses() -> None:
    while True:
        limpiar_pantalla()
        titulo_seccion("MENU DE BUSES")
        mensaje_opcion("1. Registrar bus")
        mensaje_opcion("2. Listar buses")
        mensaje_opcion("3. Buscar bus por ID")
        mensaje_opcion("4. Buscar bus por patente")
        mensaje_opcion("0. Volver al menú principal")

        opcion = input("\nSeleccione opción: ").strip()

        if opcion == "1":
            _opcion_registrar_bus()
        elif opcion == "2":
            _opcion_listar_buses()
        elif opcion == "3":
            _opcion_buscar_por_id()
        elif opcion == "4":
            _opcion_buscar_por_patente()
        elif opcion == "0":
            break
        else:
            mensaje_error("Opción no válida.")
            pausar()