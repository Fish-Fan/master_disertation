from flask import Blueprint

inquery = Blueprint('inquery', __name__)

"""the import has to be happened at this moment, or it'll cause circular import error"""
from . import event, route, form