import datetime
from flask import request
from ..modelos import db, Cuenta, CuentaSchema
from flask_restful import Resource

cuenta_schema = CuentaSchema()

class VistaCuentas(Resource):
    def get(self):
        return [cuenta_schema.dump(cuenta) for cuenta in Cuenta.query.all()]

    def post(self):
        C = Cuenta(descripcion = request.json['descripcion'],\
                   precio = request.json['precio'],\
                    tipo = request.json['tipo'],
                    paciente_id = 1,
                    fecha_registro = datetime.datetime.now()
                    )
        db.session.add(C)
        db.session.commit()
        return cuenta_schema.dump(C)
