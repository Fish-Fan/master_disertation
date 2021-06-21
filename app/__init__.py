from flask import Flask
from flask_socketio import SocketIO


socketio = SocketIO()
dataset_location = '../dataset/'
report_html_location = '../static/report_html/'

def create_app():
    # create an application
    app = Flask(__name__, static_folder='static', template_folder='template')
    app.secret_key = 'fanyank_key'
    app.debug = True

    """the import has to be happened at this moment, or it'll cause circular import error"""
    from .inquery import inquery as inqueryBlueprint
    from .login import login as loginBlueprint
    from .origin import origin as originBlueprint
    app.register_blueprint(inqueryBlueprint)
    app.register_blueprint(loginBlueprint)
    app.register_blueprint(originBlueprint)
    app.config['dataset_location'] = dataset_location
    app.config['report_html_location'] = report_html_location
    socketio.init_app(app)
    return app