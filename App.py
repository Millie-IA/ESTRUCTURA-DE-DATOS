
# temporalmente en uso. se reescribirá en el futuro para mejorar la interfaz de usuario y la estructura del código, 
# haciendo uso del archivo estilos_ui.py para centralizar los estilos de la interfaz de usuario y mejorar la consistencia en toda la aplicación.

from ui.estilos_ui import (
    limpiar_pantalla,
    mensaje_advertencia,
    mensaje_error,
    mensaje_opcion,
    pausar,
    titulo_seccion,
)
from ui.menu_clientes import menu_clientes


def main() -> None:
    while True:
        limpiar_pantalla()
        titulo_seccion("SISTEMA DE GESTION")
        mensaje_opcion("1. Gestion de Clientes")
        mensaje_opcion("0. Salir")

        opcion = input("\nSeleccione una opcion: ").strip()

        if opcion == "1":
            menu_clientes()
        elif opcion == "0":
            mensaje_advertencia("Saliendo del sistema. Hasta pronto.")
            break
        else:
            mensaje_error("Opcion no valida. Intente nuevamente.")
            pausar()


if __name__ == "__main__":
    main()