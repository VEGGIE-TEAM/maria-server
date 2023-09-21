import json
import sqlite3


class VeggieDettectBackend:
    def __init__(data):
        data.conn = sqlite3.connect("cobaServer.db")
        data.cursor = data.conn.cursor()
        data.create_tables()  # Panggil fungsi ini untuk membuat tabel jika belum ada

    def create_tables(data):
        with open(
            "database.sql", "r"
        ) as sql_file:  # Pastikan nama file dan pathnya sesuai
            sql_script = sql_file.read()
        data.cursor.executescript(sql_script)
        data.conn.commit()  # Simpan perubahan ke database

    def simpan_sayur(data, nama_sayur, gambar_sayur, tanggal_input):
        try:
            data.cursor.execute(
                "INSERT INTO Sayur (nama_sayur, gambar_sayur,tanggal_input) VALUES (?, ?, ?)",
                (nama_sayur, gambar_sayur, tanggal_input),
            )
            data.conn.commit()  # Simpan perubahan ke database
            return True
        except Exception as e:
            print("Error:", str(e))
            return False

    def simpan_pasar(data, nama_pasar):
        try:
            data.cursor.execute(
                "INSERT INTO pasar (nama_pasar) VALUES (?)",
                (nama_pasar),
            )
            data.conn.commit()  # Simpan perubahan ke database
            return True
        except Exception as e:
            print("Error:", str(e))
            return False

    def simpan_deteksi(data, id_sayur, id_pasar, hasil_deteksi):
        try:
            data.cursor.execute(
                "INSERT INTO deteksi (id_sayur ,id_pasar , hasil_deteksi) VALUES (?, ?, ?)",
                (id_sayur, id_pasar, hasil_deteksi),
            )
            data.conn.commit()  # Simpan perubahan ke database
            return True
        except Exception as e:
            print("Error saat menyimpan deteksi:", str(e))
            return False
