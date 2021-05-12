from flask import Flask, render_template
from datetime import date
from lorem_text import lorem
import random

app = Flask(__name__)

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
    with open("wpm.txt", "r") as f:
        record = f.read()
    return render_template("index.html", phrase=phrase, phrase_text=phrase_text, year=year, record=record)

@app.route("/wpm/<int:wpm>")
def wpm(wpm):
    with open("wpm.txt", "r") as f:
        recorded = int(f.read())
    if wpm > recorded:
        with open("wpm.txt", "w") as f:
            f.write(str(wpm))
    return "OK"

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")