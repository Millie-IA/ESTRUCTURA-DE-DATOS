from typing import List, Optional
from modelos.entidades import Cliente
from ruta_datos import ARCHIVO_CLIENTES, ENCODE


def _asegurar_archivo_clientes() -> None:
    try:
        with open(ARCHIVO_CLIENTES, "r", encoding=ENCODE):
            return
    except FileNotFoundError:
        with open(ARCHIVO_CLIENTES, "w", encoding=ENCODE) as f:
            f.write("id_cliente,rut,nombres,apellido_paterno,apellido_materno,contacto\n")
    except OSError as exc:
        raise RuntimeError(f"No se pudo acceder al archivo de clientes: {exc}") from exc


def _limpiar_campo_csv(valor: str) -> str:
    partes = [p for p in valor.strip().replace(",", " ").split(" ") if p != ""]
    return " ".join(partes)


#Esta funcion aunque parezca redundante, es necesaria para separar los nombres y capitalizar ambos
def _capitalizar_palabra(texto: str) -> str:
    limpio = _limpiar_campo_csv(texto)
    if limpio == "":
        return ""
    return " ".join(map(lambda p: p.capitalize(), limpio.split(" ")))


def _limpiar_rut_crudo(rut: str) -> str:
    return "".join(ch for ch in rut.strip().upper() if ch.isalnum())


def _calcular_dv_rut(cuerpo: str) -> str:
    acumulador = 0
    multiplicador = 2

    for digito in reversed(cuerpo):
        acumulador += int(digito) * multiplicador
        multiplicador = 2 if multiplicador == 7 else multiplicador + 1

    resto = acumulador % 11
    calculado = 11 - resto

    if calculado == 11:
        return "0"
    if calculado == 10:
        return "K"
    return str(calculado)


def validar_y_formatear_rut(rut: str) -> str:
    limpio = _limpiar_rut_crudo(rut)
    if len(limpio) < 2:
        raise ValueError("RUT inválido: debe incluir cuerpo y dígito verificador.")

    cuerpo = limpio[:-1]
    dv_ingresado = limpio[-1]

    if not cuerpo.isdigit():
        raise ValueError("RUT inválido: el cuerpo debe contener solo números.")

    if dv_ingresado != "K" and not dv_ingresado.isdigit():
        raise ValueError("RUT inválido: el dígito verificador debe ser un número o 'K'.")

    cuerpo_sin_ceros = cuerpo.lstrip("0")
    if cuerpo_sin_ceros == "" or len(cuerpo_sin_ceros) < 7 or len(cuerpo_sin_ceros) > 8:
        raise ValueError("RUT inválido: el cuerpo del RUT no tiene una longitud válida.")

    dv_esperado = _calcular_dv_rut(cuerpo_sin_ceros)
    if dv_ingresado != dv_esperado:
        raise ValueError("RUT inválido: el dígito verificador no corresponde al RUT.")

    grupos: List[str] = []
    for i in range(len(cuerpo_sin_ceros), 0, -3):
        inicio = max(0, i - 3)
        grupos.append(cuerpo_sin_ceros[inicio:i])
    grupos.reverse()

    return f"{'.'.join(grupos)}-{dv_ingresado}"


def _obtener_siguiente_id_cliente(clientes: List[Cliente]) -> int:
    max_id = max((c.id_cliente for c in clientes), default=0)
    return max_id + 1


def listar_clientes() -> List[Cliente]:
    _asegurar_archivo_clientes()
    clientes: List[Cliente] = []
    try:
        with open(ARCHIVO_CLIENTES, "r", encoding=ENCODE) as f:
            lineas = f.readlines()

        for linea in lineas[1:]:
            linea_limpia = linea.strip()
            if linea_limpia == "":
                continue
            partes = linea_limpia.split(",")
            if len(partes) < 6:
                continue

            cliente = Cliente(
                id_cliente=int(partes[0].strip()),
                rut=partes[1].strip().upper(),
                nombres=_capitalizar_palabra(partes[2]),
                apellido_paterno=_capitalizar_palabra(partes[3]),
                apellido_materno=_capitalizar_palabra(partes[4]),
                contacto=_limpiar_campo_csv(partes[5]),
            )
            clientes.append(cliente)
    except (OSError, ValueError) as exc:
        raise RuntimeError(f"Error al leer clientes: {exc}") from exc

    return clientes


