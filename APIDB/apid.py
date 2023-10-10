from flask import Flask, request, jsonify
import mysql.connector
from werkzeug.utils import secure_filename
import os
from datetime import datetime

app = Flask(__name__)

# Pengaturan untuk unggahan gambar
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

db = mysql.connector.connect(
    host="localhost",
    user="root",
    port=3306,
    password="",  # Gantilah dengan password MySQL Anda
    database="Veggie_db"
)

cursor = db.cursor()


@app.route('/api/data', methods=['GET', 'POST'])
def handle_data():
    if request.method == 'GET':
        data_type = request.args.get('type')
        if data_type == 'sayur':
            cursor.execute("SELECT * FROM sayur")
        elif data_type == 'pasar':
            cursor.execute("SELECT * FROM pasar")
        elif data_type == 'deteksi':
            cursor.execute("SELECT * FROM deteksi")
        else:
            return jsonify({'error': 'Invalid data type'}), 400

        result = cursor.fetchall()
        data = []
        for row in result:
            if data_type == 'sayur':
                data.append({
                    'id_sayur': row[0],
                    'nama_sayur': row[1],
                    'gambar_sayur': row[2],
                    'tanggal_input': row[3],
                })
            elif data_type == 'pasar':
                data.append({
                    'id_pasar': row[0],
                    'nama_pasar': row[1],
                })
            elif data_type == 'deteksi':
                data.append({
                    'id_deteksi': row[0],
                    'id_sayur': row[1],
                    'id_pasar': row[2],
                    'hasil_deteksi': row[3],
                })

        return jsonify(data)

    elif request.method == 'POST':
        try:
            data_type = request.form.get('type')
            if data_type == 'sayur':
                if 'nama_sayur' in request.form and 'tanggal_input' in request.form and 'gambar_sayur' in request.files:
                    # Pengolahan gambar
                    uploaded_file = request.files['gambar_sayur']
                    if uploaded_file and allowed_file(uploaded_file.filename):
                        filename = secure_filename(uploaded_file.filename)
                        filepath = os.path.join(
                            app.config['UPLOAD_FOLDER'], filename)
                        uploaded_file.save(filepath)
                    else:
                        return jsonify({'error': 'Invalid image file'}), 400

                    # Pengolahan tanggal dan waktu
                    tanggal_input = request.form.get('tanggal_input')
                    try:
                        tanggal_input = datetime.strptime(
                            tanggal_input, '%Y-%m-%d %H:%M:%S')
                    except ValueError:
                        return jsonify({'error': 'Invalid date & time format'}), 400

                    query = "INSERT INTO sayur (nama_sayur, gambar_sayur, tanggal_input) VALUES (%s, %s, %s)"
                    values = (request.form.get('nama_sayur'),
                              filepath, tanggal_input)
                else:
                    return jsonify({'error': 'Invalid form data'}), 400
            elif data_type == 'pasar':
                if 'nama_pasar' in request.form:
                    query = "INSERT INTO pasar (nama_pasar) VALUES (%s)"
                    values = (request.form.get('nama_pasar'),)
                else:
                    return jsonify({'error': 'Invalid form data'}), 400
            elif data_type == 'deteksi':
                if 'id_sayur' in request.form and 'id_pasar' in request.form and 'hasil_deteksi' in request.form:
                    query = "INSERT INTO deteksi (id_sayur, id_pasar, hasil_deteksi) VALUES (%s, %s, %s)"
                    values = (request.form.get('id_sayur'), request.form.get(
                        'id_pasar'), request.form.get('hasil_deteksi'))
                else:
                    return jsonify({'error': 'Invalid form data'}), 400
            else:
                return jsonify({'error': 'Invalid form data type'}), 400

            cursor.execute(query, values)
            db.commit()
            return jsonify({'message': f'Data {data_type} berhasil ditambahkan'}), 201
        except Exception as e:
            return jsonify({'error': 'Internal Server Error', 'details': str(e)}), 500

# Fungsi untuk memeriksa ekstensi gambar yang diunggah


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(host='0.0.0.0', port=3934)
