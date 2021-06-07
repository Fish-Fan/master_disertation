from flask import Blueprint, render_template
from flask import request, session, redirect, url_for

login_page = Blueprint('login_page', __name__)

# @login_page.route('/login')
# def toLoginPage():
#     login_page.send_static_file('login.html')

@login_page.route('/login', methods=['POST'])
def postLoginForm():
    username = request.form['username']
    session['username'] = username
    return redirect(url_for('index'))
