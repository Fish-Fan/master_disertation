from os import listdir
from flask import jsonify
import os
from . import inquery
from .. import dataset_location

PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), dataset_location)

# get data set names from local folders
@inquery.route("/dataset", methods=['GET', 'POST'])
def getDataset():
    filenames = [f for f in listdir(PATH) if os.path.isfile(os.path.join(PATH, f))]
    print(filenames)
    return jsonify(filenames)