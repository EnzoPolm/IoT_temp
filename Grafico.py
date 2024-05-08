from flask import Flask, render_template, request, jsonify
import pymysql

app = Flask(__name__)

# Configuración de la base de datos
host = "10.93.254.9"
database = "IoT_temp"
username = "iot"
password = "Patata123"

# Función para establecer la conexión a la base de datos
def conectar_base_de_datos():
    return pymysql.connect(host=host, user=username, password=password, database=database)

# Función para obtener las fechas con datos disponibles en la base de datos
def obtener_fechas_disponibles():
    # Establecer conexión a la base de datos
    conn = conectar_base_de_datos()
    cursor = conn.cursor()

    # Consulta SQL para obtener las fechas disponibles
    sql = "SELECT DISTINCT DATE(fecha) FROM mediciones"
    cursor.execute(sql)

    # Recopilar las fechas en una lista
    fechas = [str(fecha[0]) for fecha in cursor.fetchall()]

    # Cerrar conexión
    cursor.close()
    conn.close()

    return fechas

# Función para obtener los datos del gráfico para una fecha específica
def obtener_datos_grafico(fecha):
    # Establecer conexión a la base de datos
    conn = conectar_base_de_datos()
    cursor = conn.cursor()

    # Consulta SQL para obtener los datos del gráfico para la fecha especificada
    sql = "SELECT fecha, temperatura, humedad FROM mediciones WHERE DATE(fecha) = %s"
    cursor.execute(sql, (fecha,))

    # Recopilar los datos en listas separadas
    fechas = []
    temperaturas = []
    humedades = []

    for row in cursor.fetchall():
        fecha, temperatura, humedad = row
        fechas.append(fecha.strftime("%Y-%m-%d %H:%M:%S"))  # Formatear la fecha y hora
        temperaturas.append(temperatura)
        humedades.append(humedad)

    # Cerrar conexión
    cursor.close()
    conn.close()

    return {
        'labels': fechas,
        'temperaturas': temperaturas,
        'humedades': humedades
    }

@app.route('/')
def index():
    # Obtener las fechas con datos disponibles de la base de datos
    fechas_disponibles = obtener_fechas_disponibles()
    return render_template('index.html', fechas_disponibles=fechas_disponibles)

@app.route('/grafico')
def grafico():
    fecha = request.args.get('fecha')
    datos_grafico = obtener_datos_grafico(fecha)
    return jsonify(datos_grafico)

if __name__ == "__main__":
    # Mantener la aplicación en ejecución
    app.run(debug=True)
