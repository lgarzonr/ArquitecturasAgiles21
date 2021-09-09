from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields
import enum
import datetime

db = SQLAlchemy()

class TipoServicio(enum.Enum):
    LABORATORIO = 1
    CONSULTA = 2
    FARMACIA = 3
    CIRUGIA = 3

class EnumADiccionario(fields.Field):
    def _serialize(self, value, attr, obj, **kwargs):
        if value is None:
            return None
        return {"llave": value.name, "valor": value.value}

class Servicio(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    tipo = db.Column(db.Enum(TipoServicio))
    fecha_registro = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    descripcion = db.Column(db.String(128))
    paciente_id = db.Column(db.Integer)

class ServicioSchema(SQLAlchemyAutoSchema):
    tipo = EnumADiccionario(attribute=("tipo"))
    class Meta:
         model = Servicio
         include_relationships = True
         load_instance = True
