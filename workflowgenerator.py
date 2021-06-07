import json
import time

from fbp import Node
from fbp import Flow
from fbp import repository
from fbp import port
def create_node(spec_id, id, name, scope):
    spec = repository().get("nodespec", spec_id)

    if spec is None:
        raise Exception("No such node specification {}".format(spec_id))

    anode = Node(id, name, spec,scope)
    return anode


def _run_flow(flow_spec, scope):
    end_node = None
    flow_spec_obj = flow_spec
    aflow = Flow(flow_spec_obj.get("id"), flow_spec_obj.get("name"))

    for node_def in flow_spec_obj.get("nodes"):
        anode = create_node(node_def.get("spec_id"),
                            node_def.get("id"), node_def.get("name"), scope)

        aflow.add_node(anode)

        if "is_end" in node_def.keys() and node_def.get("is_end") == 1:
            end_node = anode
        for port_def in node_def.get("ports"):
            anode.set_inport_value(port_def.get("name"), port_def.get("value"))

    for link_def in flow_spec_obj.get("links"):
        print('link')
        source = link_def.get("source").split(":")
        target = link_def.get("target").split(":")

        aflow.link(source[0], source[1], target[0], target[1])

    stats = aflow.run(end_node)
    return stats
