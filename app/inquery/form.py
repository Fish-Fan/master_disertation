from os import listdir
from flask import jsonify
import os
from . import inquery
from .. import dataset_location
from .. import report_html_location
from flask import request, session
from app.profiling import profiling_util
from ..util import Workflowgenerator


DATASET_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), dataset_location)
REPORT_HTML_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), report_html_location)

# get data set names from local folders
@inquery.route("/dataset", methods=['GET', 'POST'])
def getDataset():
    filenames = [f for f in listdir(DATASET_PATH) if os.path.isfile(os.path.join(DATASET_PATH, f))]
    print(filenames)
    return jsonify(filenames)

@inquery.route("/profiling", methods=['POST'])
def doProfiling():
    filenames = request.get_json()['filename']
    session['filenames'] = filenames
    pf = profiling_util.profiling_util(DATASET_PATH + filenames)
    res = pf.getinfo()
    res['reportName'] = pf.generateHtmlReport()
    return jsonify(res)

@inquery.route('/generateworkflow', methods=['POST'])
def generateworkflow():
    rawRemoveColumns = request.get_json()['removeColumns']
    rawDateTime = request.get_json()['dateTime']
    rawDateTimeColumns = request.get_json()['dateTimeColumn']
    rawFileName = session.get('filenames')

    #pre-process datetime variable
    dateTime = {}
    if 'date' in rawDateTime:
        dateTime['date'] = True
    if 'time' in rawDateTime:
        dateTime['time'] = True

    generator = Workflowgenerator.WorkflowGenerator()
    workFlowJson = generator.generator(rawRemoveColumns, dateTime, rawDateTimeColumns,rawFileName)
    return workFlowJson
