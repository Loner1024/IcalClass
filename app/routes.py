from flask import Flask,render_template,request
from app import app
from app.forms import get_ical

@app.route('/')
@app.route('/index')
def index():
    form = get_ical()
    return render_template('index.html',title='ICalClass',form=form)
