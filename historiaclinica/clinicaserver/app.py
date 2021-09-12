from flask import Flask
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'admin'
app.config['MYSQL_DB'] = 'clinica'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

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