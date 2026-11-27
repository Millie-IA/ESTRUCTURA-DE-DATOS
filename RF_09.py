from colorama import Fore, Style
from RF_01_AL_04 import ClienteGestion, BusGestion, CiudadGestion, ViajeGestion
from RF_05_AL_07 import PasajeGestion


class ReporteGestion:

    def __init__(
        self,
        cliente_gestion: ClienteGestion,
        bus_gestion: BusGestion,
        ciudad_gestion: CiudadGestion,
        viaje_gestion: ViajeGestion,
        pasaje_gestion: PasajeGestion,
    ) -> None:
        self.cliente_gestion = cliente_gestion
        self.bus_gestion = bus_gestion
        self.ciudad_gestion = ciudad_gestion
        self.viaje_gestion = viaje_gestion
        self.pasaje_gestion = pasaje_gestion

    def _nombre_ciudad(self, dato_ciudad: str) -> str:
        pos = self.pasaje_gestion._obtener_posicion_ciudad(dato_ciudad)
        if pos is not None:
            for c in self.ciudad_gestion.ciudades:
                if int(c.posicion) == pos:
                    return c.nombre
        return str(dato_ciudad).strip()

    def obtener_ciudades_en_sentido_viaje(self, id_viaje: str) -> list:
        viaje = self.pasaje_gestion._buscar_viaje_por_id(id_viaje)
        if not viaje:
            return []

        pos_vo = self.pasaje_gestion._obtener_posicion_ciudad(viaje.p_origen)
        pos_vd = self.pasaje_gestion._obtener_posicion_ciudad(viaje.p_destino)
        if pos_vo is None or pos_vd is None:
            return list(self.ciudad_gestion.ciudades)

        min_pos, max_pos = min(pos_vo, pos_vd), max(pos_vo, pos_vd)
        filtradas = [
            c for c in self.ciudad_gestion.ciudades
            if min_pos <= int(c.posicion) <= max_pos
        ]

        # ordena por método burbuja
        sentido_asc = pos_vd >= pos_vo
        n = len(filtradas)
        for i in range(n):
            intercambio = False
            for j in range(0, n - i - 1):
                p_a = int(filtradas[j].posicion)
                p_b = int(filtradas[j + 1].posicion)
                debe_intercambiar = (p_a > p_b) if sentido_asc else (p_a < p_b)
                if debe_intercambiar:
                    filtradas[j], filtradas[j + 1] = filtradas[j + 1], filtradas[j]
                    intercambio = True
            if not intercambio:
                break

        return filtradas

    def listar_pasajes_viaje_con_estado(self, id_viaje: str) -> bool:
        viaje = self.pasaje_gestion._buscar_viaje_por_id(id_viaje)
        if not viaje:
            print(Fore.RED + f"Error: No existe un viaje con ID '{id_viaje}'.")
            return False

        id_v = str(id_viaje).strip()
        pasajes_viaje = [
            p for p in self.pasaje_gestion.pasajes if str(p.id_viaje).strip() == id_v
        ]

        origen_v = self._nombre_ciudad(viaje.p_origen)
        destino_v = self._nombre_ciudad(viaje.p_destino)

        print(Fore.CYAN + Style.BRIGHT + "\n" + "=" * 98)
        print(
            Fore.CYAN + Style.BRIGHT
            + f"PASAJES DEL VIAJE #{viaje.id_viaje} ({origen_v} -> {destino_v} | {viaje.fecha} {viaje.hora})"
        )
        print(Fore.CYAN + "=" * 98)

        if not pasajes_viaje:
            print(Fore.YELLOW + "No hay pasajes registrados para este viaje.")
            return True

        for p in pasajes_viaje:
            estado_upper = str(p.estado).strip().upper()
            if estado_upper == "HABILITADO":
                etiqueta_estado = Fore.GREEN + "HABILITADO" + Style.RESET_ALL
            else:
                etiqueta_estado = Fore.RED + "ANULADO" + Style.RESET_ALL

            cliente = self.cliente_gestion.buscar_cliente_por_id(p.id_cliente)
            nombre_cli = (
                f"{cliente.nombres} {cliente.apellido_paterno} {cliente.apellido_materno}".strip()
                if cliente
                else f"Cliente ID {p.id_cliente}"
            )
            orig_p = self._nombre_ciudad(p.p_origen)
            dest_p = self._nombre_ciudad(p.p_destino)

            print(
                f"ID Pasaje: {str(p.id_pasaje):<4} | "
                f"Asiento: {int(p.asiento):<3} | "
                f"Pasajero: {nombre_cli[:28]:<28} | "
                f"Tramo: {orig_p} -> {dest_p} | "
                f"Valor: ${int(float(p.valor)):<7} | "
                f"Estado: {etiqueta_estado}"
            )

        print(Fore.CYAN + "=" * 98)
        return True

    def calcular_recaudacion_vigente(self, id_viaje: str) -> tuple[bool, float]:
        viaje = self.pasaje_gestion._buscar_viaje_por_id(id_viaje)
        if not viaje:
            print(Fore.RED + f"Error: No existe un viaje con ID '{id_viaje}'.")
            return False, 0.0

        id_v = str(id_viaje).strip()
        recaudacion = 0.0

        for p in self.pasaje_gestion.pasajes:
            if str(p.id_viaje).strip() != id_v:
                continue
            if str(p.estado).strip().upper() == "HABILITADO":
                recaudacion += float(p.valor)

        origen_v = self._nombre_ciudad(viaje.p_origen)
        destino_v = self._nombre_ciudad(viaje.p_destino)

        print(Fore.CYAN + Style.BRIGHT + "\n=== RECAUDACIÓN DEL VIAJE ===")
        print(f"Viaje #{viaje.id_viaje}: {origen_v} -> {destino_v} ({viaje.fecha} {viaje.hora})")
        print(Fore.GREEN + Style.BRIGHT + f"Recaudación habilitada (excluye ANULADOS): ${recaudacion:,.0f}")
        return True, recaudacion

    def consultar_ocupacion_tramo(self, id_viaje: str, p_origen: str, p_destino: str) -> bool:
        viaje = self.pasaje_gestion._buscar_viaje_por_id(id_viaje)
        if not viaje:
            print(Fore.RED + f"Error: No existe un viaje con ID '{id_viaje}'.")
            return False

        bus = self.bus_gestion.consultar_bus(viaje.id_bus)
        if not bus:
            print(Fore.RED + f"Error: No se encontró el bus '{viaje.id_bus}' asociado al viaje.")
            return False

        pos_o = self.pasaje_gestion._obtener_posicion_ciudad(p_origen)
        pos_d = self.pasaje_gestion._obtener_posicion_ciudad(p_destino)
        if pos_o is None or pos_d is None:
            print(Fore.RED + "Error: Ciudad de origen o destino inválida.")
            return False

        if pos_o == pos_d:
            print(Fore.RED + "Error: El origen y el destino del tramo no pueden ser iguales.")
            return False

        pos_vo = self.pasaje_gestion._obtener_posicion_ciudad(viaje.p_origen)
        pos_vd = self.pasaje_gestion._obtener_posicion_ciudad(viaje.p_destino)
        if pos_vo is not None and pos_vd is not None:
            sentido_viaje = pos_vd > pos_vo
            sentido_tramo = pos_d > pos_o
            if sentido_viaje != sentido_tramo:
                print(Fore.RED + "Error: El tramo no respeta el sentido del viaje.")
                return False
            min_v, max_v = min(pos_vo, pos_vd), max(pos_vo, pos_vd)
            if not (min_v <= pos_o <= max_v and min_v <= pos_d <= max_v):
                print(Fore.RED + "Error: El tramo está fuera del recorrido del viaje.")
                return False

        capacidad = int(bus.capacidad)
        asientos_ocupados: list[int] = []
        asientos_disponibles: list[int] = []

        for asiento in range(1, capacidad + 1):
            disponible = self.pasaje_gestion.reutilizacion_de_asientos_por_tramo(
                id_viaje, asiento, pos_o, pos_d
            )
            if disponible:
                asientos_disponibles.append(asiento)
            else:
                asientos_ocupados.append(asiento)

        nom_o = self._nombre_ciudad(p_origen)
        nom_d = self._nombre_ciudad(p_destino)

        print(Fore.CYAN + Style.BRIGHT + "\n=== OCUPACIÓN Y DISPONIBILIDAD POR TRAMO ===")
        print(f"Viaje #{viaje.id_viaje} | Bus: {bus.patente} (Capacidad: {capacidad} asientos)")
        print(f"Tramo consultado: {nom_o} -> {nom_d}")
        print(
            Fore.RED
            + "Asientos OCUPADOS:    "
            + (Fore.WHITE + ", ".join(map(str, asientos_ocupados)) if asientos_ocupados else Fore.WHITE + "Ninguno")
        )
        print(
            Fore.GREEN
            + "Asientos DISPONIBLES: "
            + (Fore.WHITE + ", ".join(map(str, asientos_disponibles)) if asientos_disponibles else Fore.WHITE + "Ninguno")
        )
        return True