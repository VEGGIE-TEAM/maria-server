from flask import Flask, request, jsonify
import mysql.connector
import json

app = Flask(__name__)

db = mysql.connector.connect(
    host="localhost",
    user="root",
    port=3306,
    password="",
    database="siswa"
)

cursor = db.cursor()


@app.route('/api/data', methods=['GET', 'POST'])
def handle_data():
    if request.method == 'GET':
        cursor.execute("SELECT * FROM sayur")
        result = cursor.fetchall()
        data = []
        for row in result:
            data.append({
                'id_sayur': row[0],
                'nama_sayur': row[1],
                'lokasi': row[2],
            })
        return jsonify(data)

    elif request.method == 'POST':
        try:
            if request.is_json:
                new_data = request.get_json()
                if 'nama_sayur' in new_data and 'lokasi' in new_data:
                    query = "INSERT INTO sayur (nama_sayur, lokasi) VALUES (%s, %s)"
                    values = (new_data['nama_sayur'], new_data['lokasi'])
                    cursor.execute(query, values)
                    db.commit()
                    return jsonify({'message': 'Data berhasil ditambahkan'}), 201
                else:
                    return jsonify({'error': 'Invalid JSON data'}), 400
            else:
                nama_sayur = request.form.get('nama_sayur')
                lokasi = request.form.get('lokasi')
                if nama_sayur is not None and lokasi is not None:
                    query = "INSERT INTO sayur (nama_sayur, lokasi) VALUES (%s, %s)"
                    values = (nama_sayur, lokasi)
                    cursor.execute(query, values)
                    db.commit()
                    return jsonify({'message': 'Data berhasil ditambahkan'}), 201
                else:
                    return jsonify({'error': 'Data tidak valid'}), 400
        except Exception as e:
            return jsonify({'error': 'Internal Server Error', 'details': str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3934)
