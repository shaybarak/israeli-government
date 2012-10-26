from model import Archive
from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('howmany.html', how_many = len(Archive.latest().members))
