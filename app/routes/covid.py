from app import app, login
import mongoengine.errors
from flask import render_template, flash, redirect, url_for
from flask_login import current_user
from app.classes.data import Covid
from app.classes.forms import CovidForm
from flask_login import login_required
import datetime as dt

@app.route('/covid/new', methods=['GET', 'POST'])
@login_required
def covidNew():
    form = CovidForm()
    if form.validate_on_submit():
        newCovid = Covid(
            date = form.date.data,
            address = form.address.data,
            option = form.option.data,
            author = current_user.id,
            modifydate = dt.datetime.utcnow
        )
        newCovid.save()
        return redirect(url_for('covid',covidID=newCovid.id))
