
# Archivo creado por ALEJANDRO JARPA
# Este archivo define los estilos de la interfaz de usuario, como colores y formatos de texto.
# Los nombres de las funciones son autodescriptivos y reflejan su propósito en la interfaz de usuario.

import os
from colorama import Fore, Style, init, just_fix_windows_console

just_fix_windows_console()
init(autoreset=True)

def limpiar_pantalla() -> None:
    os.system("cls" if os.name == "nt" else "clear")
    just_fix_windows_console()

def pausar(mensaje: str = "\nPresione ENTER para continuar...") -> None:
    input(f"{Fore.CYAN}{Style.BRIGHT}{mensaje}{Style.RESET_ALL}")

def titulo_seccion(texto: str) -> None:
    linea = "=" * (len(texto) + 6)
    print(f"\n{Fore.CYAN}{Style.BRIGHT}{linea}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{Style.BRIGHT}   {texto}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{Style.BRIGHT}{linea}{Style.RESET_ALL}")

def subtitulo(texto: str) -> None:
    print(f"\n{Fore.MAGENTA}{Style.BRIGHT}--- {texto} ---{Style.RESET_ALL}")


def mensaje_exito(texto: str) -> None:
    print(f"{Fore.GREEN}{Style.BRIGHT}[OK] {texto}{Style.RESET_ALL}")


def mensaje_error(texto: str) -> None:
    print(f"{Fore.RED}{Style.BRIGHT}[ERROR] {texto}{Style.RESET_ALL}")


def mensaje_advertencia(texto: str) -> None:
    print(f"{Fore.YELLOW}{Style.BRIGHT}[AVISO] {texto}{Style.RESET_ALL}")


def mensaje_info(texto: str) -> None:
    print(f"{Fore.WHITE}{Style.BRIGHT}{texto}{Style.RESET_ALL}")


def mensaje_opcion(texto: str) -> None:
    print(f"{Fore.BLUE}{Style.BRIGHT}{texto}{Style.RESET_ALL}")


def leer_texto_no_vacio(prompt: str) -> str:
    while True:
        valor = input(f"{Fore.YELLOW}{Style.BRIGHT}{prompt}{Style.RESET_ALL}").strip()
        if valor:
            return valor
        mensaje_error("El campo no puede estar vacío.")


def leer_entero(prompt: str, permitir_vacio: bool = False) -> int:
    while True:
        raw = input(f"{Fore.YELLOW}{Style.BRIGHT}{prompt}{Style.RESET_ALL}").strip()
        if permitir_vacio and raw == "":
            return -1
        try:
            return int(raw)
        except ValueError:
            mensaje_error("Debe ingresar un número entero válido.")