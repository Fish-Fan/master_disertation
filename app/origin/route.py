from . import origin
from flask import session, render_template, jsonify, request
import json
from app import fbp
from app.fbp.port import Port

global scope
scope = {}

@origin.route("/", methods=['GET'])
def index():
    if not session.get('username'):
        return origin.send_static_file("login.html")
    return render_template('index.html', name=session.get('username'))

@origin.route("/nodestree", methods=['GET'])
def nodestree():
    tree = list()
    repository = fbp.repository()
    node_specs = repository.get("nodespec")

    for k, v in node_specs.iteritems():
        _insert(tree, v)
    return jsonify(tree)


def _insert(treeroot, node):
    id = node["id"]
    ids = id.split(".")
    found = False

    for n in treeroot:
        if n["id"] == ids[0]:
            found = True
            _inset_node(n, node, ids)

    if not found:
        item = dict()
        item["id"] = ids[0]
        item["title"] = ids[0]
        item["children"] = list()
        treeroot.append(item)
        _inset_node(item, node, ids)

    return


def _inset_node(parent, node, path):
    if len(path) == 1:
        if path[0] == parent["id"]:
            parent["value"] = node
    else:
        if path[0] == parent["id"]:
            children = parent["children"]
            found = False
            for item in children:
                if item["id"] == path[1]:
                    _inset_node(item, node, path[1:])
                    found = True

            if not found:
                item = dict()
                item["id"] = path[1]
                item["title"] = path[1]
                item["children"] = list()
                parent["children"].append(item)
                _inset_node(item, node, path[1:])
    return


@origin.route("/nodes", methods=['GET', 'POST'])
def nodes():
    repository = fbp.repository()
    if request.method == 'POST':
        node = request.get_json()
        repository.register("nodespec", node["id"], node)
        return jsonify(node), 200, {'ContentType': 'application/json'}
    else:
        node_specs = repository.get("nodespec")

        if not node_specs:
            return jsonify({}), 200, {'ContentType': 'application/json'}

        # Adding default output when it is not there
        for k, v in node_specs.items():
            if not "output" in v["port"].keys():
                v["port"]["output"] = list()
                v["port"]["output"].append({"name": "out"})

        return jsonify(node_specs), 200, {'ContentType': 'application/json'}


@origin.route("/nodes/<id>", methods=['GET', 'DELETE', 'PUT'])
def get_node(id):
    repository = fbp.repository()
    if request.method == 'GET':
        node = repository.get("nodespec", id)
        return jsonify(node), 200, {'ContentType': 'application/json'}
    elif request.method == 'DELETE':
        repository.unregister("nodespec", id)
        return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}
    elif request.method == 'PUT':
        node = request.get_json()
        # TODO Valude the node here
        repository.register("nodespec", id, node)
        return jsonify(node), 200, {'ContentType': 'application/json'}

    return json.dumps({'success': False}), 400, {'ContentType': 'application/json'}


@origin.route("/flows", methods=['GET', 'POST'])
def flows():
    repository = fbp.repository()
    if request.method == 'POST':
        flow = request.get_json()
        repository.register("flow", flow["id"], flow)
        return jsonify(flow)
    else:
        flows = repository.get("flow")
        if flows is None:
            return jsonify({})

        result = [v for k, v in flows.items()]
        return jsonify(result)

@origin.route("/flows/<id>", methods=['GET'])
def get_flow(id):
    repository = fbp.repository()
    node = repository.get("flow", id)
    return jsonify(node)


@origin.route("/runflow", methods=['POST'])
def runflow():
    # try:

    # print(scope)

    data = request.get_json()
    tbs = fbp.run_flow(data, scope)

    # tbs2 = []

    # for i, tb in enumerate(tbs):
    #     print(type(tb['outputs']))
    #     if isinstance(tb['outputs'], pd.DataFrame):
    #         print('dataframe00000000000000000---------------------------')
    #         tb['outputs'] = tb['outputs'].index.values.tolist()

        # tbs2.append(tb)

    # print(tbs2)

    return jsonify(tbs)
    # except Exception as e:
    #     return json.dumps({"error": str(e)}), 500



@origin.route("/ports/types", methods=['GET'])
def get_supported_port_types():
    return jsonify(types=Port.support_types())