from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import date
from lorem_text import lorem
import random

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///typer.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    ip = db.Column(db.String(80), nullable=False)

class HighestRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    wpm = db.Column(db.Integer)

db.create_all()

def convert(phrase):
    html = ""
    id = 0
    for char in phrase:
        html += f"""<span id="{id}">{char}</span>"""
        id += 1
    return html

@app.route("/")
def main():
    phrase_text = lorem.paragraph()
    phrase = convert(phrase_text)
    year = date.today().year
    records = HighestRecord.query.all()
    if len(records) == 0:
        record = 0
        record_maker = None
    else:
        record = int(records[0].wpm)
        record_maker = records[0].name

    ip = request.remote_addr
    user = User.query.filter_by(ip=ip).first()
    if user:
        return render_template("index.html", phrase=phrase, phrase_text=phrase_text, year=year, record=record, record_maker=record_maker, anonymous=False, username=user.name)
    else:
        return render_template("index.html", phrase=phrase, phrase_text=phrase_text, year=year, record=record, record_maker=record_maker, anonymous=True, username=None)

@app.route("/name/<name>")
def create_user(name):
    new_user = User(name=name, ip=request.remote_addr)
    db.session.add(new_user)
    db.session.commit()
    return "OK"

@app.route("/wpm/<int:wpm>")
def wpm(wpm):
    records = HighestRecord.query.all()
    if len(records) == 0:
        new_record = HighestRecord(wpm=wpm, name=User.query.filter_by(ip=request.remote_addr).first().name)
        db.session.add(new_record)
        db.session.commit()
    else:
        record = records[0]
        if wpm > int(record.wpm):
            record.wpm = wpm
            record.name = User.query.filter_by(ip=request.remote_addr).first().name
            db.session.commit()
    return "OK"

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")