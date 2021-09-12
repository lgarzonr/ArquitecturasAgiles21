from flask import (request,)
from monitor.modelos.modelos import EstadoServicio, EstadoServicioSchema
from flask_restful import Resource
from ..modelos import (db, EstadoServicio, EstadoServicioSchema)
from sqlalchemy import desc

estadoServicioSchema = EstadoServicioSchema()

class VistaHeartBeat(Resource):
    def post(self):
        nuevo_registro = EstadoServicio(
            servicio_id = request.json["servicio_id"],
            estado = request.json["estado"],
            descripcion = request.json["descripcion"]
        )
        db.session.add(nuevo_registro)
        db.session.commit()
        return estadoServicioSchema.dump(nuevo_registro)

    def get(self):
        return [estadoServicioSchema.dump(es) for es in EstadoServicio.query.order_by(desc(EstadoServicio.id)).all()]
