from os import listdir
from flask import jsonify
import os
from . import inquery
from .. import dataset_location
from flask import request
from app.profiling import profiling_util

PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), dataset_location)

# get data set names from local folders
@inquery.route("/dataset", methods=['GET', 'POST'])
def getDataset():
    filenames = [f for f in listdir(PATH) if os.path.isfile(os.path.join(PATH, f))]
    print(filenames)
    return jsonify(filenames)

@inquery.route("/profiling", methods=['POST'])
def doProfiling():
    filenames = request.get_json()['filename']
    pf = profiling_util.profiling_util(PATH + filenames)
    res = pf.getinfo()
    return jsonify(res)