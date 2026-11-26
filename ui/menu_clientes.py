from controladores.clientes_controller import (
    buscar_cliente_por_id,
    buscar_cliente_por_rut,
    listar_clientes,
    registrar_cliente,
)
from ui.estilos_ui import (
    leer_entero,
    leer_texto_no_vacio,
    limpiar_pantalla,
    mensaje_advertencia,
    mensaje_error,
    mensaje_exito,
    mensaje_info,
    mensaje_opcion,
    pausar,
    subtitulo,
    titulo_seccion,
)
from modelos.entidades import Cliente


def _imprimir_cliente(cliente: Cliente) -> None:
    nombre_completo = (
        f"{cliente.nombres} {cliente.apellido_paterno} {cliente.apellido_materno}".strip()
    )
    mensaje_info(
        f"ID: {cliente.id_cliente} | RUT: {cliente.rut} | "
        f"Nombre: {nombre_completo} | Contacto: {cliente.contacto}"
    )


def _opcion_registrar_cliente() -> None:
    limpiar_pantalla()
    subtitulo("Registrar Cliente")

    rut = leer_texto_no_vacio("RUT: ")
    primer_nombre = leer_texto_no_vacio("Primer nombre: ")
    segundo_nombre = input("Segundo nombre (opcional, Enter para omitir): ").strip()
    apellido_paterno = leer_texto_no_vacio("Apellido paterno: ")
    apellido_materno = leer_texto_no_vacio("Apellido materno: ")
    contacto = leer_texto_no_vacio("Contacto: ")

    try:
        cliente_creado: Cliente = registrar_cliente(
            rut=rut,
            primer_nombre=primer_nombre,
            segundo_nombre=segundo_nombre,
            apellido_paterno=apellido_paterno,
            apellido_materno=apellido_materno,
            contacto=contacto,
        )
        nombre_completo = (
            f"{cliente_creado.nombres} {cliente_creado.apellido_paterno} "
            f"{cliente_creado.apellido_materno}".strip()
        )
        mensaje_exito(
            f"Cliente registrado: {nombre_completo} (ID {cliente_creado.id_cliente})."
        )
    except ValueError as exc:
        mensaje_error(f"Validacion: {exc}")
    except RuntimeError as exc:
        mensaje_error(f"Sistema: {exc}")

    pausar()


def _opcion_listar_clientes() -> None:
    limpiar_pantalla()
    subtitulo("Listado de Clientes")

    try:
        clientes = listar_clientes()
        if len(clientes) == 0:
            mensaje_advertencia("No hay clientes registrados.")
        else:
            for cliente in clientes:
                _imprimir_cliente(cliente)
    except RuntimeError as exc:
        mensaje_error(f"Sistema: {exc}")

    pausar()


def _opcion_buscar_por_id() -> None:
    limpiar_pantalla()
    subtitulo("Buscar Cliente por ID")

    id_cliente = leer_entero("Ingrese ID del cliente: ")

    try:
        cliente = buscar_cliente_por_id(id_cliente)
        if cliente is None:
            mensaje_advertencia("Cliente no encontrado.")
        else:
            _imprimir_cliente(cliente)
    except RuntimeError as exc:
        mensaje_error(f"Sistema: {exc}")

    pausar()


def _opcion_buscar_por_rut() -> None:
    limpiar_pantalla()
    subtitulo("Buscar Cliente por RUT")

    rut = leer_texto_no_vacio("Ingrese RUT del cliente: ")

    try:
        cliente = buscar_cliente_por_rut(rut)
        if cliente is None:
            mensaje_advertencia("Cliente no encontrado.")
        else:
            _imprimir_cliente(cliente)
    except RuntimeError as exc:
        mensaje_error(f"Sistema: {exc}")

    pausar()


def menu_clientes() -> None:
    while True:
        limpiar_pantalla()
        titulo_seccion("MENU DE CLIENTES")
        mensaje_opcion("1. Registrar cliente")
        mensaje_opcion("2. Listar clientes")
        mensaje_opcion("3. Buscar cliente por ID")
        mensaje_opcion("4. Buscar cliente por RUT")
        mensaje_opcion("0. Volver al menu principal")

        opcion = input("\nSeleccione opcion: ").strip()

        if opcion == "1":
            _opcion_registrar_cliente()
        elif opcion == "2":
            _opcion_listar_clientes()
        elif opcion == "3":
            _opcion_buscar_por_id()
        elif opcion == "4":
            _opcion_buscar_por_rut()
        elif opcion == "0":
            break
        else:
            mensaje_error("Opcion no valida.")
            pausar()