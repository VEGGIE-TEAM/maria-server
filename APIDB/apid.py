from flask import Flask, request, jsonify
import mysql.connector
from werkzeug.utils import secure_filename
import os
from datetime import datetime

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

db = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    port=3306,
    password="",
    database="veggie_db"
)

cursor = db.cursor()


# Fungsi untuk memeriksa ekstensi gambar yang diunggah
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/api/data', methods=['GET', 'POST'])
def handle_data():
    if request.method == 'GET':
        # Implement your GET logic here to retrieve data from the database
        # Use request.args to access query parameters

        return jsonify({'message': 'This is a GET request'})

    elif request.method == 'POST':
        try:
            nama_sayur = request.form.get('nama_sayur')
            nama_pasar = request.form.get('nama_pasar')

            # Look up the 'id_sayur' and 'id_pasar' based on provided names
            cursor.execute("SELECT id_sayur FROM sayur WHERE nama_sayur = %s", (nama_sayur,))
            result_sayur = cursor.fetchone()

            cursor.execute("SELECT id_pasar FROM pasar WHERE nama_pasar = %s", (nama_pasar,))
            result_pasar = cursor.fetchone()

            if result_sayur is None:
                return jsonify({'error': 'Nama sayur not found'}), 404

            if result_pasar is None:
                return jsonify({'error': 'Nama pasar not found'}), 404

            id_sayur = result_sayur[0]
            id_pasar = result_pasar[0]

            gambar_sayur = request.files['gambar_sayur']
            if gambar_sayur and allowed_file(gambar_sayur.filename):
                filename = secure_filename(gambar_sayur.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                gambar_sayur.save(filepath)
            else:
                return jsonify({'error': 'Invalid image file'}), 400

            hasil_deteksi = request.form.get('hasil_deteksi')

            tanggal_input = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            query = "INSERT INTO deteksi (id_sayur, id_pasar, gambar_sayur, tanggal_input, hasil_deteksi) VALUES (%s, %s, %s, %s, %s)"
            values = (id_sayur, id_pasar, filepath, tanggal_input, hasil_deteksi)

            cursor.execute(query, values)
            db.commit()
            return jsonify({'message': 'Data deteksi berhasil ditambahkan'}), 200
        except Exception as e:
            return jsonify({'error': 'Internal Server Error', 'details': str(e)}), 500

if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(host='0.0.0.0', port=3934)
