from flask import Blueprint, render_template
from . import db
from flask_login import login_required, current_user

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/about')
def about():
    return render_template('intro.html')

@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.name)
