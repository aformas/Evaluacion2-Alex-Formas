Asistente de Planificación de Rutas (Graphhopper API)
Este proyecto es un script interactivo en Python que se conecta con la API de Graphhopper para proporcionar servicios de geocodificación y cálculo de rutas. Permite a los usuarios ingresar ubicaciones de origen y destino en texto plano, devolviendo información detallada del viaje que incluye distancias, tiempos estimados y direcciones de navegación paso a paso.

Características

Geocodificación Inteligente: Convierte nombres de ciudades, direcciones o lugares de interés en coordenadas geográficas (latitud y longitud) precisas.

Cálculo de Rutas para Vehículos: Genera trayectos optimizados basados en perfiles de conducción de automóviles.

Métricas Detalladas de Viaje: Desglosa la distancia total a recorrer (en kilómetros y millas) y el tiempo estimado de viaje (en horas, minutos y segundos).

Guía de Navegación Paso a Paso: Proporciona instrucciones de conducción iterativas en español para todo el trayecto.

Validación de Errores: Maneja entradas vacías y ubicaciones no encontradas, mostrando mensajes de error claros desde la API.

Requisitos Previos
Python 3.6 o superior.

La librería externa requests. Puedes instalarla mediante pip:

Bash
pip install requests
Una API Key válida de Graphhopper. Puedes obtener una cuenta gratuita en el Dashboard de Graphhopper.

Instalación y Configuración
Clona este repositorio en tu máquina local:

Bash
git clone https://github.com/tu-usuario/tu-repositorio.git
cd tu-repositorio
Configura tu API Key:
Abre el archivo principal del script (por ejemplo, ruta_graphhopper.py) en tu editor de código preferido y ubica la constante API_KEY. Reemplaza el valor con tu clave personal:

Python
API_KEY = "tu_api_key_personal_aqui"
Ejecuta la aplicación:

Bash
python ruta_graphhopper.py
💻 Uso de la Aplicación
Al ejecutar el script, la terminal mostrará un menú interactivo.

El sistema te solicitará el punto de partida. Ingresa una ciudad, país o dirección (ej. Madrid, España).

Una vez validado el origen, ingresa el punto de destino.

El programa calculará las coordenadas, procesará la ruta y te entregará el resumen completo del viaje junto con las instrucciones paso a paso.

Para terminar la ejecución en cualquier momento, simplemente escribe q, s o salir cuando se te pida una ubicación.

Ejemplo de Salida en Terminal
Plaintext
############################################################
      ASISTENTE DE PLANIFICACIÓN DE RUTAS      
 (Para cerrar el programa escribe 'q', 's' o 'salir')
############################################################

[1] Ingresa el punto de partida: Santiago, Chile
> Geocodificación exitosa para: Santiago, Región Metropolitana, Chile (Tipo: city)

[2] Ingresa el punto de destino: Valparaíso, Chile
> Geocodificación exitosa para: Valparaíso, Región de Valparaíso, Chile (Tipo: city)

------------------------------------------------------------
--- RESUMEN DEL VIAJE: Santiago... -> Valparaíso... ---
Total a recorrer: 115.50 Kilómetros (71.74 Millas)
Tiempo estimado: 1 horas, 20 minutos, 15 segundos
------------------------------------------------------------
GUÍA DE NAVEGACIÓN:
------------------------------------------------------------
 -> Continúa hacia el norte en Avenida Libertador Bernardo O'Higgins (Distancia: 0.50 km / 0.31 mi)
 -> Gira a la derecha en Ruta 68 (Distancia: 105.00 km / 65.21 mi)
 -> Llega a tu destino (Distancia: 0.00 km / 0.00 mi)
------------------------------------------------------------
🛠️ Tecnologías y Dependencias
Lenguaje: Python 3

Librerías estándar: urllib.parse (para la codificación segura de parámetros URL).

Librerías de terceros: requests (para el manejo de peticiones HTTP GET).

APIs externas: Graphhopper Routing API (utilizando los endpoints /geocode y /route).
