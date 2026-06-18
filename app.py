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

#Untuk render Template / page  mahasiswa
@app.route('/login_mahasiswa')
def render_login_mahasiswa():
    
    return render_template(
        "Login_Pages/LoginPage_mhs.html"
    )


@app.route('/dashboard_mahasiswa')
def render_dashboard_mahasiswa():
    
    return render_template(
        "Dashboard_Mhs/Dashbord_mahasiswa.html"
    )

#Untuk render Template / page  Dosen
@app.route('/login_dosen')
def halaman_login_dosen():

    return render_template(
        'Login_Pages/LoginPage_dsn.html'
    )


@app.route('/dashboard_dosen')
def dashboard_dosen():

    if session.get('role') != 'dosen':
        return redirect('/login-dosen')

    return render_template(
        'Dashboard_dsn/Dashboard_dsn.html'
    )

@app.route('/profil_dosen')
def profil_dosen():

    if session.get('role') != 'dosen':
        return redirect('/login-dosen')

    return render_template(
        'Dashboard_dsn/Profil_dsn.html'
    )





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










# =============================== Bagian API Keperluan Data dosen ========================
# APi untuk input / login dosen 
@app.route('/api/dosen/login', methods=['POST'])
def login_dosen():

    data = request.get_json()

    nidn = data['nidn']
    password = data['password']

    sql = """
    SELECT *
    FROM dosen
    WHERE nidn=%s
    AND password=%s
    """

    cursor.execute(sql, (nidn, password))
    dosen = cursor.fetchone()

    if dosen:

        session['nidn'] = dosen['nidn']
        session['nama'] = dosen['nama']
        session['role'] = 'dosen'

        return jsonify({
            "status": True,
            "message": "Login dosen berhasil",
            "nama": dosen['nama']
        })

    return jsonify({
        "status": False,
        "message": "NIDN atau password salah"
    }), 401

#session data dosen
@app.route('/api/dosen/session')
def dosen_session():

    if session.get('role') != 'dosen':
        return jsonify({
            "status": False,
            "message": "Belum login"
        }), 401

    return jsonify({
        "status": True,
        "nidn": session['nidn'],
        "nama": session['nama']
    })


#untuk ambil data dosen
@app.route('/api/dosen/profile', methods=['GET'])
def profile_dosen():

    if session.get('role') != 'dosen':
        return jsonify({
            "status": False,
            "message": "Belum login"
        }), 401

    cursor.execute(
        """
        SELECT
            nidn,
            nama,
            fakultas,
            email
        FROM dosen
        WHERE nidn=%s
        """,
        (session['nidn'],)
    )

    dosen = cursor.fetchone()

    return jsonify({
        "status": True,
        "data": dosen
    })

#logout akun dosen
@app.route('/api/logout', methods=['POST'])
def logout():

    session.clear()

    return jsonify({
        "status": True,
        "message": "Logout berhasil"
    })


if __name__ == "__main__":
    app.run(debug=True)