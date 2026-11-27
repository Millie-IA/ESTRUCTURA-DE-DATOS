# ESTRUCTURA-DE-DATOS
'''
### INTEGRANTES DEL PROYECTO:
    - Alejandro Jarpa
    - Diego Saavedra
    - Mylenne Durán

### INSTALACIÓN
Abrir terminal de Python con una versión superior o igual a 3.11

Escribir los siguientes comandos:
-> Instalación de la biblioteca requeridas
pip install -r requirements.txt

### EJECUCIÓN
Abrir la terminal de Python en la carpeta raíz del proyecto y ejecutar:
python App.py

### REPARTO DE TAREAS
--> Integrante 1 (Mylenne): Módulo Base, Persistencia y CRUD de Entidades
Este integrante sienta las bases del proyecto para que los demás puedan consumir los datos.

 Responsabilidades: Implementar el sistema de persistencia en archivos (CSV) asegurando que maneje archivos vacíos o inexistentes sin caídas.
  - RF01 (Clientes): Registro, listado, búsqueda y validación de RUTs duplicados.   
  - RF02 (Buses): Registro, listado y consulta de buses.   
  - RF03 y RF04 (Ciudades y Viajes): Cargar el catálogo fijo de las 6 ciudades y programar los viajes (Concepción-Santiago / Santiago-Concepción) con su tarifa base.

--> Integrante 2 (Diego): Lógica de Negocio Central (Tramos, Asientos y Anulaciones)
Este es el núcleo algorítmico del sistema y requiere lógica detallada.

 Responsabilidades:
  - RF05 (Ventas de pasajes): Registrar ventas calculando automáticamente la tarifa según los segmentos no utilizados (descuento acumulativo del 10% por cada segmento no recorrido).
  - RF06 (Reutilización de asientos por tramo): Validar si un asiento está libre cruzando los tramos (origen/destino) para permitir superposiciones
  en tramos consecutivos (ej. Asiento 12: Concepción-Chillán, luego Chillán-Talca).
  - RF07 (Anulación de pasajes): Permitir anular un pasaje cambiando su estado, liberando el asiento exclusivamente en el tramo afectado y evitando anulaciones repetidas.

--> Integrante 3 (Alejandro): Reportes, Nóminas, Algoritmos de Ordenamiento y UI (Consola)
Este integrante se encarga de la visualización, la experiencia de usuario y de cumplir con las técnicas algorítmicas obligatorias de la sección 5.

 Responsabilidades:
  - RF08 (Nómina de pasajeros): Desarrollar la nómina por viaje. Atención: Debe implementar un algoritmo de ordenamiento manual (como Bubble Sort o Insertion Sort) para ordenar por apellido paterno, nombre o número de asiento, ya que la pauta prohíbe resolverlo únicamente con sort() o sorted().
  - RF09 (Consultas y reportes): Mostrar pasajes vigentes/anulados, recaudación vigente del viaje y ocupación de asientos por tramo.

### ORGANIZACIÓN DEL PROYECTO
Los requerimientos de código se distribuyen en módulos específicos por integrante (por ejemplo, RF_01_AL_04.py).

La persistencia de datos se gestiona mediante archivos CSV para cada entidad.

Los menús de interacción con el usuario se centralizan en el archivo App.py.

### ESTRUCTURAS / ALGORITMOS UTILIZADOS
Programación Orientada a Objetos (Simulada): Se estructuró el código mediante clases para las entidades del dominio y clases gestoras para mantener una arquitectura limpia y organizada.

Algoritmos de Búsqueda: Se implementó búsqueda secuencial dentro de los métodos de gestión y búsqueda de entidades.

Algoritmos de Ordenamiento: Se utilizó Bubble Sort para ordenar las nóminas de pasajeros por viaje de manera manual en el módulo correspondiente.
'''
