from flask import Blueprint, render_template
from flask import request, session, redirect, url_for

login_page = Blueprint('login_page', __name__, template_folder="static")

@login_page.route('/login', methods=['GET'])
def toLoginPage():
    return render_template('login.html')

@login_page.route('/login', methods=['POST'])
def postLoginForm():
    username = request.form['username']
    session['username'] = username
    return redirect(url_for('index'))

@login_page.route('/logout', methods=['GET'])
def logout():
    session.pop('username')
    return redirect(url_for('login_page.toLoginPage'))