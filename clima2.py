# ==========================================
# Aplicación simple de clima con Open-Meteo
# ==========================================

# Librería necesaria:
# Instalar con:
# pip install requests

import requests

# ------------------------------------------
# Constantes
# ------------------------------------------

# URL de la API de geocodificación
GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"

# URL de la API del clima
WEATHER_URL = "https://api.open-meteo.com/v1/forecast"

# Tiempo máximo de espera de la petición
TIMEOUT = 10


# ------------------------------------------
# Función para traducir códigos del clima
# ------------------------------------------
def obtener_descripcion_clima(weather_code):
    """
    Convierte el código del clima en un texto entendible.
    """

    codigos_clima = {
        0: "Despejado",
        1: "Principalmente despejado",
        2: "Parcialmente nublado",
        3: "Nublado",
        45: "Niebla",
        48: "Niebla con escarcha",
        51: "Llovizna ligera",
        53: "Llovizna moderada",
        55: "Llovizna intensa",
        61: "Lluvia ligera",
        63: "Lluvia moderada",
        65: "Lluvia fuerte",
        71: "Nieve ligera",
        73: "Nieve moderada",
        75: "Nieve intensa",
        80: "Chubascos ligeros",
        81: "Chubascos moderados",
        82: "Chubascos fuertes",
        95: "Tormenta"
    }

    return codigos_clima.get(weather_code, "Clima desconocido")


# ------------------------------------------
# Función para obtener coordenadas
# ------------------------------------------
def obtener_coordenadas(ciudad):
    """
    Busca la latitud y longitud de una ciudad.
    """

    parametros = {
        "name": ciudad,
        "count": 1,
        "language": "es",
        "format": "json"
    }

    try:
        respuesta = requests.get(
            GEOCODING_URL,
            params=parametros,
            timeout=TIMEOUT
        )

        # Verifica si la respuesta fue correcta
        respuesta.raise_for_status()

        datos = respuesta.json()

        # Verifica si la ciudad existe
        if "results" not in datos:
            print("Error: Ciudad no encontrada.")
            return None

        ciudad_info = datos["results"][0]

        return {
            "nombre": ciudad_info["name"],
            "latitud": ciudad_info["latitude"],
            "longitud": ciudad_info["longitude"]
        }

    except requests.exceptions.Timeout:
        print("Error: La solicitud tardó demasiado.")
        return None

    except requests.exceptions.ConnectionError:
        print("Error: Problema de conexión a internet.")
        return None

    except requests.exceptions.RequestException as error:
        print(f"Error en la API: {error}")
        return None


# ------------------------------------------
# Función para obtener el clima
# ------------------------------------------
def obtener_clima(latitud, longitud):
    """
    Consulta el clima actual usando coordenadas.
    """

    parametros = {
        "latitude": latitud,
        "longitude": longitud,
        "current_weather": True
    }

    try:
        respuesta = requests.get(
            WEATHER_URL,
            params=parametros,
            timeout=TIMEOUT
        )

        # Verifica si la respuesta fue correcta
        respuesta.raise_for_status()

        datos = respuesta.json()

        # Verifica si existe información del clima
        if "current_weather" not in datos:
            print("Error: No se pudo obtener el clima.")
            return None

        clima_actual = datos["current_weather"]

        return {
            "temperatura": clima_actual["temperature"],
            "codigo_clima": clima_actual["weathercode"]
        }

    except requests.exceptions.Timeout:
        print("Error: La solicitud tardó demasiado.")
        return None

    except requests.exceptions.ConnectionError:
        print("Error: Problema de conexión a internet.")
        return None

    except requests.exceptions.RequestException as error:
        print(f"Error en la API: {error}")
        return None


# ------------------------------------------
# Función principal
# ------------------------------------------
def mostrar_reporte_clima(ciudad):
    """
    Muestra el reporte del clima en consola.
    """

    # Validar que la ciudad no esté vacía
    if not ciudad or ciudad.strip() == "":
        print("Error: Debes ingresar una ciudad válida.")
        return

    # Obtener coordenadas
    coordenadas = obtener_coordenadas(ciudad)

    # Si ocurrió un error, detener el programa
    if coordenadas is None:
        return

    # Obtener clima actual
    clima = obtener_clima(
        coordenadas["latitud"],
        coordenadas["longitud"]
    )

    # Si ocurrió un error, detener el programa
    if clima is None:
        return

    # Obtener descripción del clima
    descripcion = obtener_descripcion_clima(
        clima["codigo_clima"]
    )

    # Mostrar reporte en consola
    print("=" * 30)
    print("       REPORTE DE CLIMA")
    print("=" * 30)
    print(f"Ciudad: {coordenadas['nombre']}")
    print(f"Temperatura: {clima['temperatura']} °C")
    print(f"Clima: {descripcion}")
    print("=" * 30)


# ------------------------------------------
# Ejecución del programa
# ------------------------------------------

# Pedir ciudad al usuario
nombre_ciudad = input("Ingresa el nombre de una ciudad: ")

# Mostrar reporte
mostrar_reporte_clima(nombre_ciudad)