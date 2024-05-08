import adafruit_dht
import board
import time
import requests
import mysql.connector
from mysql.connector import Error

# Definir el pin GPIO
pin = board.D4

# Iniciar el sensor
sensor = adafruit_dht.DHT11(pin)

# Token de acceso al bot de Telegram y chat ID
TELEGRAM_BOT_TOKEN = '7081480305:AAFc6R0lm9-mh_tw2JC9wTdR4XzAt6HIqco'
CHAT_ID = '2033814630'

# Configuración de la conexión a la base de datos MySQL
try:
    connection = mysql.connector.connect(host='10.93.254.9',
                                         database='IoT_temp',
                                         user='iot',
                                         password='Patata123')
    if connection.is_connected():
        db_Info = connection.get_server_info()
        print("Conectado a MySQL Server versión ", db_Info)
        cursor = connection.cursor()
        cursor.execute("select database();")
        record = cursor.fetchone()
        print("Conectado a la base de datos: ", record)
except Error as e:
    print("Error al conectar a la base de datos MySQL:", e)

def guardar_en_bd(fecha, temperatura, humedad):
    try:
        cursor.execute("INSERT INTO mediciones (fecha, temperatura, humedad) VALUES (%s, %s, %s)", (fecha, temperatura, humedad))
        connection.commit()
        print("Datos guardados en la base de datos.")
    except Error as e:
        print("Error al guardar datos en la base de datos MySQL:", e)

def enviar_mensaje_telegram(mensaje):
    url = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage'
    datos = {'chat_id': CHAT_ID, 'text': mensaje}
    response = requests.post(url, data=datos)
    if response.status_code != 200:
        print("Error al enviar el mensaje a Telegram:", response.status_code)

def verificar_rangos(temperatura, humedad):
    mensaje = ""
    if temperatura < 20 or temperatura > 25:
        mensaje += f"⚠ Temperatura fuera de rango ({temperatura}°C)⚠ \n"
    if humedad < 40 or humedad > 55:
        mensaje += f"⚠ Humedad fuera de rango ({humedad}%)⚠ \n"
    if mensaje:
       enviar_mensaje_telegram(mensaje)

ultimo_tiempo_insercion = 0
duracion_entre_inserciones = 300  # 5 minutos

try:
    while True:
        try:
            # Leer la temperatura y la humedad desde el sensor
            temperature_c = sensor.temperature
            humidity = sensor.humidity
            # Mostrar los valores en la consola
            print("Temperatura={0:0.1f}°C, Humedad={1:0.1f}%".format(temperature_c, humidity))
            # Verificar si los valores están fuera de rango y enviar mensaje si es necesario
            verificar_rangos(temperature_c, humidity)

            # Obtener el tiempo actual
            tiempo_actual = time.time()

            # Verificar si han pasado 5 minutos desde la última inserción
            if tiempo_actual - ultimo_tiempo_insercion >= duracion_entre_inserciones:
                # Guardar los datos en la base de datos
                fecha_actual = time.strftime('%Y-%m-%d %H:%M:%S')
                guardar_en_bd(fecha_actual, temperature_c, humidity)
                # Actualizar el tiempo de la última inserción
                ultimo_tiempo_insercion = tiempo_actual
        except RuntimeError as e:
            # Manejar errores de lectura del sensor
            print("Error al leer datos del sensor:", e)

        # Esperar un tiempo antes de realizar la próxima lectura
        time.sleep(10)

except KeyboardInterrupt:
    # Manejo de la interrupción por teclado (CTRL+C)
    print("Programa terminado por el usuario.")
except Exception as e:
    # Manejo de cualquier otro tipo de excepción
    print("Se produjo un error:", e)
finally:
    # Liberar recursos del sensor
    sensor.exit()
    # Cerrar la conexión a la base de datos
    if connection.is_connected():
        cursor.close()
        connection.close()
        print("Conexión a MySQL cerrada.")
