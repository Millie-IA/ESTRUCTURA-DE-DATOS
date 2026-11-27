import csv
import os
from RF_01_AL_04 import *

PASAJES = "pasajes.csv"

ENCODE = "utf-8-sig"

class Pasaje:
    def __init__(self, id_pasaje:str, id_viaje:str, id_cliente:str, p_origen:str, p_destino:str, asiento:int, valor:float, estado:str="HABILITADO")-> None:
        self.id_pasaje = id_pasaje
        self.id_viaje = id_viaje
        self.id_cliente = id_cliente
        self.p_origen = p_origen
        self.p_destino = p_destino
        self.asiento = asiento
        self.valor = valor
        self.estado = estado


class PasajeGestion:
    def __init__(self, cliente_gestion: ClienteGestion, bus_gestion: BusGestion, ciudad_gestion: CiudadGestion, viaje_gestion: ViajeGestion) -> None:
        self.pasajes = []
        self.cliente_gestion = cliente_gestion
        self.bus_gestion = bus_gestion
        self.ciudad_gestion = ciudad_gestion
        self.viaje_gestion = viaje_gestion
        self._inicializar_archivo()
        self.cargar_pasajes()
        
        

    def _inicializar_archivo(self)-> None:
        try:
            
            if not os.path.exists(PASAJES) or os.path.getsize(PASAJES) == 0:
                with open(PASAJES, "w", newline= "", encoding=ENCODE) as archivo:
                    writer = csv.writer(archivo)
                    writer.writerow(["id_pasaje", "id_viaje", "id_cliente", "p_origen", "p_destino", "asiento", "valor", "estado"])
        except OSError as e:
            print(f"Error de archivo al inicializar {PASAJES}: {e}")
        """Crea pasajes.csv con su cabecera si no existe."""
        # TODO: verificar os.path.exists y crear cabecera con csv.writer


    def cargar_pasajes(self)-> None:
        """Carga los pasajes desde pasajes.csv."""
        self._inicializar_archivo()
        self.pasajes = []
        try:
            with open(PASAJES, "r", encoding=ENCODE) as archivo:
                lector = csv.DictReader(archivo)
                for fila in lector:
                    pasaje  = Pasaje(
                        fila["id_pasaje"],
                        fila["id_viaje"],
                        fila["id_cliente"],
                        fila["p_origen"],
                        fila["p_destino"],
                        int(fila["asiento"]),
                        float(fila["valor"]),
                        fila["estado"] 
                    )
                    self.pasajes.append(pasaje)
        except (OSError, ValueError, KeyError) as e:
            print(f"Error al leer o convertir datos desde {PASAJES}: {e}")

    # TODO: leer csv con DictReader y armar lista de pasajes


    def guardar_pasajes(self)-> None:
        """Guarda la lista de pasajes en pasajes.csv."""
        try:
            with open(PASAJES, "w", newline="", encoding=ENCODE) as archivo:
                writer= csv.writer(archivo)
                writer.writerow(["id_pasaje", "id_viaje", "id_cliente", "p_origen", "p_destino", "asiento", "valor", "estado"])
                for p in self.pasajes:
                    writer.writerow([
                        p.id_pasaje,
                        p.id_viaje,
                        p.id_cliente,
                        p.p_origen,
                        p.p_destino,
                        p.asiento,
                        p.valor,
                        p.estado
                    ])
                    # TODO: escribir cabecera y filas con csv.writer
        except OSError as e:
            print(f"Error al guardar en {PASAJES} (ve que no esté abierto): {e}")        
                
    def _obtener_posicion_ciudad(self, dato_ciudad:str)-> int | None:
        dato = str(dato_ciudad).strip().lower()
        for c in self.ciudad_gestion.ciudades:
            nombre_c = c.ciudad.strip().lower()
            if str(c.posicion).strip() == dato or nombre_c == dato:
                return int(c.posicion)
        return None
    
    
    def _buscar_viaje_por_id(self, id_viaje:str)-> Viaje | None:
        for v in self.viaje_gestion.viajes:
            if v.id_viaje.strip() == str(id_viaje).strip():
                return v
        return None
    
    def calcular_tarifa(self, tarifa_base: float, pos_origen:int, pos_destino:int)-> float:
        if pos_destino > pos_origen:
            segmentos_usados = pos_destino - pos_origen
        else:
            segmentos_usados = pos_origen - pos_destino
            
        segmentos_no_usados = 5 - segmentos_usados
        descuento = 0.10 * segmentos_no_usados
        return tarifa_base * (1- descuento)
    
    def tramos_se_superponen(self, pos_a1:int, pos_a2:int, pos_b1:int, pos_b2:int) -> bool:
        inicio_a = min(pos_a1, pos_a2)
        fin_a = max(pos_a1, pos_a2)
        inicio_b = min(pos_b1, pos_b2)
        fin_b = max(pos_b1, pos_b2)    
        return inicio_a < fin_b and inicio_b < fin_a
    
    
    def reutilizacion_de_asientos_por_tramo(self, id_viaje:str, asiento:int, pos_origen:int, pos_destino:int)-> bool:
        for p in self.pasajes:
            if p.id_viaje.strip() == str(id_viaje).strip() and p.asiento == asiento and p.estado == "HABILITADO":
                pos_ex_orig = self._obtener_posicion_ciudad(p.p_origen)
                pos_ex_dest = self._obtener_posicion_ciudad(p.p_destino)
                if pos_ex_orig is not None and pos_ex_dest is not None:
                    if self.tramos_se_superponen(pos_origen, pos_destino, pos_ex_orig, pos_ex_dest):
                        return False
        return True
    
    
    def vender_pasaje(self, id_cliente:str, id_viaje:str, p_origen:str, p_destino:str, asiento:int)-> bool:
        cliente = self.cliente_gestion.buscar_cliente_por_id(id_cliente)
        if not cliente:
            print(f"Error - El cliente con ID '{id_cliente}' no existe.")
            return False
        
        viaje = self._buscar_viaje_por_id(id_viaje)
        if not viaje:
            print(f"Error - El viaje con ID '{id_viaje}' no existe.")
            return False
        
        bus = self.bus_gestion.consultar_bus(viaje.id_bus)
        if not bus:
            print(f"Error - El bus asociado al viaje no existe.")
            return False
        
        if asiento < 1 or asiento > bus.capacidad:
            print(f"Error - El asiento {asiento} esta fuera de rango (1 a {bus.capacidad}).")
            return False
            
        pos_p_orig = self._obtener_posicion_ciudad(p_origen)
        pos_p_dest = self._obtener_posicion_ciudad(p_destino)
        pos_v_orig = self._obtener_posicion_ciudad(viaje.p_origen)
        pos_v_dest = self._obtener_posicion_ciudad(viaje.p_destino)
        
        if pos_p_orig is None or pos_p_dest is None or pos_v_orig is None or pos_v_dest is None:
            print(f"Error - Ciudad o destino no válido.")
            return False
        
        if pos_p_orig == pos_p_dest:
            print(f"Error - El origen y el destino no pueden ser iguales.")
            return False
        
        
        sentido_viaje_norte = pos_v_dest > pos_v_orig
        sentido_pasaje_norte = pos_p_dest > pos_p_orig
        
        if sentido_viaje_norte != sentido_pasaje_norte:
            print(f"Error - El tramo seleccionado no respeta el sentido del viaje.")
            return False
        
        min_v, max_v = min(pos_v_orig, pos_v_dest), max(pos_v_orig, pos_v_dest)
        if not (min_v <= pos_p_orig <= max_v and min_v <= pos_p_dest <= max_v):
            print("Error - El tramo solicitado esta fuera del recorrido del viaje")
            return False
        
        if not self.reutilizacion_de_asientos_por_tramo(id_viaje, asiento, pos_p_orig, pos_p_dest):
            print(f"Error - El asiento {asiento} ya está ocupado en parte o totalidad de ese tramo.")
            return False

        valor = self.calcular_tarifa(viaje.tarifa_base, pos_p_orig, pos_p_dest)
        nuevo_id = str(len(self.pasajes) + 1)
        nuevo_pasaje = Pasaje(
            nuevo_id,
            
            str(id_viaje).strip(),
            str(id_cliente).strip(),
            str(p_origen).strip(),
            str(p_destino).strip(),
            asiento,
            valor,
            "HABILITADO"
        )
        
        self.pasajes.append(nuevo_pasaje)
        self.guardar_pasajes()
        
        print(f"Pasaje vendido con exito ID: {nuevo_id} | Valor: ${int(valor)}")
        return True
    
    
    
    
    
    def anular_pasaje(self, id_pasaje:str)-> bool:
        for p in self.pasajes:
            if p.id_pasaje.strip() == str(id_pasaje).strip():
                if p.estado == "ANULADO":
                    print(f"El pasaje {id_pasaje} ya se encuentra ANULADO.")
                    return False
                
                p.estado = "ANULADO"
                self.guardar_pasajes()
                print(f"pasaje {id_pasaje} anulado con éxito.")
                return True
        print(f"Error - no se encontro un pasaje con id '{id_pasaje}'.")
        return False
    


