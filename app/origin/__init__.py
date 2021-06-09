from flask import Blueprint

origin = Blueprint('origin', __name__)

"""the import has to be happened at this moment, or it'll cause circular import error"""
from . import route