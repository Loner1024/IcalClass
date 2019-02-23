from flask import render_template, request, flash, redirect, url_for
from app import app
from app.forms import get_ical
from app.get_class import GetIcal
import time

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    form = get_ical()
    if form.validate_on_submit():
        # flash('success!')
        x = GetIcal(form.student_id.data)
        class_data = x.get_class()
        x.out_ical(class_data)
        time.sleep( 5 )
        return redirect(form.student_id.data+'.ics')
        # return redirect(url_for('index'))
    return render_template('index.html',title='ICalClass',form=form)

@app.route('/help')
def help_page():
    return render_template('help.html')

@app.route('/about')
def about_page():
    return render_template('about.html')

# 20171016087
'''
@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    form = get_ical()
    if form.validate_on_submit():
        flash('Login requested for user {}'.format(form.student_id.data))
        return redirect(url_for('index'))
    return render_template('index.html', form=form)
    '''