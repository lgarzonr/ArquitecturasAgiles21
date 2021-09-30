from flask import request
from ..modelos import db, Servicio, ServicioSchema
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError
from kafka import KafkaProducer
import json

producer = KafkaProducer(
    bootstrap_servers='bootstrap_servers',
    security_protocol = 'SASL_SSL',
    sasl_mechanism = 'PLAIN',
    sasl_plain_username = 'sasl_plain_username',
    sasl_plain_password = 'sasl_plain_password',
    value_serializer=lambda v: json.dumps(v).encode('utf-8'))

servicio_schema = ServicioSchema()

class VistaPacienteServicio(Resource):
    def post(self, id_paciente):
        nuevo_servicio = Servicio(
                tipo=request.json["tipo"],
                descripcion=request.json["descripcion"],
                paciente_id=id_paciente,
                precio=request.json["precio"]
                )

        db.session.add(nuevo_servicio)
        db.session.commit()

        dump_schema = servicio_schema.dump(nuevo_servicio)

        historicas_clinicas_schema = dict(dump_schema)
        historicas_clinicas_schema["precio"] = "*****"

        cuentas_schema = dict(dump_schema)
        cuentas_schema["descripcion"] = "***********" 

        producer.send('ac-historiasclinicas', historicas_clinicas_schema)
        producer.send('ac-cuentas', cuentas_schema)
        producer.flush()
        
        return dump_schema