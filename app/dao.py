from sqlalchemy.dialects import mysql

from app.models import Thuoc
from flask import Flask, render_template, request, redirect, url_for, flash
from app import app

def load_thuocs():
    return Thuoc.query.all()

def insertthuoc():
    if request.method == "POST":
        flash("Data Inserted Successfully")
        tenthuoc = request.form['tenthuoc']
        cachdung = request.form['cachdung']
        soluong = request.form['soluong']
        donvi = request.form['donvi']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO thuoc (tenthuoc, cachdung, soluong, donvi) VALUES (%s, %s, %s, %s)", (tenthuoc, cachdung, soluong, donvi))
        mysql.connection.commit()
