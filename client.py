#!/usr/bin/python

### import guacamole libraries
import avango
import avango.gua
import avango.script

### import application libraries
from lib.SimpleViewingSetup import SimpleViewingSetup
from lib.MultiUserViewingSetup import MultiUserViewingSetup
from lib.ViewingSetup import StereoViewingSetup


### import python libraries
import time
import sys

class Client(avango.script.Script):

    def __init__(self):
        self.super(Client).__init__()

    def my_constructor(self,
        SERVER_IP,
        CLIENT_IP,
        ):

        print("CLIENT on", CLIENT_IP, "is connected to SERVER on", SERVER_IP)
    
        ### parameters ###
        self.client_ip = CLIENT_IP

        self.old_trans = avango.gua.make_identity_mat()

        self.old_nav_trans = avango.gua.make_identity_mat()
    
    
        ### resources ###
    
        ## init scenegraph
        self.scenegraph = avango.gua.nodes.SceneGraph(Name = "scenegraph")

        ## init distribution 
        self.nettrans = avango.gua.nodes.NetTransform(Name = "nettrans", Groupname = "AVCLIENT|{0}|7432".format(SERVER_IP))
        self.scenegraph.Root.value.Children.value.append(self.nettrans)
        self.navigation_node = avango.gua.nodes.TransformNode()

        if CLIENT_IP == "141.54.147.28": # artemis
            self.viewingSetup = SimpleViewingSetup(
                SCENEGRAPH = self.scenegraph,
                STEREO_MODE = "mono",
                WINDOW_RESOLUTION = avango.gua.Vec2ui(3840, 2160),
                SCREEN_DIMENSIONS = avango.gua.Vec2(0.62, 0.345),
                BLACK_LIST = [CLIENT_IP],
                )

        elif CLIENT_IP == "141.54.147.29": # atalante
            self.viewingSetup = SimpleViewingSetup(
                SCENEGRAPH = self.scenegraph,
                STEREO_MODE = "mono",
                BLACK_LIST = [CLIENT_IP],
                )

        elif CLIENT_IP == "141.54.147.37": # eris
            ## MITSUBISHI 3D-TV setup
            self.viewingSetup = SimpleViewingSetup(
                SCENEGRAPH = self.nettrans,
                WINDOW_RESOLUTION = avango.gua.Vec2ui(1920, 1080),
                SCREEN_DIMENSIONS = avango.gua.Vec2(1.44, 0.81),
                #SCREEN_MATRIX = avango.gua.make_identity_mat(),
                STEREO_MODE = "checkerboard",        
                HEADTRACKING_SENSOR_STATION = "tracking-lcd-glasses-3",
                TRACKING_TRANSMITTER_OFFSET = avango.gua.make_trans_mat(-1.01,-(0.98 + 0.58),3.5 + 0.48) * avango.gua.make_rot_mat(90.0,0,1,0),
                BLACK_LIST = [CLIENT_IP],
                )


        elif CLIENT_IP == "141.54.147.30": # athena
            ## LCD wall 1-User setup
            self.viewingSetup = StereoViewingSetup(
                SCENEGRAPH = self.scenegraph,
                WINDOW_RESOLUTION = avango.gua.Vec2ui(1920*2, 1200),
                SCREEN_DIMENSIONS = avango.gua.Vec2(3.0, 2.0),
                LEFT_SCREEN_POSITION = avango.gua.Vec2ui(140, 0),
                LEFT_SCREEN_RESOLUTION = avango.gua.Vec2ui(1780, 1185),
                RIGHT_SCREEN_POSITION = avango.gua.Vec2ui(1920, 0),
                RIGHT_SCREEN_RESOLUTION = avango.gua.Vec2ui(1780, 1185),
                STEREO_FLAG = True,
                STEREO_MODE = avango.gua.StereoMode.SIDE_BY_SIDE,
                HEADTRACKING_FLAG = True,
                HEADTRACKING_STATION = "tracking-lcd-glasses-athena", # wired 3D-TV glasses on Mitsubishi 3D-TV workstation
                TRACKING_TRANSMITTER_OFFSET = avango.gua.make_trans_mat(0.0,-1.42,1.6),
                )
            self.navigation_node = self.viewingSetup.navigation_node
            #self.viewingSetup.init_user(HEADTRACKING_SENSOR_STATION = "tracking-lcd-glasses-athena")

        elif CLIENT_IP == "141.54.147.20": #kerberos
            ## DLP wall 1-User setup
            self.viewingSetup = StereoViewingSetup(
                SCENEGRAPH = self.scenegraph,
                WINDOW_RESOLUTION = avango.gua.Vec2ui(1920*2, 1200),
                SCREEN_DIMENSIONS = avango.gua.Vec2(4.2, 2.61),
                LEFT_SCREEN_POSITION = avango.gua.Vec2ui(0, 0),
                LEFT_SCREEN_RESOLUTION = avango.gua.Vec2ui(1920, 1200),
                RIGHT_SCREEN_POSITION = avango.gua.Vec2ui(1920, 0),
                RIGHT_SCREEN_RESOLUTION = avango.gua.Vec2ui(1920, 1200),
                WARP_MATRIX_RED_RIGHT = "/opt/dlp-warpmatrices/dlp_6_warp_P1.warp",
                WARP_MATRIX_GREEN_RIGHT = "/opt/dlp-warpmatrices/dlp_6_warp_P2.warp",
                WARP_MATRIX_BLUE_RIGHT = "/opt/dlp-warpmatrices/dlp_6_warp_P3.warp",
                WARP_MATRIX_RED_LEFT = "/opt/dlp-warpmatrices/dlp_6_warp_P1.warp",
                WARP_MATRIX_GREEN_LEFT = "/opt/dlp-warpmatrices/dlp_6_warp_P2.warp",
                WARP_MATRIX_BLUE_LEFT = "/opt/dlp-warpmatrices/dlp_6_warp_P3.warp",
                SCREEN_MATRIX = avango.gua.make_trans_mat(0.0, 1.55, -1.6),
                STEREO_FLAG = True,
                STEREO_MODE = avango.gua.StereoMode.SIDE_BY_SIDE,
                HEADTRACKING_FLAG = True,
                HEADTRACKING_STATION = "tracking-dlp-glasses-n_1",
                TRACKING_TRANSMITTER_OFFSET = avango.gua.make_trans_mat(0.0,0.045,0.0),
                )
            self.navigation_node = self.viewingSetup.navigation_node             
                
        elif CLIENT_IP == "141.54.147.35": # Oculus1 workstation
             ## SAMSUNG DESKTOP setup
              self.viewingSetup = SimpleViewingSetup(
                SCENEGRAPH = self.scenegraph,
                STEREO_MODE = "mono",
                #STEREO_MODE = "anaglyph",
                WINDOW_RESOLUTION = avango.gua.Vec2ui(1920, 1080),
                SCREEN_DIMENSIONS = avango.gua.Vec2(0.53, 0.3),
                #HEADTRACKING_SENSOR_STATION = "tracking-lcd-prop-1",
                #TRACKING_TRANSMITTER_OFFSET = avango.gua.make_trans_mat(0.54,-(0.98 + 0.64),3.5 + 0.48) * avango.gua.make_rot_mat(90.0,0,1,0),
                BLACK_LIST = [CLIENT_IP],
                )

            ## OCULUS setup
            #self.viewingSetup = OculusViewingSetup(
            #    SCENEGRAPH = self.scenegraph,
            #     )
            
        elif CLIENT_IP == "141.54.147.52": # Oculus2 workstation
             ## SAMSUNG DESKTOP setup
              self.viewingSetup = SimpleViewingSetup(
                SCENEGRAPH = self.scenegraph,
                STEREO_MODE = "mono",
                #STEREO_MODE = "anaglyph",
                WINDOW_RESOLUTION = avango.gua.Vec2ui(1920, 1080),
                SCREEN_DIMENSIONS = avango.gua.Vec2(0.53, 0.3),
                #HEADTRACKING_SENSOR_STATION = "tracking-lcd-prop-1",
                #TRACKING_TRANSMITTER_OFFSET = avango.gua.make_trans_mat(0.54,-(0.98 + 0.64),3.5 + 0.48) * avango.gua.make_rot_mat(90.0,0,1,0),
                BLACK_LIST = [CLIENT_IP],
                )

        else:
            print("ERROR: no viewing setup defined for this IP")
            quit()
        
        print_graph(self.nettrans)
        

        # Triggers framewise evaluation of respective callback method
        self.init_trigger = avango.script.nodes.Update(Callback = self.init_callback, Active = True)
        
        self.always_evaluate(True)

        while True:
            self.viewingSetup.viewer.frame()
        #self.viewingSetup.run(locals(), globals())

    
    ### callback functions ###
    def init_callback(self):
        #print("frame", time.clock(), len(self.nettrans.Children.value))
        
        ## wait for distributed sceneraph to arrive
        if len(self.nettrans.Children.value) > 0:
            for _child_node in self.nettrans.Children.value:
                print(_child_node.Name.value)

            ## uncomment for skateboard client
            #_skate_trans = self.nettrans.Children.value[1]
            #self.navigation_node.WorldTransform.connect_from(_skate_trans.WorldTransform)

            _scooter_trans = self.nettrans.Children.value[2]
            self.navigation_node.WorldTransform.connect_from(_scooter_trans.WorldTransform)
                        
            print_graph(self.nettrans)
        
            self.init_trigger.Active.value = False # disable init callback

    def evaluate(self):
        if self.navigation_node.Transform.value != self.old_nav_trans:
            self.navigation_node.Transform.value *= avango.gua.make_rot_mat(90.0, 0, 1, 0)
            self.old_nav_trans = self.navigation_node.Transform.value
        #if len(self.nettrans.Children.value) > 0:
        #    self.camera_trans = self.nettrans.Children.value[1].WorldTransform.value * avango.gua.make_rot_mat(-90.0, 0, 0, 1)  
        #_nav_trans = self.navigation_node.Transform.value
        #if _nav_trans != self.old_trans:
            #print("_nav_trans: ",_nav_trans)
            #print("old trans: ", self.old_trans)
            #print("╯°□°）╯︵ ┻━┻")
            #self.navigation_node.Transform.value *= avango.gua.make_trans_mat(0,0,-1)
        #    self.old_trans = self.navigation_node.Transform.value



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
    client = Client()
    #client.my_constructor(SERVER_IP = "141.54.147.32", CLIENT_IP = "141.54.147.30") #boreas
    #client.my_constructor(SERVER_IP = "141.54.147.49", CLIENT_IP = "141.54.147.30") #minos
    #client.my_constructor(SERVER_IP = "141.54.147.57", CLIENT_IP = "141.54.147.30") # orestes
    client.my_constructor(SERVER_IP = "141.54.147.45", CLIENT_IP = "141.54.147.20") #kronos with dlp wall