def buscar_cliente_por_id(id_cliente: int) -> Optional[Cliente]:
    clientes: List[Cliente] = listar_clientes()
    return next((c for c in clientes if c.id_cliente == id_cliente), None)


def buscar_cliente_por_rut(rut: str) -> Optional[Cliente]:
    rut_buscado = _limpiar_rut_crudo(rut)
    if rut_buscado == "":
        return None

    clientes: List[Cliente] = listar_clientes()
    buscar_coincidencia = lambda c: _limpiar_rut_crudo(c.rut) == rut_buscado
    return next((c for c in clientes if buscar_coincidencia(c)), None)


def buscar_cliente_por_rut(rut: str) -> Optional[Cliente]:
    clientes: List[Cliente] = listar_clientes()
    try:
        rut_formateado = validar_y_formatear_rut(rut)
        return next(
            (c for c in clientes if c.rut.strip().upper() == rut_formateado),
            None,
        )
    except ValueError:
        rut_crudo = _limpiar_rut_crudo(rut)
        if rut_crudo == "":
            return None
        return next(
            (c for c in clientes if _limpiar_rut_crudo(c.rut) == rut_crudo),
            None,
        )


def registrar_cliente(
    rut: str,
    primer_nombre: str,
    segundo_nombre: str,
    apellido_paterno: str,
    apellido_materno: str,
    contacto: str,
) -> Cliente:
    rut_formateado = validar_y_formatear_rut(rut)
    primer_nombre_cap = _capitalizar_palabra(primer_nombre)
    segundo_nombre_cap = _capitalizar_palabra(segundo_nombre)
    ap_paterno_cap = _capitalizar_palabra(apellido_paterno)
    ap_materno_cap = _capitalizar_palabra(apellido_materno)
    contacto_limpio = _limpiar_campo_csv(contacto)

    if primer_nombre_cap == "":
        raise ValueError("El primer nombre es obligatorio.")
    if ap_paterno_cap == "":
        raise ValueError("El apellido paterno es obligatorio.")
    if ap_materno_cap == "":
        raise ValueError("El apellido materno es obligatorio.")
    if contacto_limpio == "":
        raise ValueError("El contacto es obligatorio.")

    nombres_unidos = (
        f"{primer_nombre_cap} {segundo_nombre_cap}".strip()
        if segundo_nombre_cap != ""
        else primer_nombre_cap
    )

    clientes_actuales: List[Cliente] = listar_clientes()
    rut_crudo_nuevo = _limpiar_rut_crudo(rut_formateado)
    if any(
        c.rut.strip().upper() == rut_formateado
        or _limpiar_rut_crudo(c.rut) == rut_crudo_nuevo
        for c in clientes_actuales
    ):
        raise ValueError(
            f"Ya existe un cliente registrado con el RUT {rut_formateado}."
        )

    nuevo_id = _obtener_siguiente_id_cliente(clientes_actuales)
    nuevo_cliente = Cliente(
        id_cliente=nuevo_id,
        rut=rut_formateado,
        nombres=nombres_unidos,
        apellido_paterno=ap_paterno_cap,
        apellido_materno=ap_materno_cap,
        contacto=contacto_limpio,
    )

    try:
        necesita_salto = False
        with open(ARCHIVO_CLIENTES, "rb") as f_bin:
            f_bin.seek(0, 2)
            if f_bin.tell() > 0:
                f_bin.seek(-1, 2)
                if f_bin.read(1) != b"\n":
                    necesita_salto = True

        with open(ARCHIVO_CLIENTES, "a", encoding=ENCODE) as f:
            prefijo = "\n" if necesita_salto else ""
            linea_csv = (
                f"{prefijo}"
                f"{nuevo_cliente.id_cliente},"
                f"{nuevo_cliente.rut},"
                f"{nuevo_cliente.nombres},"
                f"{nuevo_cliente.apellido_paterno},"
                f"{nuevo_cliente.apellido_materno},"
                f"{nuevo_cliente.contacto}\n"
            )
            f.write(linea_csv)
    except OSError as exc:
        raise RuntimeError(f"Error al guardar el cliente: {exc}") from exc

    return nuevo_cliente