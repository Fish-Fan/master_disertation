from .. import socketio
from app.profiling import profiling_util
from flask_socketio import emit
import os
from .. import dataset_location
from flask import session

PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), dataset_location)

# receive user picked filename
@socketio.on("post_files")
def receiveDataset(json):
    filenames = json.get('filenames')[0]
    pf = profiling_util.profiling_util(PATH + filenames)
    session['filenames'] = filenames
    session.modified = True
    columns = pf.getColumns()
    emit('columns', columns)
    # with open('resoures/text/task2.json') as f:
    #     result = json.load(f)
    # return jsonify(result)

# receive user picked datetime column name
@socketio.on('post_datetime_column')
def receiveDateTimeColumn(json):
    datetimeColumn = json.get('datetimeColumn')[0]
    print(datetimeColumn)

@socketio.event
def handle_my_event(json):
    print('receive socket message ' + str(json))
    pf = profiling_util.profiling_util(PATH + 'qqq.csv')
    columns = pf.getColumns()
    emit('myemit', columns)
    return "emit response from flask"

@socketio.on('myemit')
def handle_message(data):
    print('receive message ' + str(data))