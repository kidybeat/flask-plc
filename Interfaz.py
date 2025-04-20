from flask import Flask, jsonify, render_template_string
from s71200Snap7 import leer_datos_plc
import threading
import time

app = Flask(__name__)

# Variables globales para almacenar los datos del PLC
datos_plc = {"DBdata1": "Cargando...", "DBdata2": "Cargando...", "DBdata3": "Cargando..."}

# Función para actualizar los datos del PLC periódicamente
def actualizar_datos():
    global datos_plc
    while True:
        datos = leer_datos_plc("192.168.1.4", 0, 1, 1, 0, 10)
        if "error" in datos:
            datos_plc = {"DBdata1": f"Error: {datos['error']}", "DBdata2": "", "DBdata3": ""}
        else:
            datos_plc = {
                "DBdata1": datos["seft0"],
                "DBdata2": datos["seft2"],
                "DBdata3": datos["seft4"],
            }
        time.sleep(1)  # Actualizar cada segundo

# Ruta para mostrar los datos en la raíz
@app.route('/')
def home():
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Interfaz PLC</title>
        <meta http-equiv="refresh" content="1"> <!-- Refrescar la página cada segundo -->
    </head>
    <body>
        <h1>Interfaz de usuario para leer datos de un PLC S7-1200</h1>
        <p>DBdata1: {{ DBdata1 }}</p>
        <p>DBdata2: {{ DBdata2 }}</p>
        <p>DBdata3: {{ DBdata3 }}</p>
    </body>
    </html>
    """
    return render_template_string(html, DBdata1=datos_plc["DBdata1"], DBdata2=datos_plc["DBdata2"], DBdata3=datos_plc["DBdata3"])

# Ruta para obtener los datos del PLC en formato JSON
@app.route('/api/datos', methods=['GET'])
def obtener_datos():
    return jsonify(datos_plc)

# Iniciar el hilo para actualizar los datos del PLC
if __name__ == '__main__':
    threading.Thread(target=actualizar_datos, daemon=True).start()
    app.run(host='0.0.0.0', port=5000, debug=True)