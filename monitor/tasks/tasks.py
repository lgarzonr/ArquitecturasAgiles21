from ..modelos import (db, EstadoServicio)
from datetime import datetime, timedelta

servicios_id_monitoreados=['historiasClinica',]
delta_tiempo_segundos=30

def check_statuses_reported(app_context):
    with app_context:
        for microservicio_id in servicios_id_monitoreados:
            d = (datetime.utcnow() - timedelta(seconds=delta_tiempo_segundos))
            reporte = EstadoServicio.query.filter(EstadoServicio.fecha_registro>d,EstadoServicio.servicio_id==microservicio_id, EstadoServicio.estado != "OFF").limit(1).first()
            if(reporte==None):
                nuevo_registro = EstadoServicio(
                    servicio_id = microservicio_id,
                    estado = "OFF",
                    descripcion = "Microservicio con no se ha comunicado con monitor en los ultimos {0} segundos".format(delta_tiempo_segundos)
                )
                db.session.add(nuevo_registro)
                db.session.commit()
