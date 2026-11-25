import os
from colorama import Fore, Style, init
from menu_nomina import opcion_5_nomina

init(autoreset=True)


def limpiar_pantalla():
    os.system("cls")


def menu_principal():
    while True:
        limpiar_pantalla()
        print(Fore.CYAN + Style.BRIGHT + "=" * 50)
        print(Fore.CYAN + Style.BRIGHT + "RUTASUR TRANSPORTES - MENÚ PRINCIPAL".center(50))
        print(Fore.CYAN + Style.BRIGHT + "=" * 50)
        print(Fore.WHITE + "1. Opción 1")
        print(Fore.WHITE + "2. Opción 2")
        print(Fore.WHITE + "3. Opción 3")
        print(Fore.WHITE + "4. Opción 4")
        print(Fore.GREEN + Style.BRIGHT + "5. Obtener nómina de pasajeros por viaje")
        print(Fore.RED + "0. Salir")
        print(Fore.CYAN + "=" * 50)

        op = input(Fore.YELLOW + "Seleccione una opción: ").strip()

        if op == "1":
            limpiar_pantalla()
            print(Fore.MAGENTA + "Opción 1 aún no implementada.")
            op = input("Presione Enter para volver...")
        elif op == "2":
            limpiar_pantalla()
            print(Fore.MAGENTA + "Opción 2 aún no implementada.")
            op = input("Presione Enter para volver...")
        elif op == "3":
            limpiar_pantalla()
            print(Fore.MAGENTA + "Opción 3 aún no implementada.")
            op = input("Presione Enter para volver...")
        elif op == "4":
            limpiar_pantalla()
            print(Fore.MAGENTA + "Opción 4 aún no implementada.")
            op = input("Presione Enter para volver...")
        elif op == "5":
            opcion_5_nomina()
        elif op == "0":
            limpiar_pantalla()
            print(Fore.CYAN + Style.BRIGHT + "Cerrando sistema de RutaSur Transportes...")
            break
        else:
            limpiar_pantalla()
            print(Fore.RED + Style.BRIGHT + "Opción inválida.")
            op = input("Presione Enter para reintentar...")


if __name__ == "__main__":
    menu_principal()