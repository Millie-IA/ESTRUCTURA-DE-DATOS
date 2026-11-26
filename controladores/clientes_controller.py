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
                rut=partes[1].strip(),
                nombres=partes[2].strip(),
                apellido_paterno=partes[3].strip(),
                apellido_materno=partes[4].strip(),
                contacto=partes[5].strip(),
            )
            clientes.append(cliente)
    except (OSError, ValueError) as exc:
        raise RuntimeError(f"Error al leer clientes: {exc}") from exc

    return clientes


def buscar_cliente_por_id(id_cliente: int) -> Optional[Cliente]:
    clientes: List[Cliente] = listar_clientes()
    for cliente in clientes:
        if cliente.id_cliente == id_cliente:
            return cliente
    return None

def buscar_cliente_por_rut(rut: str) -> Optional[Cliente]:
    rut_normalizado = rut.strip().upper()
    clientes: List[Cliente] = listar_clientes()
    for cliente in clientes:
        if cliente.rut.strip().upper() == rut_normalizado:
            return cliente
    return None