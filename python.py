
import html
import sqlite3
conn = sqlite3.connect("database.sqlite")
cursor = conn.cursor()
#cursor.execute("SELECT game_id, COUNT(*) FROM Characters GROUP BY game_id;")
print(cursor.fetchall())

from flask import Flask, render_template, abort
from jinja2 import TemplateNotFound
import os
print(os.path.abspath("database.sqlite"))


app=Flask(__name__)
@app.route("/")
def home():
    return render_template("homepage.html", body=html)

@app.route("/northenbeaches")
def northenbeaches():
    return render_template("northenbeaches.html", body=html) 


@app.route("/northenbeaches/<beach>")
def beach_page(beach):
    template_path = f"N-beaches_templates/{beach}.html"
    try:
        return render_template(template_path, body=html)
    except TemplateNotFound:
        abort(404)
        # added a coment to test the commit functionality of git


app.run(ssl_context=('localhost.crt', 'localhost.key'), port=443, host="0.0.0.0") 