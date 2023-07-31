from flask import Blueprint, render_template, redirect, url_for, request, flash, Flask
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from .models import User
from . import db
from flask_login import login_user, login_required, logout_user
import os
import pathlib

from project.backend import enroll_user, authenticate_user

auth = Blueprint('auth', __name__)
UPLOAD_FOLDER = 'project/uploads'
ALLOWED_EXTENSIONS = {'wav', 'm4a', 'mp3'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@auth.route('/login')
def login():
    return render_template('login.html')

@auth.route('/login', methods=['POST'])
def login_post():
    # login code goes here
    username = request.form.get('username')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(name=username).first()

    # check if the user actually exists
    # take the user-supplied password, hash it, and compare it to the hashed password in the database
    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login')) # if the user doesn't exist or password is wrong, reload the page
    

    # check if the post request has the file part
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    # If the user does not select a file, the browser submits an
    # empty file without a filename.
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(UPLOAD_FOLDER, filename))
    else:
        flash('Error Uploading File')
        return redirect(request.url)

    #Perform Voice Biometrics on File
    authenticated = authenticate_user(username, os.path.join(UPLOAD_FOLDER, filename))
    os.remove(os.path.join(UPLOAD_FOLDER, filename))

    if (not authenticated):
        flash(f'This Audio Recording was not verified as your voice. Please create a new clip and resubmit. Keep in mind, our beta voice biomteric only has 90% accuracy')
        return redirect(request.url)

    # if the above check passes, then we know the user has the right credentials
    login_user(user, remember=remember)
    return redirect(url_for('main.profile'))

@auth.route('/signup')
def signup():
    return render_template('signup.html')

@auth.route('/signup',  methods=['POST'])
def signup_post():
    # code to validate and add user to database goes here
    name = request.form.get('name').lower()
    password = request.form.get('password')

    user = User.query.filter_by(name=name).first() # if this returns a user, then the email already exists in database

    if user: # if a user is found, we want to redirect back to signup page so user can try again
        flash('Username address already exists')
        return redirect(url_for('auth.signup'))

    #Make sure there are no numbers in the username
    if any(i.isdigit() for i in name):
        flash('Do not include numbers in username')
        return redirect(url_for('auth.signup'))

    # Enroll all submitted files into the AI
    for i, f in enumerate(request.files):
        file = request.files[f]
        if file.filename == '':
            flash('Did not upload all files.')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = f"{name}{i}{pathlib.Path(file.filename).suffix}"
            file.save(os.path.join(UPLOAD_FOLDER, filename))
        else:
            flash('Error Uploading File')
            return redirect(request.url)
        
        enroll_user(f"{name}{i}", os.path.join(UPLOAD_FOLDER, filename))
        os.remove(os.path.join(UPLOAD_FOLDER, filename))
        
    # create a new user with the form data. Hash the password so the plaintext version isn't saved.
    new_user = User(name=name, password=generate_password_hash(password, method='sha256'))

    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()

    # code to validate and add user to database goes here
    return redirect(url_for('auth.login'))

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))