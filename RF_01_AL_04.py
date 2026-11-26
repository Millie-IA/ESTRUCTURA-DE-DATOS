import os
import csv
from colorama import init, Fore, Style


# ARCHIVOS

CLIENTES = "clientes.csv"
BUSES = "buses.csv"
CIUDADES = "ciudades.csv"
VIAJES = "viajes.csv"

ENCODE = "utf-8-sig"

# ==========================================
# 1. CLASES DE ENTIDAD
# ==========================================

class Cliente:
    def __init__(self, id_cliente: str, rut: str, nombres: str, apellido_paterno: str, apellido_materno: str, contacto: str) -> None:
        self.id_cliente = id_cliente
        self.rut = rut
        self.nombres = nombres
        self.apellido_paterno = apellido_paterno
        self.apellido_materno = apellido_materno
        self.contacto = contacto

class Bus:
    def __init__(self, id_bus: str, patente: str, capacidad: int, estado: str) -> None:
        self.id_bus = id_bus
        self.patente = patente
        self.capacidad = capacidad
        self.estado = estado # Ej: 'Disponible', 'En ruta', etc.

class Ciudad:
    def __init__(self, posicion: int, ciudad: str) -> None:
        self.posicion = posicion
        self.nombre = ciudad

class Viaje:
    def __init__(self, id_viaje: str, id_bus: str, fecha: str, hora: str, p_origen: str, p_destino: str, tarifa_base: float) -> None:
        self.id_viaje = id_viaje
        self.id_bus = id_bus
        self.fecha = fecha
        self.hora = hora
        self.p_origen = p_origen
        self.p_destino = p_destino
        self.tarifa_base = tarifa_base


# ==========================================
# 2. GESTORES 
# ==========================================

class ClienteGestion:
    def __init__(self) -> None:
        self.clientes = []
        self._inicializar_archivo()
        self.cargar_clientes()

    def _inicializar_archivo(self) -> None:
        """Verifica si el archivo clientes.csv existe; si no, lo crea con su encabezado."""
        if not os.path.exists(CLIENTES) or os.path.getsize(CLIENTES) == 0:
            with open(CLIENTES, "w", newline = "", encoding = ENCODE) as archivo:
                writer = csv.writer(archivo)
                writer.writerow(["id_cliente", "rut", "nombres", "apellido_paterno", "apellido_materno", "contacto"])
                
    def cargar_clientes(self) -> None:
        """Carga los clientes desde el archivo CSV a la lista en memoria self.clientes."""
        self._inicializar_archivo()
        
        self.clientes = []
        
        with open (CLIENTES, "r", encoding = ENCODE) as archivo:
            
            lector = csv.DictReader(archivo)
            
            for fila in lector:
                cliente = Cliente(
                    id_cliente = fila["id_cliente"],
                    rut = fila["rut"],
                    nombres = fila["nombres"],
                    apellido_paterno = fila["apellido_paterno"],
                    apellido_materno = fila["apellido_materno"],
                    contacto = fila["contacto"]
                )
                
                self.clientes.append(cliente)

    def registrar_cliente(self, rut: str, nombres: str, apellido_paterno: str, apellido_materno: str, contacto: str) -> bool:
        """RF01: Registra un cliente validando campos obligatorios y evitando RUTs duplicados."""
        
        # 1. Validaciones
        if not rut.strip() or not nombres.strip() or not apellido_paterno.strip() or not apellido_materno.strip() or not contacto.strip():
            print(Fore.RED + "Error: Hay campos obligatorios vacíos.")
            return False

        rut_limpio = rut.replace(".", "").replace("-", "").upper().strip()
        for c in self.clientes:
            c_rut_l = c.rut.replace(".", "").replace("-", "").upper().strip()
            if c.rut_l == rut_limpio:
                print(Fore.RED + f"Error: El RUT {rut} ya existe.")
                return False

        # 2. Crear objeto y añadir a memoria
        nuevo_id = str(len(self.clientes) + 1)
        nuevo_cliente = Cliente(nuevo_id, rut, nombres, apellido_paterno, apellido_materno, contacto)
        self.clientes.append(nuevo_cliente)

        # 3. Guardar el nuevo registro
        self._inicializar_archivo()
        with open(CLIENTES, "a", newline = "", encoding = ENCODE) as archivo:
            writer = csv.writer(archivo)
            writer.writerow([
                nuevo_cliente.id_cliente,
                nuevo_cliente.rut,
                nuevo_cliente.nombres,
                nuevo_cliente.apellido_paterno,
                nuevo_cliente.apellido_materno,
                nuevo_cliente.contacto
            ])

        print(Fore.GREEN + "¡Cliente registrado con éxito!")
        return True

    def listar_clientes(self) -> list:
        """RF01: Retorna la lista de todos los clientes registrados."""
        self.cargar_clientes()
        
        if not self.clientes:
            print(Fore.ORANGE + "No hay clientes registrados en el sistema")
            return []
        
        print(Fore.CYAN + "\n-- LISTADO DE CLIENTES REGISTRADOS ---")
        for c in self.clientes:
            print(f"ID : {c.id_cliente} | RUT : {c.rut} | Nombre completo : {c.nombres} {c.apellido_paterno} {c.apellido_materno} | Contacto : {c.contacto}")
        return self.clientes

    def buscar_cliente_por_id(self, id_cliente: str) -> Cliente | None:
        """RF01: Busca y retorna un cliente según su ID."""
        for c in self.clientes:
            if c.id_cliente.strip() == id_cliente.strip():
                return c
        return None

