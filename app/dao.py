from sqlalchemy.dialects import mysql

from app.models import Medicine, User, MedicineUnit
from flask import Flask, render_template, request, redirect, url_for, flash
from app import app, db
import hashlib
from flask_login import current_user

def get_medicine():
    return Medicine.query.all()

def insert_medicine():
    if request.method == "POST":
        flash("Data Inserted Successfully")
        medicine_name = request.form['medicine_name']
        how_to_use = request.form['how_to_use']
        # soluong = request.form['soluong']
        unit_name = request.form['unit_name']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO medicine (medicine_name, how_to_use, unit_name) VALUES (%s, %s, %s, %s)", (medicine_name, how_to_use, unit_name))
        mysql.connection.commit()


# đơn vị thuốc
def get_medicineunit():
    return MedicineUnit.query.all()


# login
def add_user(name, username, password):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    u = User(name=name, username=username, password=password)

    db.session.add(u)
    db.session.commit()


def auth_user(username, password):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())

    return User.query.filter(User.username.__eq__(username.strip()),
                             User.password.__eq__(password)).first()

def get_user_by_id(user_id):
    return User.query.get(user_id)