from flask import Flask, request, jsonify
import mysql.connector

app = Flask(__name__)

db = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    port=3306,
    password="",
    database="veggie_db"
)

cursor = db.cursor()


@app.route('/users', methods=['GET', 'POST', 'PUT'])
def handle_data():
    if request.method == 'GET':
        cursor.execute("SELECT * FROM user")
        result = cursor.fetchall()
        data = []
        for row in result:
            data.append({
                'id_pengguna': row[0],
                'username': row[1],
                'password': row[2],
            })
        return jsonify(data)

    elif request.method == 'POST':
        if request.headers['Content-Type'] != 'application/json':
            return jsonify({'error': 'Unsupported Media Type'}), 415

        new_data = request.json
        query = "INSERT INTO user (username, password) VALUES (%s, %s)"
        values = (new_data['username'], new_data['password'])
        cursor.execute(query, values)
        db.commit()
        return jsonify({'message': 'Data berhasil ditambahkan'})

    elif request.method == 'PUT':
        if request.headers['Content-Type'] != 'application/json':
            return jsonify({'error': 'Unsupported Media Type'}), 415

        update_data = request.json
        if 'username' in update_data and 'email' not in update_data:
            query = "UPDATE user SET password = %s WHERE username = %s"
            values = (update_data['password'], update_data['username'])
            cursor.execute(query, values)
            if cursor.rowcount == 0:
                return jsonify({'error': 'Username tidak ditemukan'}), 404
        else:
            return jsonify({'error': 'Harap berikan username yang sudah terdaftar'}), 400

        db.commit()
        return jsonify({'message': 'Data berhasil diperbarui'})


@app.route('/login', methods=['POST'])
def user_login():
    if request.headers['Content-Type'] != 'application/json':
        return jsonify({'error': 'Unsupported Media Type'}), 415

    login_data = request.json
    username = login_data['username']
    password = login_data['password']

    cursor.execute("SELECT * FROM user WHERE username = %s AND password = %s", (username, password))
    result = cursor.fetchone()

    if result:
        return jsonify({'message': 'Login berhasil'})
    else:
        return jsonify({'error': 'Username atau password salah'}), 401

@app.route('/admin', methods=['POST'])
def login_admin():
    if request.headers['Content-Type'] != 'application/json':
        return jsonify({'error': 'Unsupported Media Type'}), 415

    login_data = request.json
    username = login_data['username']
    password = login_data['password']

    cursor.execute("SELECT * FROM admin WHERE username = %s AND password = %s", (username, password))
    result = cursor.fetchone()

    if result:
        return jsonify({'message': 'Login berhasil'})
    else:
        return jsonify({'error': 'Username atau password salah'}), 401


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3935)
