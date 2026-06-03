# beura of meterorological data and beach conditions

import sqlite3
conn = sqlite3.connect("database.sqlite")
cursor = conn.cursor()
#rcursor.execute("SELECT game_id, COUNT(*) FROM Characters GROUP BY game_id;")
print(cursor.fetchall())

from flask import Flask, render_template
import os
print(os.path.abspath("database.sqlite"))


app=Flask(__name__)

@app.route('/')
def home():
    html = "homepage" # Define html FIRST
    return render_template('homepage.html',body=html)

'''
@app.route('/check conditions')
def games():
    html = "games"
    return render_template('games.html',body=html)

@app.route('/plan activities')
def forsaken():
    html = "forsaken...."
    conn = sqlite3.connect('database.sqlite')
    cursor = conn.cursor()

@app.route('/sun safety')
def forsaken():
    html = "forsaken...."
    conn = sqlite3.connect('database.sqlite')
    cursor = conn.cursor()

@app.route('/pack-your-bag')
def forsaken():
    html = "forsaken...."
    conn = sqlite3.connect('database.sqlite')
    cursor = conn.cursor()
    '''