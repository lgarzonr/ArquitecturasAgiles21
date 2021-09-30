from flask import Flask
from flask_mysqldb import MySQL
from flask_apscheduler import APScheduler
import requests

app = Flask(__name__)

app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'abcd1234'
app.config['MYSQL_DB'] = 'clinica'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

def send_status():
    monitor_uri = 'http://localhost:5002/reporte_microservicio'
    pload = {'servicio_id':'historiasClinica','estado':'OK', 'descripcion':'servicio OK'}
    r = requests.post(monitor_uri, json = pload)
    print(r.text)

@app.route('/paciente/<int:paciente_id>/historiaclinica')
def historia(paciente_id):
    cur = mysql.connection.cursor()
    cur.execute("""SELECT * 
    FROM clinica.detalle, clinica.paciente
    where clinica.detalle.paciente_id = clinica.paciente.id
    and clinica.paciente.id = %s """, (paciente_id,))
    rv = cur.fetchall()
    return str(rv)


if __name__ == '__main__':
    app.run(debug=True)
