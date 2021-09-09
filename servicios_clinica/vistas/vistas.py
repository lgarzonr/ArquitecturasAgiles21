from flask import request
from ..modelos import db, Servicio, ServicioSchema
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError

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

        return servicio_schema.dump(nuevo_servicio)


