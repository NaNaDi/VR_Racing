#!/usr/bin/python

### import guacamole libraries
import avango
import avango.gua

from lib.scene import scene
from lib.SimpleViewingSetup import SimpleViewingSetup
from lib.MultiUserViewingSetup import MultiUserViewingSetup

### import python libraries
import sys

class Server:

    def __init__(self,
        SERVER_IP,
        ):


        ## init scenegraph
        self.scenegraph = avango.gua.nodes.SceneGraph(Name = "scenegraph")


        ## init server viewing setup
        self.serverViewingSetup = SimpleViewingSetup(
            SCENEGRAPH = self.scenegraph,
            WINDOW_RESOLUTION = avango.gua.Vec2ui(1200, 1200),
            SCREEN_DIMENSIONS = avango.gua.Vec2(10.0, 10.0),
            NAVIGATION_MATRIX = \
                avango.gua.make_trans_mat(0.0,10.0,0.0) * \
                avango.gua.make_rot_mat(90.0,-1,0,0),
            PROJECTION_MODE = avango.gua.ProjectionMode.ORTHOGRAPHIC,
            )


        ## init distribution 
        self.nettrans = avango.gua.nodes.NetTransform(Name = "nettrans", Groupname = "AVSERVER|{0}|7432".format(SERVER_IP))
        self.scenegraph.Root.value.Children.value.append(self.nettrans)
        

        self.client_group = avango.gua.nodes.TransformNode(Name = "client_group")
        self.nettrans.Children.value.append(self.client_group)

        ## init scene
        self.scene = Scene(PARENT_NODE = self.nettrans)

        ## init client setups
        
        # first Client
        self.clientSetup0 = ClientSetup(
            PARENT_NODE = self.client_group,
            CLIENT_IP = "141.54.147.30", # athena
            #CLIENT_IP = "141.54.147.35", # Oculus1 workstation
            #CLIENT_IP = "141.54.147.52", # Oculus2 workstation
            #CLIENT_IP = "141.54.147.28", # artemis
            #KINECT_FILENAME = "/opt/kinect-resources/calib_3dvc/surface_23_24_25_26_1.ks",
            )

        # distribute complete scenegraph
        distribute_all_nodes_below(NETTRANS = self.nettrans, NODE = self.nettrans)

        print_graph(self.scenegraph.Root.value)
        
        ## start application/render loop
        self.serverViewingSetup.run(locals(), globals())

## Registers a scenegraph node and all of its children at a NetMatrixTransform node for distribution.
# @param NET_TRANS_NODE The NetMatrixTransform node on which all nodes should be marked distributable.
# @param PARENT_NODE The node that should be registered distributable with all of its children.
def distribute_all_nodes_below(NETTRANS = None, NODE = None):

    # do not distribute the nettrans node itself
    if NODE != NETTRANS:
        NETTRANS.distribute_object(NODE)

    # iterate over children and make them distributable
    for _child_node in NODE.Children.value:
        distribute_all_nodes_below(NETTRANS, _child_node)

### helper functions ###

## print the subgraph under a given node to the console
def print_graph(root_node):
  stack = [(root_node, 0)]
  while stack:
    node, level = stack.pop()
    print("│   " * level + "├── {0} <{1}>".format(
      node.Name.value, node.__class__.__name__))
    stack.extend(
      [(child, level + 1) for child in reversed(node.Children.value)])

## print all fields of a fieldcontainer to the console
def print_fields(node, print_values = False):
  for i in range(node.get_num_fields()):
    field = node.get_field(i)
    print("→ {0} <{1}>".format(field._get_name(), field.__class__.__name__))
    if print_values:
      print("  with value '{0}'".format(field.value))


if __name__ == '__main__':
    server = Server(SERVER_IP = "141.54.147.45") # kronos