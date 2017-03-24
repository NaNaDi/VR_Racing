#!/usr/bin/python

### import guacamole libraries
import avango
import avango.gua
from avango.script import field_has_changed
import avango.daemon

from lib.scene import Scene
from lib.SimpleViewingSetup import SimpleViewingSetup
from lib.MultiUserViewingSetup import MultiUserViewingSetup
from lib.Intersection import Intersection
from lib.GroundFollowing import GroundFollowing

### import python libraries
import sys

class Server(avango.script.Script):

    trans_mat = avango.avango.gua.SFMatrix4()
    ground_following_vertical_mat = avango.avango.gua.SFMatrix4()

    def __init__(self):
        self.super(Server).__init__()

    def my_constructor(self, SERVER_IP):
        ## init scenegraph
        self.scenegraph = avango.gua.nodes.SceneGraph(Name = "scenegraph")

        physics = avango.gua.nodes.Physics()
        physics_root = avango.gua.nodes.TransformNode(Name="physics_root")
        self.scenegraph.Root.value.Children.value.append(physics_root)

        self.movement = 0.0

        self.old_rotation = avango.gua.Quat()
        self.old_leg_pos = 0.0

        #self.navigation = Navigation()

        self.navigation_node = avango.gua.nodes.TransformNode()

        self.velocity = 0.0

        #self.rotation_offset = avango.gua.make_rot_mat(90,0,1,0)

        ## init server viewing setup
        self.serverViewingSetup = SimpleViewingSetup(
            SCENEGRAPH = self.scenegraph,
            WINDOW_RESOLUTION = avango.gua.Vec2ui(1200, 1200),
            SCREEN_DIMENSIONS = avango.gua.Vec2(10.0, 10.0),
            NAVIGATION_MATRIX = \
                avango.gua.make_trans_mat(0.0,30.0,0.0) * \
                avango.gua.make_rot_mat(90.0,-1,0,0),
            PROJECTION_MODE = avango.gua.ProjectionMode.ORTHOGRAPHIC,
            )


        ## init distribution 
        self.nettrans = avango.gua.nodes.NetTransform(Name = "nettrans", Groupname = "AVSERVER|{0}|7432".format(SERVER_IP))
        self.scenegraph.Root.value.Children.value.append(self.nettrans)
        

        #self.client_group = avango.gua.nodes.TransformNode(Name = "client_group")
        #self.nettrans.Children.value.append(self.client_group)

        self.board_sensor = avango.daemon.nodes.DeviceSensor(DeviceService = avango.daemon.DeviceService())
        self.board_sensor.Station.value = "tracking-lcd-prop-1"
        #self.leg_sensor.TransmitterOffset.value = avango.gua.make_trans_mat(0.0,-1.42,1.6)

        self.leg_sensor = avango.daemon.nodes.DeviceSensor(DeviceService = avango.daemon.DeviceService())
        self.leg_sensor.Station.value = "tracking-lcd-prop-2"

        ## init scene
        self.scene = Scene(PARENT_NODE = self.nettrans)
        #_loader = avango.gua.nodes.TriMeshLoader()
        #self.box_trans = avango.gua.nodes.TransformNode()
        #self.box_geometry = _loader.create_geometry_from_file("box_geometry", "data/objects/cube.obj", avango.gua.LoaderFlags.DEFAULTS)
        #self.box_trans.Children.value.append(self.box_geometry)
        #self.scenegraph.Root.value.Children.value.append(self.box_trans)

        #self.box_trans.Transform.connect_from(self.leg_sensor.Matrix)

        #skate_acceleration = Skateboard_Acceleration()

        #self.skate_trans = self.scene.getSkateboard()
        #self.skate_trans = avango.gua.nodes.TransformNode()
        self.skate_trans = self.scene.getSkateboard()
        self.trans_mat.connect_from(self.board_sensor.Matrix)
        self.groundFollowing = GroundFollowing()
        self.groundFollowing.my_constructor(SCENEGRAPH = self.scenegraph, START_MATRIX = avango.gua.make_trans_mat(self.skate_trans.Transform.value.get_translate()))
        self.ground_following_vertical_mat.connect_from(self.groundFollowing.sf_modified_mat)
        #skate_acceleration.my_constructor(PARENT_NODE = self.nettrans, LEG_NODE = self.skate_trans)


        #self.skate_trans.Transform.value *= avango.gua.make_scale_mat(0.025)

        ## init client setups
        
        #first Client
        #self.clientSetup0 = ClientSetup() #athena
        #self.clientSetup0.my_constructor(PARENT_NODE = self.skate_trans,CLIENT_IP = "141.54.147.30", SCENEGRAPH = self.scenegraph)
        #    #CLIENT_IP = "141.54.147.35", # Oculus1 workstation
        #    #CLIENT_IP = "141.54.147.52", # Oculus2 workstation
        #    #CLIENT_IP = "141.54.147.28", # artemis
        #    #KINECT_FILENAME = "/opt/kinect-resources/calib_3dvc/surface_23_24_25_26_1.ks",

        #self.clientSetup0.navigation_node.Transform.connect_from(self.skate_trans.Transform)

        # distribute complete scenegraph
        distribute_all_nodes_below(NETTRANS = self.nettrans, NODE = self.nettrans)

        print_graph(self.scenegraph.Root.value)

        self.always_evaluate(True)
        
        ## start application/render loop
        self.serverViewingSetup.run(locals(), globals())

    def evaluate(self):
        leg_pos = self.leg_sensor.Matrix.value.get_translate().z
        #self.skate_trans.Transform.value *= self.ground_following_vertical_mat.value
        #print(self.ground_following_vertical_mat.value)
        if leg_pos<self.old_leg_pos:
            self.old_leg_pos=leg_pos
        if leg_pos<0.1 and leg_pos>-0.1 and self.old_leg_pos != 0.0 and self.old_leg_pos < -0.1:
            #self.skate_trans.Transform.value += avango.gua.make_trans_mat(0,0,self.old_leg_pos)
            self.velocity += self.old_leg_pos
            self.old_leg_pos=0.0
        if self.velocity < 0.0:
            self.skate_trans.Transform.value *= avango.gua.make_trans_mat(0,0,self.velocity*0.1)
            self.velocity += 0.00005
        else:
            self.velocity = 0.0

    @field_has_changed(trans_mat)
    def trans_mat_changed(self):
        _rot = self.trans_mat.value.get_rotate()
        self.skate_trans.Transform.value *= avango.gua.make_inverse_mat(avango.gua.make_rot_mat(self.old_rotation))
        self.skate_trans.Transform.value *= avango.gua.make_rot_mat(_rot.x*100, 1, 0, 0) * avango.gua.make_rot_mat(_rot.z*100*8, 0, 1, 0) * avango.gua.make_rot_mat(_rot.z*100, 0, 0, 1)
        self.old_rotation = self.skate_trans.Transform.value.get_rotate()



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
    server = Server() 
    server.my_constructor(SERVER_IP = "141.54.147.32") # boreas


