import os
from colorama import init, Fore, Style
from RF_01_AL_04 import ClienteGestion, BusGestion, CiudadGestion, ViajeGestion
from RF_05_AL_07 import PasajeGestion
init(autoreset=True)

def limpiar_pantalla() -> None:
    os.system("cls" if os.name == "nt" else "clear")

def pausar() -> None:
    """Detiene la ejecución brevemente para que el usuario lea los mensajes."""
    input(Fore.YELLOW + "\nPresione Enter para continuar..." + Style.RESET_ALL)

def main() -> None:
    # Instanciar los gestores principales
    pasaje_gestion = PasajeGestion(cliente_gestion, bus_gestion, ciudad_gestion, viaje_gestion)
    cliente_gestion = ClienteGestion()
    bus_gestion = BusGestion()
    ciudad_gestion = CiudadGestion()
    viaje_gestion = ViajeGestion(bus_gestion, ciudad_gestion)

    while True:
        limpiar_pantalla()
        print(Fore.CYAN + Style.BRIGHT + "=" * 55)
        print(Fore.CYAN + Style.BRIGHT + "      SISTEMA DE GESTIÓN DE PASAJES - RUTASUR       ")
        print(Fore.CYAN + Style.BRIGHT + "=" * 55)
        print(Fore.YELLOW + "1." + Style.RESET_ALL + " Gestión de Clientes (RF01)")
        print(Fore.YELLOW + "2." + Style.RESET_ALL + " Gestión de Buses (RF02)")
        print(Fore.YELLOW + "3." + Style.RESET_ALL + " Catálogo de Ciudades (RF03)")
        print(Fore.YELLOW + "4." + Style.RESET_ALL + " Gestión de Viajes (RF04)")
        print(Fore.YELLOW + "5." + Style.RESET_ALL + " Venta de Pasajes y Reutilización de Asientos (RF05 & RF06)")
        print(Fore.YELLOW + "6." + Style.RESET_ALL + " Anulación de Pasajes (RF07)")
        print(Fore.YELLOW + "7." + Style.RESET_ALL + " Nómina de Pasajeros por Viaje (RF08)")
        print(Fore.YELLOW + "8." + Style.RESET_ALL + " Consultas y Reportes (RF09)")
        print(Fore.YELLOW + "9." + Style.RESET_ALL + " Salir")
        print(Fore.CYAN + "-" * 55)

        opcion = input(Fore.GREEN + "Ingrese una opción (1-9): " + Style.RESET_ALL).strip()

        if opcion == "1":
            # --- SUBMENÚ CLIENTES (RF01) ---
            while True:
                limpiar_pantalla()
                print(Fore.CYAN + "\n=== GESTIÓN DE CLIENTES ===")
                print("1. Registrar Cliente")
                print("2. Listar Clientes")
                print("3. Buscar Cliente por ID")
                print("4. Volver al Menú Principal")
                sub_op = input(Fore.GREEN + "Seleccione una opción: " + Style.RESET_ALL).strip()
                
                if sub_op == "1":
                    print(Fore.CYAN + "\n-- REGISTRAR NUEVO CLIENTE --")
                    rut = input("RUT (ej. 12.345.678-9): ")
                    nombres = input("Nombres: ")
                    ap_pat = input("Apellido Paterno: ")
                    ap_mat = input("Apellido Materno: ")
                    contacto = input("Contacto (Teléfono/Correo): ")
                    cliente_gestion.registrar_cliente(rut, nombres, ap_pat, ap_mat, contacto)
                    pausar()
                elif sub_op == "2":
                    cliente_gestion.listar_clientes()
                    pausar()
                elif sub_op == "3":
                    id_c = input("Ingrese el ID del cliente a buscar: ")
                    cli = cliente_gestion.buscar_cliente_por_id(id_c)
                    if cli:
                        print(Fore.GREEN + f"\n¡Cliente encontrado!")
                        print(f"ID: {cli.id_cliente} | RUT: {cli.rut} | Nombre: {cli.nombres} {cli.apellido_paterno} {cli.apellido_materno} | Contacto: {cli.contacto}")
                    else:
                        print(Fore.RED + "Error: No se encontró un cliente con ese ID.")
                    pausar()
                elif sub_op == "4":
                    break
                else:
                    print(Fore.RED + "Opción inválida. Intente nuevamente.")
                    pausar()

        elif opcion == "2":
            # --- SUBMENÚ BUSES (RF02) ---
            while True:
                limpiar_pantalla()
                print(Fore.CYAN + "\n=== GESTIÓN DE BUSES ===")
                print("1. Registrar Bus")
                print("2. Listar Buses")
                print("3. Consultar Bus por ID")
                print("4. Volver al Menú Principal")
                sub_op = input(Fore.GREEN + "Seleccione una opción: " + Style.RESET_ALL).strip()
                
                if sub_op == "1":
                    print(Fore.CYAN + "\n-- REGISTRAR NUEVO BUS --")
                    patente = input("Patente (única): ")
                    try:
                        capacidad = int(input("Capacidad (número entero positivo de asientos): "))
                    except ValueError:
                        print(Fore.RED + "Error: La capacidad debe ser un número entero.")
                        pausar()
                        continue
                    estado = input("Estado (ej. Disponible / En ruta): ")
                    bus_gestion.registrar_bus(patente, capacidad, estado)
                    pausar()
                elif sub_op == "2":
                    bus_gestion.listar_buses()
                    pausar()
                elif sub_op == "3":
                    id_b = input("Ingrese el ID del bus: ")
                    b = bus_gestion.consultar_bus(id_b)
                    if b:
                        print(Fore.GREEN + f"\nBus encontrado -> ID: {b.id_bus} | Patente: {b.patente} | Capacidad: {b.capacidad} | Estado: {b.estado}")
                    else:
                        print(Fore.RED + "Error: Bus no encontrado.")
                    pausar()
                elif sub_op == "4":
                    break
                else:
                    print(Fore.RED + "Opción inválida. Intente nuevamente.")
                    pausar()

        elif opcion == "3":
            # --- CATÁLOGO DE CIUDADES (RF03) ---
            limpiar_pantalla()
            ciudad_gestion.listar_ciudades()
            pausar()

        elif opcion == "4":
            # --- SUBMENÚ VIAJES (RF04) ---
            while True:
                limpiar_pantalla()
                print(Fore.CYAN + "\n=== GESTIÓN DE VIAJES ===")
                print("1. Programar Viaje")
                print("2. Listar Viajes Programados")
                print("3. Volver al Menú Principal")
                sub_op = input(Fore.GREEN + "Seleccione una opción: " + Style.RESET_ALL).strip()
                
                if sub_op == "1":
                    print(Fore.CYAN + "\n-- PROGRAMAR VIAJE --")
                    print(Fore.YELLOW + "Ciudades del recorrido fijo:")
                    for c in ciudad_gestion.ciudades:
                        print(f"[{c.posicion}] {c.nombre}")
                    
                    id_bus = input("\nID del Bus existente: ")
                    fecha = input("Fecha (YYYY-MM-DD): ")
                    hora = input("Hora (HH:MM): ")
                    p_origen = input("Ciudad Origen (Nombre o posición): ")
                    p_destino = input("Ciudad Destino (Nombre o posición): ")
                    try:
                        tarifa_base = float(input("Tarifa Base de referencia (ej. 10000): "))
                    except ValueError:
                        print(Fore.RED + "Error: Tarifa base inválida.")
                        pausar()
                        continue
                    
                    viaje_gestion.programar_viaje(id_bus, fecha, hora, p_origen, p_destino, tarifa_base)
                    pausar()
                elif sub_op == "2":
                    viaje_gestion.listar_viajes()
                    pausar()
                elif sub_op == "3":
                    break
                else:
                    print(Fore.RED + "Opción inválida. Intente nuevamente.")
                    pausar()

        elif opcion == "5":
            limpiar_pantalla()
            limpiar_pantalla()
            print(Fore.CYAN + Style.BRIGHT + "\n=== VENTA DE PASAJES (RF05 & RF06) ===")
            
            cliente_gestion.listar_clientes()
            id_cliente  = input(Fore.WHITE + "\nIngrese ID del cliente").strip()
            
            viaje_gestion.listar_clietes()
            id_cliente = input(Fore.WHITE + "\nIngrese ID del viaje: ").strip()
            
            print(Fore.YELLOW + "\nParadas disponibles en la ruta:")
            for c in ciudad_gestion.ciudades:
                print(f" [{c.posicion}] {c.nombre}")
                
            p_origen = input(Fore.WHITE + "\nIngrese ciudad o posición de origen: ").strip()
            p_destino = input(Fore.WHITE + "Ingrese ciudad o posicion de destino: ").strip()
            
            try:
                asiento = int(input(Fore.WHITE + "Ingreso número de asiento: ").strip())
                pasaje_gestion.vender_pasaje(id_cliente, id_viaje, p_origen, p_destino, asiento)
            except ValueError:
                print(Fore.RED + "Error - El número de asiento debe ser un entero válido")
            pausar()

        elif opcion == "6":
            limpiar_pantalla()
            print(Fore.YELLOW + "\n[Módulo RF07: Anulación de Pasajes]")
            print("Módulo listo para ser integrado.")
            pausar()

        elif opcion == "7":
            limpiar_pantalla()
            print(Fore.YELLOW + "\n[Módulo RF08: Nómina de Pasajeros por Viaje]")
            print("Módulo listo para ser integrado.")
            pausar()

        elif opcion == "8":
            limpiar_pantalla()
            print(Fore.YELLOW + "\n[Módulo RF09: Consultas y Reportes]")
            print("Módulo listo para ser integrado.")
            pausar()

        elif opcion == "9":
            print(Fore.GREEN + "\n¡Gracias por utilizar RutaSur Transportes! Saliendo del sistema...")
            break
        else:
            input(Fore.RED + "ERROR: Opción inválida. Ingrese números del 0 al 9. Presione Enter para continuar.")

if __name__ == "__main__":
    main()