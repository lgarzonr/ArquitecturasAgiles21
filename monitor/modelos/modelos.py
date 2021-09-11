from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields
import enum
import datetime

db = SQLAlchemy()

class Estados(enum.Enum):
    OK = 1
    ERROR = 2

class EstadoServicio(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    fecha_registro = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    servicio_id = db.Column(db.Integer)
    estado = db.Column(db.Enum(Estados))
    descripcion = db.Column(db.String(128))

class EnumDiccionario(fields.Field):
    def _serialize(self, value, attr, obj, **kwrgs):
        if value is None:
            return None
        return {"llave": value.name, "valor": value.value}

class EstadoServicioSchema(SQLAlchemyAutoSchema):
    estado = EnumDiccionario(attribute=("estado"))
    class Meta:
        model = EstadoServicio
        include_relationships = True
        load_instance = True