class BusGestion:
    def __init__(self) -> None:
        self.buses = []
        self._inicializar_archivo()
        self.cargar_buses()

    def _inicializar_archivo(self) -> None:
        """Crea el archivo buses.csv con su cabecera si no existe."""
        
        if not os.path.exists(BUSES) or os.path.getsize(BUSES) == 0:
            with open(BUSES, "w", newline = "", encoding = ENCODE) as archivo:
                writer = csv.writer(archivo)
                writer.writerow(["id_bus","patente", "capacidad", "estado"])
                
    def cargar_buses(self) -> None:
        """Carga los buses desde el archivo CSV."""
        self._inicializar_archivo()
                
        self.buses = []
        
        with open (BUSES, "r", encoding = ENCODE) as archivo:
            
            lector = csv.DictReader(archivo)
            
            for fila in lector:
                bus = Bus(
                    id_bus = fila["id_bus"],
                    patente = fila["patente"],
                    capacidad = int(fila["capacidad"]),
                    estado = fila["estado"]
                )
                
                self.buses.append(bus)

    def registrar_bus(self, patente: str, capacidad: int, estado: str) -> bool:
        """RF02: Registra un bus validando patente única y capacidad entera positiva."""
        
        # 1. Validaciones
        if not patente.strip() or not estado.strip():
            print(Fore.RED + "Error: Hay campos obligatorios vacíos.")
            return False

        if capacidad <= 0:
            print(Fore.RED + f"Error: La capacidad debe ser un número entero positivo.")
            return False

        for b in self.buses:
            if b.patente.strip().upper() == patente.strip().upper():
                print(Fore.RED + f"Error: La patente {patente} ya existe.")
                return False
            
        # 2. Crear objeto y añadir a memoria
        nuevo_id = str(len(self.buses) + 1)
        nuevo_bus = Bus(nuevo_id, patente, capacidad, estado)
        self.buses.append(nuevo_bus)

        # 3. Guardar el nuevo registro
        self._inicializar_archivo()
        with open(BUSES, "a", newline = "", encoding = ENCODE) as archivo:
            writer = csv.writer(archivo)
            writer.writerow([
                nuevo_bus.id_bus,
                nuevo_bus.patente,
                nuevo_bus.capacidad,
                nuevo_bus.estado
            ])

        print(Fore.GREEN + "Bus registrado con éxito!")
        return True

    def listar_buses(self) -> list:
        """RF02: Retorna el listado de buses."""
        self.cargar_buses()
                
        if not self.buses:
            print(Fore.ORANGE + "No hay buses registrados en el sistema")
            return []
        
        print(Fore.CYAN + "\n-- LISTADO DE BUSES REGISTRADOS ---")
        for b in self.buses:
            print(f"ID : {b.id_bus} | Patente : {b.patente} | Capacidad : {b.capacidad} | Estado : {b.estado}")
        return self.buses

    def consultar_bus(self, id_bus: str) -> Bus | None:
        """RF02: Consulta un bus específico por su ID."""
        for b in self.buses:
            if b.id_bus.strip() == id_bus.strip():
                return b
        return None

