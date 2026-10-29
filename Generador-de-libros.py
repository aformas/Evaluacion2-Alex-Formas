import requests
import random

# Definición de las URLs de la API
ENDPOINT_AUTH = "http://library.demo.local/api/v1/loginViaBasic"
ENDPOINT_LIBROS = "http://library.demo.local/api/v1/books"

# 1. Autenticación en el sistema
print("Iniciando solicitud de token...")
respuesta_auth = requests.post(ENDPOINT_AUTH, auth=('cisco', 'Cisco123!'))

if respuesta_auth.status_code == 200:
    token_acceso = respuesta_auth.json().get("token")
    print("¡Token de seguridad obtenido con éxito!\n")
else:
    print(f"Error de credenciales. Código de estado: {respuesta_auth.status_code}")
    exit()

# Configuración de las cabeceras HTTP
cabeceras = {
    "X-API-KEY": token_acceso,
    "Content-Type": "application/json"
}

# 2. Configuración de datos para la generación de libros
tipos_libro = ["Manual de", "Implementación de", "Fundamentos de", "Guía Avanzada de", "Laboratorios de"]
tecnologias = ["Routing", "Switching", "Seguridad", "Data Center", "Wireless", "Python para Redes"]

AUTOR_ASIGNADO = "Alex_Fornas"
ISBN_ASIGNADO = "219365810"

print("--- Insertando 50 registros en la base de datos ---")

for id_actual in range(100, 150):
    titulo_aleatorio = f"{random.choice(tipos_libro)} {random.choice(tecnologias)} v{random.randint(1, 7)}.0"
    
    cuerpo_peticion = {
        "id": id_actual,
        "title": titulo_aleatorio,
        "author": AUTOR_ASIGNADO,
        "isbn": ISBN_ASIGNADO
    }
    
    peticion_post = requests.post(ENDPOINT_LIBROS, json=cuerpo_peticion, headers=cabeceras)
    
    if peticion_post.status_code == 200:
        print(f"[ÉXITO] ID {id_actual} añadido: {titulo_aleatorio}")
    else:
        print(f"[FALLO] No se insertó el ID {id_actual}. Error: {peticion_post.status_code}")

# 3. Consulta y visualización de TODO el catálogo (Paginado)
print("\n********************************************************")
print("               INVENTARIO DE LA BIBLIOTECA              ")
print("********************************************************")

pagina_actual = 1
coleccion_total = []

# Bucle para consultar todas las páginas disponibles
while True:
    parametros_busqueda = {"includeISBN": "true", "page": pagina_actual}
    respuesta_catalogo = requests.get(ENDPOINT_LIBROS, params=parametros_busqueda)

    if respuesta_catalogo.status_code == 200:
        libros_pagina = respuesta_catalogo.json()
        
        # Si la lista vuelve vacía, significa que ya no hay más páginas
        if not libros_pagina:
            break
            
        coleccion_total.extend(libros_pagina)
        pagina_actual += 1
    else:
        print(f"Hubo un problema al recuperar la página {pagina_actual}.")
        break

# Mostrar todos los libros recopilados
for obra in coleccion_total:
    print(f"[{obra.get('id')}] {obra.get('title')} | Escrito por: {obra.get('author')} | Cód. ISBN: {obra.get('isbn', 'Desconocido')}")

print(f"\n>>> Conteo total de obras en el sistema: {len(coleccion_total)} <<<")
