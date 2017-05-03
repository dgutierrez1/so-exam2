from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)


class Check(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cpu = db.Column(db.String(100), unique=True)
    memory = db.Column(db.String(100), unique=True)
    disk = db.Column(db.String(100), unique = True)
    service = db.Column(db.String(100), unique = True)

    def __init__(self, cpu, memory, disk, service):
        self.cpu = cpu
        self.memory = memory
        self.disk = disk
        service = service

    def __repr__(self):
        return '<Check %r>' % self.id
