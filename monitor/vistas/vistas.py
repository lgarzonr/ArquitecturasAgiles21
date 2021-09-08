from flask_restful import Resource

class VistaHeartBeat(Resource):
    def post(self):
        print('guardar estado recibido por microservicio')
        return 200

    def get(self):
        print('get log de monitor')
        return 200