#!/usr/bin/python

### import guacamole libraries
import avango
import avango.gua
import avango.daemon

### import application libraries
from lib.GuaVE import GuaVE
#from lib.FPSGui import FPSGui


class StereoViewingSetup:

    ### constructor
    def __init__(self,
        SCENEGRAPH = None,
        WINDOW_RESOLUTION = avango.gua.Vec2ui(1024, 1024), # in pixel
        SCREEN_DIMENSIONS = avango.gua.Vec2(0.3, 0.3), # in meter        
        LEFT_SCREEN_POSITION = avango.gua.Vec2ui(0, 0), # in pixel
        LEFT_SCREEN_RESOLUTION = avango.gua.Vec2ui(1024, 1024), # in pixel
        RIGHT_SCREEN_POSITION = avango.gua.Vec2ui(0, 0), # in pixel
        RIGHT_SCREEN_RESOLUTION = avango.gua.Vec2ui(1024, 1024), # in pixel   
        WARP_MATRIX_RED_RIGHT = None,
        WARP_MATRIX_GREEN_RIGHT = None,
        WARP_MATRIX_BLUE_RIGHT = None,
        WARP_MATRIX_RED_LEFT = None,
        WARP_MATRIX_GREEN_LEFT = None,
        WARP_MATRIX_BLUE_LEFT = None,
        SCREEN_MATRIX = avango.gua.make_identity_mat(),
        STEREO_FLAG = False,
        STEREO_MODE = avango.gua.StereoMode.ANAGLYPH_RED_CYAN,
        HEADTRACKING_FLAG = False,
        HEADTRACKING_STATION = None,
        TRACKING_TRANSMITTER_OFFSET = avango.gua.make_identity_mat(),
        ):

        ### resources ###
        
        self.shell = GuaVE()

        ## init window
        self.window = avango.gua.nodes.Window(Title = "window")
        self.window.Size.value = WINDOW_RESOLUTION
        #self.window.Display.value = ":0.2" # 3rd GPU

        if LEFT_SCREEN_POSITION != None:
            self.window.LeftPosition.value = LEFT_SCREEN_POSITION

        self.window.LeftResolution.value = LEFT_SCREEN_RESOLUTION

        if RIGHT_SCREEN_POSITION != None:
            self.window.RightPosition.value = RIGHT_SCREEN_POSITION
        
        self.window.RightResolution.value = RIGHT_SCREEN_RESOLUTION

        if WARP_MATRIX_RED_RIGHT != None:
            self.window.WarpMatrixRedRight.value = WARP_MATRIX_RED_RIGHT

        if WARP_MATRIX_GREEN_RIGHT != None:
            self.window.WarpMatrixGreenRight.value = WARP_MATRIX_GREEN_RIGHT

        if WARP_MATRIX_BLUE_RIGHT != None:
            self.window.WarpMatrixBlueRight.value = WARP_MATRIX_BLUE_RIGHT

        if WARP_MATRIX_RED_LEFT != None:
            self.window.WarpMatrixRedLeft.value = WARP_MATRIX_RED_LEFT

        if WARP_MATRIX_GREEN_LEFT != None:
            self.window.WarpMatrixGreenLeft.value = WARP_MATRIX_GREEN_LEFT

        if WARP_MATRIX_BLUE_LEFT != None:
            self.window.WarpMatrixBlueLeft.value = WARP_MATRIX_BLUE_LEFT


        self.window.EnableVsync.value = False
        
        avango.gua.register_window(self.window.Title.value, self.window) 


        ## init viewer
        self.viewer = avango.gua.nodes.Viewer()
        self.viewer.SceneGraphs.value = [SCENEGRAPH]
        self.viewer.Windows.value = [self.window]
        self.viewer.DesiredFPS.value = 60.0 # in Hz


        ## init passes & render pipeline description
        self.resolve_pass = avango.gua.nodes.ResolvePassDescription()
        self.resolve_pass.EnableSSAO.value = False
        self.resolve_pass.SSAOIntensity.value = 4.0
        self.resolve_pass.SSAOFalloff.value = 10.0
        self.resolve_pass.SSAORadius.value = 7.0
        #self.resolve_pass.EnableScreenSpaceShadow.value = True
        self.resolve_pass.EnvironmentLightingColor.value = avango.gua.Color(0.3, 0.3, 0.3)
        self.resolve_pass.ToneMappingMode.value = avango.gua.ToneMappingMode.UNCHARTED
        self.resolve_pass.Exposure.value = 1.0
        self.resolve_pass.EnableFog.value = True
        self.resolve_pass.FogStart.value = 60.0
        self.resolve_pass.FogEnd.value = 120.0        
        

        #self.resolve_pass.BackgroundMode.value = avango.gua.BackgroundMode.COLOR
        #self.resolve_pass.BackgroundColor.value = avango.gua.Color(0.45, 0.5, 0.6)        
        self.resolve_pass.BackgroundMode.value = avango.gua.BackgroundMode.SKYMAP_TEXTURE        
        self.resolve_pass.BackgroundTexture.value = "data/textures/sky.png"

        self.pipeline_description = avango.gua.nodes.PipelineDescription(Passes = [])
        self.pipeline_description.EnableABuffer.value = True
        self.pipeline_description.Passes.value.append(avango.gua.nodes.TriMeshPassDescription())
        self.pipeline_description.Passes.value.append(avango.gua.nodes.LightVisibilityPassDescription())
        self.pipeline_description.Passes.value.append(self.resolve_pass)
        self.pipeline_description.Passes.value.append(avango.gua.nodes.TexturedScreenSpaceQuadPassDescription())        
        self.pipeline_description.Passes.value.append(avango.gua.nodes.SSAAPassDescription())


        ## init navigation node
        self.navigation_node = avango.gua.nodes.TransformNode(Name = "navigation_node")
        SCENEGRAPH.Root.value.Children.value.append(self.navigation_node)
        
        ## init head node
        self.head_node = avango.gua.nodes.TransformNode(Name = "head_node")
        self.head_node.Transform.value = avango.gua.make_trans_mat(0.0, 0.0, 0.6) # default head position
        self.navigation_node.Children.value.append(self.head_node)

        if HEADTRACKING_FLAG == True:
            self.headtracking_sensor = avango.daemon.nodes.DeviceSensor(DeviceService = avango.daemon.DeviceService())
            self.headtracking_sensor.Station.value = HEADTRACKING_STATION
            self.headtracking_sensor.TransmitterOffset.value = TRACKING_TRANSMITTER_OFFSET

            self.head_node.Transform.connect_from(self.headtracking_sensor.Matrix)


        ## init screen node
        self.screen_node = avango.gua.nodes.ScreenNode(Name = "screen_node")
        self.screen_node.Width.value = SCREEN_DIMENSIONS.x
        self.screen_node.Height.value = SCREEN_DIMENSIONS.y
        self.screen_node.Transform.value = SCREEN_MATRIX
        self.navigation_node.Children.value.append(self.screen_node)
        

        ## init camera node
        self.camera_node = avango.gua.nodes.CameraNode(Name = "camera_node")
        self.camera_node.SceneGraph.value = SCENEGRAPH.Name.value
        self.camera_node.LeftScreenPath.value = self.screen_node.Path.value
        self.camera_node.RightScreenPath.value = self.screen_node.Path.value
        self.camera_node.NearClip.value = 0.1 # in meter
        self.camera_node.FarClip.value = 200.0 # in meter
        self.camera_node.Resolution.value = WINDOW_RESOLUTION
        self.camera_node.OutputWindowName.value = self.window.Title.value
        self.camera_node.BlackList.value = ["invisible"]
        self.camera_node.PipelineDescription.value = self.pipeline_description
        self.head_node.Children.value.append(self.camera_node)

        ## init scene light
        self.scene_light = avango.gua.nodes.LightNode(Name = "scene_light")
        self.scene_light.Color.value = avango.gua.Color(0.9, 0.9, 0.9)
        self.scene_light.Brightness.value = 15.0
        self.scene_light.Falloff.value = 1.0 # exponent
        self.scene_light.EnableShadows.value = True
        self.scene_light.ShadowMapSize.value = 1024
        #self.scene_light.Transform.value = \
        #    avango.gua.make_trans_mat(0.0, 0.5, 0.0) * \
        #    avango.gua.make_rot_mat(-90.0, 1, 0, 0) * \
        #    avango.gua.make_scale_mat(1.0)
        self.scene_light.ShadowNearClippingInSunDirection.value = 0.1
        self.camera_node.Children.value.append(self.scene_light)

        ## pre-render camera setup for portal
        
       
        self.portal_navigation_node = avango.gua.nodes.TransformNode(Name = "portal_navigation_node")
        self.portal_navigation_node.Transform.value = avango.gua.make_trans_mat(0.0,0.5,0.0) * avango.gua.make_rot_mat(90.0,-1,0,0)
        SCENEGRAPH.Root.value.Children.value.append(self.portal_navigation_node)
        
        ## init head node
        self.portal_head_node = avango.gua.nodes.TransformNode(Name = "portal_head_node")
        self.portal_head_node.Transform.value = avango.gua.make_trans_mat(0.0, 0.0, 0.6) # default head position        
        self.portal_navigation_node.Children.value.append(self.portal_head_node)


        ## init screen node
        self.portal_screen_node = avango.gua.nodes.ScreenNode(Name = "portal_screen_node")
        self.portal_screen_node.Width.value = 3.0
        self.portal_screen_node.Height.value = 2.0
        self.portal_navigation_node.Children.value.append(self.portal_screen_node)

        self.portal_camera_node = avango.gua.nodes.CameraNode(Name = "portal_camera_node")
        self.portal_camera_node.SceneGraph.value = SCENEGRAPH.Name.value
        self.portal_camera_node.LeftScreenPath.value = self.portal_screen_node.Path.value
        self.portal_camera_node.RightScreenPath.value = self.portal_screen_node.Path.value
        self.portal_camera_node.NearClip.value = 0.1 # in meter
        self.portal_camera_node.FarClip.value = 100.0 # in meter
        self.portal_camera_node.Resolution.value = avango.gua.Vec2ui(1920, 1200)
        self.portal_camera_node.BlackList.value = ["invisible", "plane"]
        self.portal_camera_node.PipelineDescription.value = self.pipeline_description
        self.portal_camera_node.OutputTextureName.value = "portal_texture"
        self.portal_head_node.Children.value = [self.portal_camera_node]
        self.camera_node.PreRenderCameras.value.append(self.portal_camera_node)
        self.portal_camera_node.Transform.value = avango.gua.make_trans_mat(0,3,0) * avango.gua.make_rot_mat(-90,1,0,0)


        if STEREO_FLAG == True:
            self.camera_node.EnableStereo.value = True
            
            self.window.StereoMode.value = STEREO_MODE
           
            self.set_eye_distance(0.064)


        '''
        ## init sub-class
        self.fpsGui = FPSGui(
            PARENT_NODE = self.screen_node,
            WINDOW = self.window,
            VIEWER = self.viewer,
            )
        '''


    ### functions ###
    def set_eye_distance(self, FLOAT):
        self.camera_node.EyeDistance.value = FLOAT


    def run(self, LOCALS, GLOBALS):
        self.shell.start(LOCALS, GLOBALS)
        self.viewer.run()


    def list_variabels(self):
        self.shell.list_variables()


    def connect_navigation_matrix(self, SF_MATRIX):
        self.navigation_node.Transform.connect_from(SF_MATRIX)


    def get_head_position(self): # get relative head position (towards screen)
        return self.head_node.Transform.value.get_translate()


