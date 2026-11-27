# CREAR DEF CON LO SOLICITADO

# Utilizar diccionarios / listas, es mejor que clases / POO

'''
--> Integrante 2 (Diego): Lógica de Negocio Central (Tramos, Asientos y Anulaciones)Este es el núcleo algorítmico del sistema y requiere lógica detallada.
 Responsabilidades:
  - RF05 (Ventas de pasajes): Registrar ventas calculando automáticamente la tarifa según los segmentos no utilizados (descuento acumulativo del 10%
  por cada segmento no recorrido).
  - RF06 (Reutilización de asientos por tramo): Validar si un asiento está libre cruzando los tramos (origen/destino) para permitir superposiciones
  en tramos consecutivos (ej. Asiento 12: Concepción-Chillán, luego Chillán-Talca).
  - RF07 (Anulación de pasajes): Permitir anular un pasaje cambiando su estado, liberando el asiento exclusivamente en el tramo afectado y evitando
  anulaciones repetidas.

--> GENERAL:
Interfaz y Usabilidad: Diseñar el menú interactivo en consola integrando obligatoriamente la biblioteca colorama para títulos, errores y advertencias.
Preparar el archivo requirements.txt y la documentación en el README.md.   

'''
def VentasDePasajes():
  """
  Registrar un pasaje con ID único, ID de cliente, ID de viaje, origen y destino del pasajero, asiento seleccionado 
  manualmente y precio calculado. Validar que el cliente y el viaje existan, el tramo respete el sentido del viaje y el asiento  
  esté dentro de la capacidad del bus. 
"""
  pass
# RF05 (Ventas de pasajes): Registrar ventas calculando automáticamente la tarifa según los segmentos no utilizados (descuento acumulativo del 10%
# por cada segmento no recorrido).


def reutilizacion_de_asientos_por_tramo():
  """ Un mismo asiento podrá asignarse a varios pasajeros en un viaje únicamente si sus tramos no se superponen. Ejemplo 
  válido: asiento 12 Concepción–Chillán; luego Chillán–Talca; después Talca–Santiago. Ejemplo inválido: asiento 12 
  Chillán–Talca y Linares–Rancagua, porque existe superposición. 
  El descenso en una ciudad libera el asiento para un embarque en esa misma ciudad. La validación debe considerar el 
  sentido del viaje, las ventas vigentes y los datos persistidos tras reiniciar la aplicación.
"""
  
  pass
#Validar si un asiento está libre cruzando los tramos (origen/destino) para permitir superposiciones
#en tramos consecutivos (ej. Asiento 12: Concepción-Chillán, luego Chillán-Talca).

def anulacionDePasajes():
  """permitir anular una venta existente mediante su identificador. El registro deberá conservar una condición o estado que 
permita distinguir pasajes vigentes y anulados. La anulación liberará el asiento SOLO en el tramo anulado, sin modificar 
otras ventas. Las ventas anuladas no participarán en las validaciones de ocupación ni en la recaudación vigente; el 
sistema deberá evitar anulaciones repetidas. """
  pass
#Permitir anular un pasaje cambiando su estado, liberando el asiento exclusivamente en el tramo afectado y evitando
#anulaciones repetidas.