import snap7

def leer_datos_plc(ip, rack, slot, db_number, start, size):
    """
    Conecta al PLC y lee datos del bloque de datos especificado.
    """
    try:
        plc = snap7.client.Client()
        plc.connect(ip, rack, slot)
        datos = plc.db_read(db_number, start, size)
        plc.disconnect()
        
        # Devuelve un diccionario con los valores leídos
        return {
            "seft0": snap7.util.get_int(datos, 0),
            "seft2": snap7.util.get_int(datos, 2),
            "seft4": snap7.util.get_int(datos, 4),
            # Puedes agregar más valores si es necesario
        }
    except Exception as e:
        return {"error": str(e)}