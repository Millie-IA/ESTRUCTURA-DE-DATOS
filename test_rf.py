#test 

from colorama import Fore, init
from RF_01_AL_04 import ClienteGestion, BusGestion, CiudadGestion, ViajeGestion

init(autoreset=True)

print(Fore.CYAN + "=== INICIANDO PRUEBAS DE RF01 A RF04 ===")

# 1. Prueba Clientes (RF01)
cg = ClienteGestion()
cg.registrar_cliente("12.345.678-9", "Diego", "Pérez", "Soto", "912345678")
cg.registrar_cliente("12.345.678-9", "Diego", "Pérez", "Soto", "912345678")  # Debe rechazar duplicado
cg.listar_clientes()

# 2. Prueba Buses (RF02)
bg = BusGestion()
bg.registrar_bus("ABCD-12", 40, "Disponible")
bg.registrar_bus("XYZW-99", -5, "Disponible")  # Debe rechazar capacidad <= 0
bg.listar_buses()

# 3. Prueba Ciudades (RF03)
ciudades = CiudadGestion()
print(Fore.YELLOW + "\n[RF03] Ciudades cargadas en memoria:", len(ciudades.ciudades))
for c in ciudades.ciudades:
    print(f"Posición: {c.posicion} | Ciudad: {c.nombre}")

# 4. Prueba Viajes (RF04)
vg = ViajeGestion(bg, ciudades)
vg.programar_viaje("1", "2026-12-01", "08:30", "Concepción", "Santiago", 15000.0)
vg.listar_viajes()

print(Fore.GREEN + "\n=== PRUEBAS FINALIZADAS SIN ERRORES ===")
