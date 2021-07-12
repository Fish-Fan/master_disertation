from os import listdir
from flask import jsonify
import os
from . import inquery
from .. import dataset_location
from .. import report_html_location
from flask import request, session
from app.profiling.Profiling_util import Profiling_util
from ..util.WorkflowGenerator import WorkflowGenerator
from ..util.PreviewUtil import PreviewUtil
from ..util.DataFrameConverter import DataFrameConverter
from ..guidance.Guidance import Guidance
import json


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
    guidance = Guidance(DATASET_PATH + filenames)
    return guidance.analysis()


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

    generator = WorkflowGenerator()
    workFlowJson = generator.generator(rawRemoveColumns, dateTime, rawDateTimeColumns,rawFileName)
    return workFlowJson

@inquery.route('/demodataset', methods=['GET', 'POST'])
def getDemodataset():
    filenames = 'new_uk_500.csv'
    dfc = DataFrameConverter(df=None, source=DATASET_PATH + filenames)
    return dfc.doConvert()

@inquery.route('/column_profiling', methods=['GET', 'POST'])
def columnProfiling():
    column = request.get_json()['column']
    filenames = 'new_uk_500.csv'
    pf = None
    if 'preview_df' in session and session.get('preview_df'):
        pf = Profiling_util(filenames, data_frame=session.get('preview_df'))
    else:
        pf = Profiling_util(DATASET_PATH + filenames)
    ans = pf.getColumnProfiling(column)
    return jsonify(ans)

@inquery.route('/preview', methods=['GET', 'POST'])
def preview():
    filenames = 'new_uk_500.csv'
    pu = PreviewUtil(DATASET_PATH + filenames)
    tmp = pu.getPreviewJson(request.get_json())
    session['preview_df'] = pu.df.to_dict()
    return tmp


