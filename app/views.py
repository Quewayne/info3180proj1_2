"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/

This file creates your application.
"""
import os
from flask import Flask, render_template, session, redirect, url_for, flash, request, jsonify
#from flask.ext.script import Manager
from werkzeug import secure_filename
from flask.ext.bootstrap import Bootstrap
#from flask.ext.moment import Moment
from sqlalchemy.sql import *
from flask_wtf.file import *
from flask.ext.uploads import UploadSet, IMAGES
from flask.ext.wtf import Form
from random import randint
from datetime import *
from wtforms import StringField, SubmitField, FileField, RadioField, HiddenField
from wtforms.validators import Required, NumberRange
from flask.ext.sqlalchemy import SQLAlchemy
from app.models import Profile

from app import app
#from flask import render_template, request, redirect, url_for
app.config['SECRET_KEY'] = 'hard to guess string'
app.config['UPLOAD_FOLDER'] = 'app/static/img/uploads'
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)

images = UploadSet("images", IMAGES)

class NameForm(Form):
    fle= FileField('Profile Pic', validators=[file_required(),file_allowed(images, "Images only!")])
    fname = StringField('First Name', validators=[Required()])
    lname = StringField('Last Name', validators=[Required()])
    age = StringField('Age', validators=[Required(), NumberRange(10,85)])
    uname = StringField('User Name', validators=[Required()])
    sex=RadioField('Sex', choices=[('M','Male'),('F','Female')])
    submit = SubmitField('Submit')

###
# Routing for your application.
###

@app.route('/')
def home():
    """Render website's home page."""
    return render_template('home.html')

@app.route('/profile/', methods=['GET', 'POST'])
def profile():
    form = NameForm()
    if form.validate_on_submit():
        #filename = secure_filename(form.fle.data.filename)
        #form.fle.data.save('uploads/' + filename)
        im = request.files['fle']
        im_fn = form.fname.data + '_' + secure_filename(im.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], im_fn)
        im.save(file_path)
        while True:
                uid = randint(620000000,620099999)
                if not db.session.query(exists().where(Profile.uid == str(uid))).scalar():
                    break
        profile=Profile(form.fname.data, form.lname.data, form.age.data,form.sex.data,im_fn,form.uname.data,datet(),uid) 
        db.session.add(profile)
        db.session.commit()
    """Render website's home page."""
    return render_template('profile.html', form=form)

def datestr(dtime):
  return dtime.strftime("%a, %d %b, %Y")

@app.route('/profile/<idn>')
def  showprofile(idn):
    profile = Profile.query.filter_by(uid=idn).first()
    imgURL = url_for('static', filename='img/uploads/'+profile.img)
    if request.method == 'POST' and request.headers['Content-Type']== 'application/json':
        return jsonify(userid=profile.uid, image=imgURL,username=profile.uname, sex=profile.sex, age=profile.age,profile_added_on=profile.added)
    #image = '/uploads/' + profile.img
    user = {'id':profile.uid,'image':imgURL,'fname':profile.fname, 'lname':profile.lname,'age':profile.age, 'sex':profile.sex,'uname':profile.uname,'hscore':profile.hscore,'tdoll':profile.tdoll}
    return render_template('view.html', user=user,datestring=datestr(profile.added))



@app.route('/about/')
def about():
    """Render the website's about page."""
    return render_template('about.html')


@app.route('/profiles/', methods=["GET", "POST"])
def profiles():
    users = db.session.query(Profile).all()
    if request.method == "POST" and request.headers['Content-Type']== 'application/json':
        ulist=[]
        for user in users:
            ulist.append({'user name':user.uname,'userid':user.uid})
        return jsonify(users=ulist)
    else:
        return render_template('profiles.html', users=users)



###
# The functions below should be applicable to all Flask apps.
###

def datet():
  """Return current datetime obj"""
  return datetime.now()

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=600'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0",port="8888")
