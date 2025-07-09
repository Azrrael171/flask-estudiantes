from flask import Flask, jsonify, Response
import sqlite3
import json

app = Flask(__name__)

# Función para obtener los alumnos desde la base de datos SQLite
def obtener_alumnos():
    conn = sqlite3.connect('alumnos.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM alumnos")
    rows = cur.fetchall()
    conn.close()

    alumnos = []
    for row in rows:
        alumnos.append({
            'id': row[0],
            'nombre': row[1],
            'apellido': row[2],
            'aprobado': bool(row[3]),
            'nota': row[4],
            'fecha': row[5]
        })
    return alumnos

# Página de inicio
@app.route('/')
def inicio():
    return '''
    <h2>Bienvenido a la API de Alumnos</h2>
    <p>Usa los siguientes endpoints:</p>
    <ul>
        <li><a href="/alumnos">/alumnos</a> : desde SQLite</li>
        <li><a href="/alumnos_mongo">/alumnos_mongo</a> : desde estudiante.json (simula MongoDB)</li>
    </ul>
    '''

# Endpoint con datos desde SQLite
@app.route('/alumnos', methods=['GET'])
def listar_alumnos():
    datos = obtener_alumnos()
    json_data = json.dumps(datos, ensure_ascii=False, indent=2)
    return Response(json_data, content_type='application/json; charset=utf-8')

# Endpoint con datos desde estudiante.json (simulando MongoDB)
@app.route('/alumnos_mongo', methods=['GET'])
def alumnos_mongo():
    with open('estudiante.json', 'r', encoding='utf-8') as archivo:
        datos = json.load(archivo)
        # Limpiar el campo "_id" de MongoDB
        for alumno in datos:
            if '_id' in alumno:
                alumno.pop('_id')
    json_data = json.dumps(datos, ensure_ascii=False, indent=2)
    return Response(json_data, content_type='application/json; charset=utf-8')

if __name__ == '__main__':
    app.run(debug=True)
