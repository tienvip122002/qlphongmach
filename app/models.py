from sqlalchemy import Column, Integer, String, Float, ForeignKey, Enum, DateTime
from sqlalchemy.orm import relationship
from app import db, app
from datetime import datetime
from flask_login import UserMixin
import enum


class DonVi(db.Model):
    __tablename__ = 'donvi'

    id = Column(Integer, primary_key=True, autoincrement=True)
    tendonvi = Column(String(50), nullable=False, unique=True)
    thuocs = relationship('Thuoc', backref='donvi', lazy=False)

    def __str__(self):
        return self.name


class PhieuKham(db.Model):
    __tablename__ = 'phieukham'

    id = Column(Integer, primary_key=True, autoincrement=True)
    ngaykham = Column(DateTime, default=datetime.now())
    trieuchung = Column(String(255), nullable=False, unique=True)
    loaibenh = Column(String(50), nullable=False, unique=True)


phieukham_thuoc = db.Table('phieukham_thuoc',
                           Column('phieukham_id', Integer, ForeignKey('phieukham.id'), primary_key=True),
                           Column('thuoc_id', Integer, ForeignKey('thuoc.id'), primary_key=True),
                           Column('soluong', Integer, nullable=False))

class Thuoc(db.Model):
    __tablename__ = 'thuoc'

    id = Column(Integer, primary_key=True, autoincrement=True)
    tenthuoc = Column(String(50), nullable=False, unique=True)
    cachdung = Column(String(255), nullable=False, unique=True)
    gia = Column(Float, default=0)
    donvi_id = Column(Integer, ForeignKey(DonVi.id), nullable=False)

    def __str__(self):
        return self.name





if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        app.run(debug=True)

