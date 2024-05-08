# Proyecto de Monitorización de temperatura y humedad de un CPD

Este proyecto tiene como objetivo recopilar y procesar datos de temperatura y humedad utilizando un sensor DHT11 conectado a una placa Raspberry Pi. A continuación, se describen las etapas principales del proceso:

1. **Recopilación de Datos:** Utilizando el sensor DHT11, se lee la temperatura y la humedad del entorno.
2. **Envío de Mensajes a Telegram:** Se verifica si los valores de temperatura y humedad están fuera de ciertos rangos establecidos y se envía un mensaje a través de Telegram si es necesario.
3. **Guardado de Datos en la Base de Datos:** Se establece una conexión a una base de datos MySQL donde se almacenarán los datos recopilados y se implementa una función para guardar la fecha, temperatura y humedad.
4. **Visualización del Gráfico en una Página Web:** Se utiliza Flask para crear una aplicación web local donde se muestra un gráfico interactivo con los datos recopilados.

