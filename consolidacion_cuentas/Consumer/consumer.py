from kafka import KafkaConsumer
from json import loads
import json
import datetime
import sqlite3


def registrar_cuenta(pDescripcion, pTipo, pPaciente_id, pPrecio):
    try:
        conexion=sqlite3.connect("..\cuentas_db.db")        
        conexion.execute("INSERT INTO cuenta (precio, descripcion, tipo, paciente_id, fecha_registro) VALUES (?,?,?,?,?)", (pPrecio, pDescripcion, pTipo, pPaciente_id, datetime.datetime.now()))
        conexion.commit()    
        print("Record inserted successfully ")
    except sqlite3.Error as err:
        print("Ocurrió un error: ", err.args[0])
    finally:
        if(conexion):
            conexion.close()
            print("Se cerró la conexión a BD")


consumer = KafkaConsumer('ac-cuentas',
                         bootstrap_servers= 'bootstrap_servers',
                         security_protocol = 'SASL_SSL',
                         sasl_mechanism = 'PLAIN',
                         sasl_plain_username = 'sasl_plain_username',
                         sasl_plain_password = 'sasl_plain_password',
                         value_deserializer=lambda x: loads(x.decode('utf-8'))
                         )

for msg in consumer:
    msg = msg.value
    print("msg: ", msg)
    precio = msg['precio']
    descripcion = msg['descripcion']
    tipo = (msg['tipo'])
    paciente_id = msg['paciente_id']
    registrar_cuenta(descripcion, json.dumps(tipo), paciente_id, precio)