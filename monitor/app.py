from monitor import create_app 
from flask_restful import Api
from flask_apscheduler import APScheduler
from .tasks import check_statuses_reported
from .vistas import VistaHeartBeat

app = create_app('default')
app_context = app.app_context()
app_context.push()

scheduler = APScheduler()
scheduler.add_job(id = 'intervalCheck', func = check_statuses_reported, trigger = 'interval', seconds = 2)
scheduler.start()

api= Api(app)
api.add_resource(VistaHeartBeat, '/report_status')
    