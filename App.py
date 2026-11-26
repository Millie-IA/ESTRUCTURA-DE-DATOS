from ui.estilos_ui import (
    limpiar_pantalla,
    mensaje_advertencia,
    mensaje_error,
    mensaje_opcion,
    pausar,
    titulo_seccion,
)
from ui.menu_buses import menu_buses
from ui.menu_ciudades import menu_ciudades
from ui.menu_clientes import menu_clientes


def main() -> None:
    while True:
        limpiar_pantalla()
        titulo_seccion("RUTASUR - SISTEMA DE GESTION")
        mensaje_opcion("1. Gestión de Clientes")
        mensaje_opcion("2. Gestión de Buses")
        mensaje_opcion("3. Consulta de Ciudades")
        mensaje_opcion("0. Salir")

        opcion = input("\nSeleccione una opción: ").strip()

        if opcion == "1":
            menu_clientes()
        elif opcion == "2":
            menu_buses()
        elif opcion == "3":
            menu_ciudades()
        elif opcion == "0":
            mensaje_advertencia("Saliendo del sistema. Hasta pronto.")
            break
        else:
            mensaje_error("Opción no válida. Intente nuevamente.")
            pausar()


if __name__ == "__main__":
    main()