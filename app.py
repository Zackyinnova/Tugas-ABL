import mysql.connector

from flask import session
from flask import Flask, render_template, request, redirect, url_for, jsonify, flash

from werkzeug.security import generate_password_hash, check_password_hash


app = Flask (__name__)

app.secret_key = 'rahasia123' 

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="db_absensi"
)

cursor = db.cursor(dictionary=True)

@app.route('/')
def index():
    return render_template(
        "index.html"
    )

#Untuk render Template / page login mahasiswa
@app.route('/login_mahasiswa')
def render_login_mahasiswa():
    
    return render_template(
        "Login_Pages/LoginPage_mhs.html"
    )


@app.route('/login-dosen')
def halaman_login_dosen():

    return render_template(
        'login_dosen.html'
    )

@app.route('/dashboard_mahasiswa')
def render_dashboard_mahasiswa():
    
    return render_template(
        "Dashboard_Pages/Dashbord_mahasiswa.html"
    )

#untuk render Template page login dosen



# ============================ Bagian API ====================

# API untuk input / login mahasiswa
@app.route('/api/mahasiswa/login', methods=['POST'])
def login_mahasiswa():

    data = request.get_json()

    nim = data['nim']
    password = data['password']

    sql = """
    SELECT *
    FROM mahasiswa
    WHERE nim=%s
    AND password=%s
    """

    cursor.execute(sql, (nim, password))
    mahasiswa = cursor.fetchone()

    if mahasiswa:

        session['nim'] = mahasiswa['nim']
        session['nama'] = mahasiswa['nama']
        session['role'] = 'mahasiswa'

        return jsonify({
            "status": True,
            "message": "Login berhasil"
        })

    return jsonify({
        "status": False,
        "message": "NIM atau password salah"
    }), 401

# APi untuk input / login dosen 
@app.route('/api/dosen/login', methods=['POST'])
def login_dosen():

    data = request.get_json()

    username = data['username']
    password = data['password']

    sql = """
    SELECT *
    FROM users
    WHERE username=%s
    AND password=%s
    AND role='dosen'
    """

    cursor.execute(sql, (username, password))
    user = cursor.fetchone()

    if user:

        session['user_id'] = user['id']
        session['role'] = 'dosen'
        session['username'] = user['username']

        return jsonify({
            "status": True,
            "message": "Login dosen berhasil"
        })

    return jsonify({
        "status": False,
        "message": "Login gagal"
    }), 401



if __name__ == "__main__":
    app.run(debug=True)