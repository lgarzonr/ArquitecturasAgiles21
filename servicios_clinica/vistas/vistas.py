from flask import request
from ..modelos import db, Servicio, ServicioSchema
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError
from kafka import KafkaProducer
import json

producer = KafkaProducer(bootstrap_servers='localhost:9092', value_serializer=lambda v: json.dumps(v).encode('utf-8'))

servicio_schema = ServicioSchema()

class VistaPacienteServicio(Resource):
    def post(self, id_paciente):
        nuevo_servicio = Servicio(
                tipo=request.json["tipo"],
                descripcion=request.json["descripcion"],
                paciente_id=id_paciente
                )

        db.session.add(nuevo_servicio)
        db.session.commit()

        dump_schema = servicio_schema.dump(nuevo_servicio)

        producer.send('actualizador-hc', dump_schema)
        return dump_schema


