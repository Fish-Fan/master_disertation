from flask import Blueprint

login = Blueprint('login', __name__)

"""the import has to be happened at this moment, or it'll cause circular import error"""
from . import event, route