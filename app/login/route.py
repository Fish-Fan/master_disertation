from flask import session, render_template, request, redirect, url_for
from . import login



@login.route('/login', methods=['GET'])
def toLoginPage():
    return render_template('login.html')

@login.route('/login', methods=['POST'])
def postLoginForm():
    username = request.form['username']
    session['username'] = username
    return redirect(url_for('origin.index'))

@login.route('/logout', methods=['GET'])
def logout():
    session.pop('username')
    return redirect(url_for('.toLoginPage'))