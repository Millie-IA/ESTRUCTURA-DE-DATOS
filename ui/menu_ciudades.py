from controladores.ciudades_controller import (
    buscar_ciudad_por_id,
    buscar_ciudad_por_nombre,
    listar_ciudades,
)
from ui.estilos_ui import (
    leer_entero,
    leer_texto_no_vacio,
    limpiar_pantalla,
    mensaje_advertencia,
    mensaje_error,
    mensaje_info,
    mensaje_opcion,
    pausar,
    subtitulo,
    titulo_seccion,
)
from modelos.entidades import Ciudad


def _imprimir_ciudad(ciudad: Ciudad) -> None:
    mensaje_info(
        f"ID: {ciudad.id_ciudad} | Ciudad: {ciudad.nombre} | Posición: {ciudad.posicion}"
    )


def _opcion_consultar_catalogo() -> None:
    limpiar_pantalla()
    subtitulo("Catálogo de Ciudades")

    try:
        ciudades = listar_ciudades()
        if len(ciudades) == 0:
            mensaje_advertencia("No hay ciudades registradas en el catálogo.")
        else:
            for ciudad in ciudades:
                _imprimir_ciudad(ciudad)
    except RuntimeError as exc:
        mensaje_error(f"Sistema: {exc}")

    pausar()


def _opcion_buscar_por_id() -> None:
    limpiar_pantalla()
    subtitulo("Consultar Ciudad por ID")

    id_ciudad = leer_entero("Ingrese ID de la ciudad: ")

    try:
        ciudad = buscar_ciudad_por_id(id_ciudad)
        if ciudad is None:
            mensaje_advertencia("Ciudad no encontrada.")
        else:
            _imprimir_ciudad(ciudad)
    except RuntimeError as exc:
        mensaje_error(f"Sistema: {exc}")

    pausar()


def _opcion_buscar_por_nombre() -> None:
    limpiar_pantalla()
    subtitulo("Consultar Ciudad por Nombre")

    nombre = leer_texto_no_vacio("Ingrese nombre de la ciudad: ")

    try:
        ciudad = buscar_ciudad_por_nombre(nombre)
        if ciudad is None:
            mensaje_advertencia("Ciudad no encontrada.")
        else:
            _imprimir_ciudad(ciudad)
    except RuntimeError as exc:
        mensaje_error(f"Sistema: {exc}")

    pausar()


def menu_ciudades() -> None:
    while True:
        limpiar_pantalla()
        titulo_seccion("MENU DE CIUDADES")
        mensaje_opcion("1. Consultar catálogo completo")
        mensaje_opcion("2. Buscar ciudad por ID")
        mensaje_opcion("3. Buscar ciudad por nombre")
        mensaje_opcion("0. Volver al menú principal")

        opcion = input("\nSeleccione opción: ").strip()

        if opcion == "1":
            _opcion_consultar_catalogo()
        elif opcion == "2":
            _opcion_buscar_por_id()
        elif opcion == "3":
            _opcion_buscar_por_nombre()
        elif opcion == "0":
            break
        else:
            mensaje_error("Opción no válida.")
            pausar()