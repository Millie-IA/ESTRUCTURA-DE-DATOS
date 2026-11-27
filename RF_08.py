from colorama import Fore, Style
from RF_01_AL_04 import ClienteGestion, BusGestion, CiudadGestion, ViajeGestion
from RF_05_AL_07 import PasajeGestion


def _texto_limpio(valor: str | None) -> str:
    return "" if valor is None else valor.strip().lower()


def _id_pasaje_key(id_pasaje: str) -> tuple[int, int, str]:
    texto = str(id_pasaje).strip()
    if texto.isdigit():
        return (0, int(texto), texto.lower())
    return (1, 0, texto.lower())


def _obtener_clave_lambda(criterio: str):
    """Retorna una función lambda que construye la tupla de orden y desempate."""
    if criterio == "a":
        return lambda f: (
            _texto_limpio(f["apellido_paterno"]),
            _texto_limpio(f["apellido_materno"]),
            _texto_limpio(f["nombres"]),
            int(f["asiento"]),
            _id_pasaje_key(f["id_pasaje"]),
        )
    if criterio == "b":
        return lambda f: (
            _texto_limpio(f["nombres"]),
            _texto_limpio(f["apellido_paterno"]),
            _texto_limpio(f["apellido_materno"]),
            int(f["asiento"]),
            _id_pasaje_key(f["id_pasaje"]),
        )
    return lambda f: (
        int(f["asiento"]),
        _texto_limpio(f["apellido_paterno"]),
        _texto_limpio(f["apellido_materno"]),
        _texto_limpio(f["nombres"]),
        _id_pasaje_key(f["id_pasaje"]),
    )


def _ordenar_burbuja_nomina(filas: list[dict], criterio: str) -> list[dict]:
    """Ordena una nueva lista usando método burbuja con clave generada por lambda."""
    # ordena por método burbuja 
    copia = list(filas)
    clave_fn = _obtener_clave_lambda(criterio)

    total = len(copia)
    for i in range(total):
        intercambio = False
        for j in range(0, total - i - 1):
            if clave_fn(copia[j]) > clave_fn(copia[j + 1]):
                copia[j], copia[j + 1] = copia[j + 1], copia[j]
                intercambio = True
        if not intercambio:
            break

    return copia


class NominaGestion:
    """RF08: Genera y muestra la nómina de pasajeros habilitados por viaje."""

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

    def _nombre_ciudad_legible(self, dato_ciudad: str) -> str:
        pos = self.pasaje_gestion._obtener_posicion_ciudad(dato_ciudad)
        if pos is not None:
            for c in self.ciudad_gestion.ciudades:
                if int(c.posicion) == pos:
                    return c.ciudad
        return str(dato_ciudad).strip()

    def obtener_nomina_viaje(self, id_viaje: str, criterio: str = "c") -> list[dict]:
        """
        Retorna una NUEVA lista de filas con pasajes HABILITADOS del viaje indicado,
        ordenada por método burbuja según `criterio` ('a', 'b' o 'c') sin alterar el CSV.
        """
        criterio_limpio = str(criterio).strip().lower()
        if criterio_limpio not in ("a", "b", "c"):
            raise ValueError("Criterio de ordenación inválido. Use 'a', 'b' o 'c'.")

        id_viaje_limpio = str(id_viaje).strip()
        filas = []

        for p in self.pasaje_gestion.pasajes:
            if str(p.id_viaje).strip() != id_viaje_limpio:
                continue
            if str(p.estado).strip().upper() != "HABILITADO":
                continue

            cliente = self.cliente_gestion.buscar_cliente_por_id(p.id_cliente)
            if cliente is not None:
                ap_pat = cliente.apellido_paterno
                ap_mat = cliente.apellido_materno
                nombres = cliente.nombres
            else:
                ap_pat = "Sin registro"
                ap_mat = ""
                nombres = f"Cliente #{p.id_cliente}"

            filas.append({
                "id_pasaje": p.id_pasaje,
                "asiento": int(p.asiento),
                "apellido_paterno": ap_pat,
                "apellido_materno": ap_mat,
                "nombres": nombres,
                "ciudad_embarque": self._nombre_ciudad_legible(p.p_origen),
                "destino_final": self._nombre_ciudad_legible(p.p_destino),
            })

        return _ordenar_burbuja_nomina(filas, criterio_limpio)

    def mostrar_nomina_viaje(self, id_viaje: str, criterio: str = "c") -> bool:
        """Valida el viaje e imprime la nómina de pasajes habilitados."""
        viaje = self.pasaje_gestion._buscar_viaje_por_id(id_viaje)
        if not viaje:
            print(Fore.RED + f"Error: No se encontró un viaje con ID '{id_viaje}'.")
            return False

        try:
            filas = self.obtener_nomina_viaje(id_viaje, criterio)
        except ValueError as e:
            print(Fore.RED + f"Error: {e}")
            return False

        origen_viaje = self._nombre_ciudad_legible(viaje.p_origen)
        destino_viaje = self._nombre_ciudad_legible(viaje.p_destino)
        bus = self.bus_gestion.consultar_bus(viaje.id_bus)
        if bus is not None:
            patente_info = f" | Bus: {bus.patente} (ID {viaje.id_bus})"
        else:
            patente_info = f" | Bus ID: {viaje.id_bus}"

        crit = str(criterio).strip().lower()
        if crit == "a":
            etiqueta_criterio = "Apellido paterno (A-Z)"
        elif crit == "b":
            etiqueta_criterio = "Nombres (A-Z)"
        else:
            etiqueta_criterio = "Número de asiento (ascendente)"

        print(Fore.CYAN + Style.BRIGHT + "\n" + "=" * 95)
        print(
            Fore.CYAN + Style.BRIGHT
            + f"NÓMINA DE PASAJEROS HABILITADOS — VIAJE #{viaje.id_viaje} "
            + f"({origen_viaje} -> {destino_viaje} | {viaje.fecha} {viaje.hora}{patente_info})"
        )
        print(Fore.YELLOW + f"Ordenado por: {etiqueta_criterio} (método burbuja)")
        print(Fore.CYAN + "=" * 95)

        if not filas:
            print(Fore.YELLOW + "No hay pasajes habilitados registrados para este viaje.")
            return True

        encabezado = (
            f"{'Asiento':<8} | {'Apellido Paterno':<18} | {'Apellido Materno':<18} | "
            f"{'Nombres':<20} | {'Embarque':<14} | {'Destino Final':<14}"
        )
        print(Fore.GREEN + Style.BRIGHT + encabezado)
        print("-" * 95)

        for r in filas:
            print(
                f"{r['asiento']:<8} | "
                f"{str(r['apellido_paterno'])[:18]:<18} | "
                f"{str(r['apellido_materno'])[:18]:<18} | "
                f"{str(r['nombres'])[:20]:<20} | "
                f"{str(r['ciudad_embarque'])[:14]:<14} | "
                f"{str(r['destino_final'])[:14]:<14}"
            )

        print(Fore.CYAN + "=" * 95)
        return True