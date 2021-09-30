from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields
import enum
import datetime

db = SQLAlchemy()

class Cuenta(db.Model):
    numDetalle = db.Column(db.Integer, primary_key = True, autoincrement=True)   
    tipo = db.Column(db.String(128))
    fecha_registro = db.Column(db.DateTime)
    descripcion = db.Column(db.String(128))
    paciente_id = db.Column(db.Integer)
    precio = db.Column(db.Integer)

class CuentaSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Cuenta
        include_relationships = True
        load_instance = True

    