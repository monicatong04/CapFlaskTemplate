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
        print("validated,saving")
        newCovid = Covid(
            date = form.date.data,
            address = form.address.data,
            option = form.option.data,
            hours = form.hours.data,
            author = current_user.id,
            modifydate = dt.datetime.utcnow
        )
        newCovid.save()
        return redirect(url_for('covid',covidID=newCovid.id))
    print("invalid")
    return render_template('covidform.html',form=form)

@app.route('/covid/<covidID>')
@login_required
def covid(covidID):
    thisCovid = Covid.objects.get(id=covidID)
    return render_template('covid.html',covid=thisCovid)

@app.route('/covid/list')
@login_required
def covidList():
    covids = Covid.objects()
    return render_template('covids.html',covids=covids)

@app.route('/covid/edit/<covidID>', methods=['GET', 'POST'])
@login_required
def covidEdit(covidID):
    editCovid = Covid.objects.get(id=covidID)
    if current_user != editCovid.author:
        flash("You can't edit a post you don't own.")
        return redirect(url_for('covid',covidID=covidID))
    form = CovidForm()
    if form.validate_on_submit():
        editCovid.update(
            date = form.date.data,
            address = form.address.data,
            hours = form.hours.data,
            option = form.option.data,
            modifydate = dt.datetime.utcnow
        )
        return redirect(url_for('covid',covidID=covidID))

    form.date.data = editCovid.date
    form.address.data = editCovid.address
    form.hours.data = editCovid.hours
    form.option.data = editCovid.option

    return render_template('covidform.html',form=form)

@app.route('/covid/delete/<covidID>')
@login_required
def covidDelete(covidID):
    deleteCovid = Covid.objects.get(id=covidID)
    if current_user == deleteCovid.author:
        deleteCovid.delete()
        flash('The Post was deleted.')
    else:
        flash("You can't delete a post you don't own.")
    covids = Covid.objects()  
    return render_template('covids.html',covids=covids)