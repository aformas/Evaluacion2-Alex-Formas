import requests
import urllib.parse

# URLs de los servicios de Graphhopper
API_GEO_URL = "https://graphhopper.com/api/1/geocode?"
API_ROUTE_URL = "https://graphhopper.com/api/1/route?"
LENGUAJE = "es"

# Clave de API proporcionada
API_KEY = "de456df5-f99f-43f9-b252-cffab25d8119"

def obtener_coordenadas(lugar, clave):
    # Asegurarnos de que el usuario no envíe un lugar vacío
    while not lugar.strip():
        lugar = input("La ubicación no puede estar vacía. Intenta de nuevo: ")
    
    # Construcción de la URL de búsqueda
    parametros_geo = urllib.parse.urlencode({"q": lugar, "limit": "1", "key": clave, "locale": LENGUAJE})
    url_final = API_GEO_URL + parametros_geo

    respuesta_servidor = requests.get(url_final)
    datos_json = respuesta_servidor.json()
    codigo_estado = respuesta_servidor.status_code

    if codigo_estado == 200 and len(datos_json["hits"]) > 0:
        primer_resultado = datos_json["hits"][0]
        latitud = primer_resultado["point"]["lat"]
        longitud = primer_resultado["point"]["lng"]
        nombre = primer_resultado["name"]
        tipo_lugar = primer_resultado["osm_value"]
        
        pais = primer_resultado.get("country", "")
        estado = primer_resultado.get("state", "")
        
        # Formateando el nombre completo del lugar
        if estado and pais:
            lugar_formateado = f"{nombre}, {estado}, {pais}"
        elif estado:
            lugar_formateado = f"{nombre}, {estado}"
        else:
            lugar_formateado = nombre
        
        print(f"> Geocodificación exitosa para: {lugar_formateado} (Tipo: {tipo_lugar})")
        print(f"> URL consultada: {url_final}\n")
    else:
        latitud, longitud = "null", "null"
        lugar_formateado = lugar
        if codigo_estado != 200:
            print(f"[ERROR] Código: {codigo_estado}")
            print(f"[MENSAJE] {datos_json.get('message', 'No se encontró el lugar')}")
            
    return codigo_estado, latitud, longitud, lugar_formateado


# Flujo principal de la aplicación
while True:
    print("\n" + "#" * 60)
    print("      ASISTENTE DE PLANIFICACIÓN DE RUTAS      ")
    print(" (Para cerrar el programa escribe 'q', 's' o 'salir')")
    print("#" * 60)
    
    punto_a = input("\n[1] Ingresa el punto de partida: ")
    if punto_a.strip().lower() in ["salir", "s", "quit", "q"]:
        print("\nCerrando el asistente... ¡Buen viaje!")
        break
        
    datos_origen = obtener_coordenadas(punto_a, API_KEY)
    if datos_origen[0] != 200:
        continue

    punto_b = input("[2] Ingresa el punto de destino: ")
    if punto_b.strip().lower() in ["salir", "s", "quit", "q"]:
        print("\nCerrando el asistente... ¡Buen viaje!")
        break
        
    datos_destino = obtener_coordenadas(punto_b, API_KEY)
    if datos_destino[0] != 200:
        continue
    
    print("-" * 60)
    if datos_origen[0] == 200 and datos_destino[0] == 200:
        coordenadas_origen = f"&point={datos_origen[1]}%2C{datos_origen[2]}"
        coordenadas_destino = f"&point={datos_destino[1]}%2C{datos_destino[2]}"
        
        # Parámetros para trazar la ruta en automóvil
        url_ruta = API_ROUTE_URL + urllib.parse.urlencode({"key": API_KEY, "locale": LENGUAJE, "vehicle": "car"}) + coordenadas_origen + coordenadas_destino
        
        peticion_ruta = requests.get(url_ruta)
        estado_ruta = peticion_ruta.status_code
        info_ruta = peticion_ruta.json()
        
        print(f"URL de Ruta Generada:\n{url_ruta}\n")
        print(f"--- RESUMEN DEL VIAJE: {datos_origen[3]} -> {datos_destino[3]} ---")
        
        if estado_ruta == 200:
            # Cálculos de distancia y tiempo (vienen en metros y milisegundos)
            dist_metros = info_ruta["paths"][0]["distance"]
            tiempo_milisegundos = info_ruta["paths"][0]["time"]
            
            # Conversiones
            dist_km = dist_metros / 1000
            dist_mi = dist_km / 1.61
            
            tiempo_seg = int((tiempo_milisegundos / 1000) % 60)
            tiempo_min = int((tiempo_milisegundos / 1000 / 60) % 60)
            tiempo_hr = int(tiempo_milisegundos / 1000 / 3600)
            
            print(f"Total a recorrer: {dist_km:.2f} Kilómetros ({dist_mi:.2f} Millas)")
            print(f"Tiempo estimado: {tiempo_hr} horas, {tiempo_min} minutos, {tiempo_seg} segundos")
            print("-" * 60)
            print("GUÍA DE NAVEGACIÓN:")
            print("-" * 60)
            
            # Desglose de las direcciones paso a paso
            for movimiento in info_ruta["paths"][0]["instructions"]:
                instruccion = movimiento["text"]
                distancia_movimiento = movimiento["distance"] / 1000
                distancia_mov_mi = distancia_movimiento / 1.61
                
                print(f" -> {instruccion} (Distancia: {distancia_movimiento:.2f} km / {distancia_mov_mi:.2f} mi)")
                
            print("-" * 60 + "\n")
        else:
            print(f"[ERROR DE RUTA] {info_ruta.get('message', 'No se pudo trazar una ruta entre estos puntos')}")
            print("-" * 60 + "\n")
