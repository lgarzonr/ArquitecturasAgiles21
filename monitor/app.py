from monitor import create_app 
from flask_restful import Api
from flask_apscheduler import APScheduler
from .tasks import check_statuses_reported
from .vistas import VistaHeartBeat
from .modelos import db, EstadoServicio

app = create_app('default')
app_context = app.app_context()
app_context.push()

scheduler = APScheduler()
scheduler.add_job(id = 'intervalCheck', func = check_statuses_reported, args =(app_context,), trigger = 'interval', seconds = 20)
scheduler.init_app(app)
scheduler.start()

db.init_app(app)
db.create_all()

api= Api(app)
api.add_resource(VistaHeartBeat, '/reporte_microservicio')
    