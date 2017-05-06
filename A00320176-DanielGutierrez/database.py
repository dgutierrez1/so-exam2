from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from coercing import CoerceUTF8


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/check_user/repositories/parcial2/so-exam2/A00320176-DanielGutierrez/check_persistence.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)
db.text_factory = str

class Check(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cpu = db.Column(CoerceUTF8)
    memory = db.Column(CoerceUTF8)
    disk = db.Column(CoerceUTF8)
    httpd = db.Column(CoerceUTF8)

    def __init__(self, cpu, memory, disk, httpd):
        self.cpu = cpu
        self.memory = memory
        self.disk = disk
        self.httpd = httpd

    def __repr__(self):
        return '<Check %r>' % self.id