class CiudadGestion:
    def __init__(self) -> None:
        self.ciudades = []
        self._inicializar_y_cargar_catalogo()

    def _inicializar_y_cargar_catalogo(self) -> None:
        """RF03: Carga el catálogo fijo de las 6 ciudades si el archivo no existe o está vacío."""
        # Ciudades fijas exigidas:
        # 0: Concepción, 1: Chillán, 2: Linares, 3: Talca, 4: Rancagua, 5: Santiago
        if not os.path.exists(CIUDADES) or os.path.getsize(CIUDADES) == 0:
            with open(CIUDADES, "w", newline = "", encoding = ENCODE) as archivo:
                writer = csv.writer(archivo)
                writer.writerow(["posicion", "ciudad"])
                writer.writerow(["0", "Concepción"])
                writer.writerow(["1", "Chillán"])
                writer.writerow(["2", "Linares"])
                writer.writerow(["3", "Talca"])
                writer.writerow(["4", "Rancagua"])
                writer.writerow(["5", "Santiago"])
                
        self.ciudades = []
        with open(CIUDADES, "r", encoding = ENCODE) as archivo:
            lector = csv.DictReader(archivo)
            for fila in lector:
                ciudad = Ciudad(
                    posicion = int(fila["posicion"]),
                    ciudad = fila["ciudad"]
                    )
                self.ciudades.append(ciudad)

    def listar_ciudades(self) -> list:
        """RF03: Retorna el catálogo completo de ciudades con sus posiciones."""
        self._inicializar_y_cargar_catalogo()

        print(Fore.CYAN + "\n-- LISTADO DE CIUDADES REGISTRADAS ---")
        for c in self.ciudades:
            print(f"Posición : {c.posicion} | Ciudad : {c.ciudad}")
        return self.ciudades


