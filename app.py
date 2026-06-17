import mysql.connector
from flask import session
from flask import Flask, render_template, request, redirect, url_for, jsonify, flash

from werkzeug.security import generate_password_hash, check_password_hash


app = Flask (__name__)

app.secret_key = 'rahasia123' 

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="db_absensi"
    )

@app.route('/')
def index():
    return render_template(
        "index.html"
    )

@app.route('/login_mahasiswa')
def login_mahasiswa():
    
    return render_template(
        "Login_mahasiswa/LoginPage_mhs.html"
    )



if __name__ == "__main__":
    app.run(debug=True)