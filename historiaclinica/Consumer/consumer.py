from kafka import KafkaConsumer
import mysql.connector
from json import loads
import json

def insert_varibles_into_table(id, fecha_registro, descripcion, tipo, paciente_id):
    try:
        connection = mysql.connector.connect(host='localhost',
                                             database='clinica',
                                             user='root',
                                             password='abcd1234')
        cursor = connection.cursor()
        mySql_insert_query = """INSERT INTO detalle (fecha_registro, descripcion, tipo, paciente_id) 
                                VALUES (%s, %s, %s, %s) """

        record = (fecha_registro, descripcion, tipo, paciente_id)
        cursor.execute(mySql_insert_query, record)
        connection.commit()
        print("Record inserted successfully ")

    except mysql.connector.Error as error:
        print("Failed to insert into MySQL table {}".format(error))

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")

consumer = KafkaConsumer('ac-historiasclinicas',
                         bootstrap_servers= 'example.com',
                         security_protocol = 'SASL_SSL',
                         sasl_mechanism = 'PLAIN',
                         sasl_plain_username = 'user',
                         sasl_plain_password = 'pass',
                         value_deserializer=lambda x: loads(x.decode('utf-8'))
                         )

for msg in consumer:
    msg = msg.value
    print(msg)
    id = (msg['id'])
    fecha_registro = msg['fecha_registro']
    descripcion = msg['descripcion']
    tipo = (msg['tipo'])
    paciente_id = msg['paciente_id']
    insert_varibles_into_table(id, fecha_registro, descripcion, json.dumps(tipo), paciente_id)