class ViajeGestion:
    def __init__(self, bus_gestion: BusGestion, ciudad_gestion: CiudadGestion) -> None:
        self.viajes = []
        self.bus_gestion = bus_gestion
        self.ciudad_gestion = ciudad_gestion
        self._inicializar_archivo()
        self.cargar_viajes()

    def _inicializar_archivo(self) -> None:
        """Crea el archivo viajes.csv con su cabecera si no existe."""
        
        if not os.path.exists(VIAJES) or os.path.getsize(VIAJES) == 0:
            with open(VIAJES, "w", newline = "", encoding = ENCODE) as archivo:
                writer = csv.writer(archivo)
                writer.writerow(["id_viaje", "id_bus", "fecha", "hora", "p_origen", "p_destino", "tarifa_base"])

    def cargar_viajes(self) -> None:
        """Carga los viajes desde el archivo CSV."""
        
        self._inicializar_archivo()
                        
        self.viajes = []
        
        with open (VIAJES, "r", encoding = ENCODE) as archivo:
            
            lector = csv.DictReader(archivo)
            
            for fila in lector:
                viaje = Viaje(
                    id_viaje = fila["id_viaje"],
                    id_bus = fila["id_bus"],
                    fecha = fila["fecha"],
                    hora = fila["hora"],
                    p_origen = fila["p_origen"],
                    p_destino = fila["p_destino"],
                    tarifa_base = float(fila["tarifa_base"])                 
                )
                
                self.viajes.append(viaje)
     
    def validar_y_calcular_tramo(self, pos_origen: int, pos_destino: int, tarifa_base: float = 10000.0) -> tuple[bool, float, str]:
        """
        Valida que el tramo respete un sentido lógico (de sur a norte o de norte a sur) 
        y calcula la tarifa automática según los segmentos no utilizados (10% descuento acumulativo por segmento).
        Posiciones: 0:Concepción, 1:Chillán, 2:Linares, 3:Talca, 4:Rancagua, 5:Santiago
        """
        
        # 1. Validar que origen y destino no sean iguales
        if pos_origen == pos_destino:
            return False, 0.0, "El origen y el destino no pueden ser iguales."

        # 2. Validar que estén dentro del rango válido (0 a 5)
        if not (0 <= pos_origen <= 5) or not (0 <= pos_destino <= 5):
            return False, 0.0, "Las posiciones deben estar entre 0 y 5."

        # Cantidad de segmentos totales del recorrido completo = 5 (de 0 a 5)
        segmentos_totales = 5
        
        # Cantidad de segmentos que realmente usará el pasajero
        segmentos_usados = abs(pos_destino - pos_origen)
        
        # Segmentos que NO se utilizan
        segmentos_no_usados = segmentos_totales - segmentos_usados

        # 4. Cálculo de tarifa: 10% de descuento acumulativo por cada segmento no utilizado
        # Fórmula: tarifa_base * (1 - 0.10 * segmentos_no_usados)
        descuento_porcentaje = 0.10 * segmentos_no_usados
        tarifa_calculada = tarifa_base * (1 - descuento_porcentaje)

        return True, tarifa_calculada, "Tramo válido."

    def programar_viaje(self, id_bus: str, fecha: str, hora: str, p_origen: str, p_destino: str, tarifa_base: float) -> bool:
        """RF04: Programa un viaje validando que el bus exista, y que la ruta sea 
        estrictamente Concepción-Santiago o Santiago-Concepción."""
        
        
        # 1. Validaciones
        if not id_bus.strip() or not fecha.strip() or not hora.strip() or not p_origen.strip() or not p_destino.strip():
            print(Fore.RED + "Error: Hay campos obligatorios vacíos para programar el viaje.")
            return False

        bus_encontrado = self.bus_gestion.consultar_bus(id_bus)
        if not bus_encontrado:
            print(Fore.RED + f"Error: El bus con ID '{id_bus}' no existe en el sistema.")
            return False
        
        
        '''Aquí no entendí la lógica que pide la pauta, así que hice dos opciones:
            - En la primera, una función que permite ingresar viajes desde cualquier lugar hasta cualquier lugar, 
            mientras no quiera llagar a la misma ciudad o elija una posicion que no existe.
            Además el calculo de tramo...(Que puede reutilizar o borrar Diego).
            
            - En la segunda, solo hay una condición con tramos predeterminados según la segunda tabla del PDF.'''
        # OPCIÓN 1
        self.validar_y_calcular_tramo(p_origen, p_destino)

        ''' OPCIÓN 2 : RUTAS PREDETERMINADAS
        
        rutas_permitidas = [
            ("Concepción", "Santiago"),
            ("Chillán", "Santiago"),
            ("Santiago", "Rancagua"),
            ("Concepción", "Talca"),
            ("Chillán", "Talca"),
            ("Talca", "Linares"),
            # Sentidos inversos
            ("Santiago", "Concepción"),
            ("Santiago", "Chillán"),
            ("Rancagua", "Santiago"),
            ("Talca", "Concepción"),
            ("Talca", "Chillán"),
            ("Linares", "Talca")
        ]
        

        if (p_origen, p_destino) not in rutas_permitidas:
            print(Fore.RED + "Error: La ruta ingresada no está permitida según las combinaciones oficiales.")
            return False
        '''

        if tarifa_base <= 0:
            print(Fore.RED + "Error: La tarifa base debe ser mayor a 0.")
            return False
                        
        # 2. Crear objeto y añadir a memoria
        nuevo_id = str(len(self.viajes) + 1)
        nuevo_viaje = Viaje(nuevo_id, id_bus, fecha, hora, p_origen, p_destino, tarifa_base)
        self.viajes.append(nuevo_viaje)

        # 3. Guardar el nuevo registro
        self._inicializar_archivo()
        with open(VIAJES, "a", newline = "", encoding = ENCODE) as archivo:
            writer = csv.writer(archivo)
            writer.writerow([
                nuevo_viaje.id_viaje,
                nuevo_viaje.id_bus,
                nuevo_viaje.fecha,
                nuevo_viaje.hora,
                nuevo_viaje.p_origen,
                nuevo_viaje.p_destino,
                nuevo_viaje.tarifa_base
            ])

        print(Fore.GREEN + "Viaje registrado con éxito!")
        return True

    def listar_viajes(self) -> list:
        """RF04: Retorna el listado de viajes programados."""
        self._inicializar_archivo()
        
        print(Fore.CYAN + "\n-- LISTADO DE VIAJES REGISTRAD0S ---")
        for v in self.viajes:
            print(f" ID : {v.id_viaje} | Bus : {v.id_bus} Fecha : {v.fecha} Hora : {v.hora} | Punto de origen : {v.p_origen} Punto de destino : {v.p_destino} | Tarifa : {v.tarifa_base}")
        return self.viajes