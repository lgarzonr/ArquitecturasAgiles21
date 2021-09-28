from flask import request
from ..modelos import db, Servicio, ServicioSchema
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError
from kafka import KafkaProducer
import json

producer = KafkaProducer(
    bootstrap_servers='example.com',
    security_protocol = 'SASL_SSL',
    sasl_mechanism = 'PLAIN',
    sasl_plain_username = 'user',
    sasl_plain_password = 'pass',
    value_serializer=lambda v: json.dumps(v).encode('utf-8'))

servicio_schema = ServicioSchema()

class VistaPacienteServicio(Resource):
    def post(self, id_paciente):
        nuevo_servicio = Servicio(
                tipo=request.json["tipo"],
                descripcion=request.json["descripcion"],
                paciente_id=id_paciente,
                precio=request.json["descripcion"]
                )

        db.session.add(nuevo_servicio)
        db.session.commit()

        dump_schema = servicio_schema.dump(nuevo_servicio)

        producer.send('ac-historiasclinicas', dump_schema)
        producer.send('ac-cuentas', dump_schema)
        producer.flush()
        
        return dump_schema
