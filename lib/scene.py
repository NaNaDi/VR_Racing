import avango
import avango.script
import avango.gua


class Scene:


    ## constructor
    def __init__(
        self,
        PARENT_NODE = None,
        ):

        if PARENT_NODE is None:
            print("ERROR: parent node missing")            
            quit()


        ### resources ###
        

        ## init scene light
        self.scene_light = avango.gua.nodes.LightNode(Name = "scene_light")
        self.scene_light.Type.value = avango.gua.LightType.POINT
        self.scene_light.Color.value = avango.gua.Color(0.9, 0.9, 0.9)
        self.scene_light.Brightness.value =70.0
        self.scene_light.Falloff.value = 1.0 # exponent
        self.scene_light.EnableShadows.value = True
        self.scene_light.ShadowMapSize.value = 1024
        self.scene_light.Transform.value = \
            avango.gua.make_trans_mat(0.0, 3.0, 1.0) * \
            avango.gua.make_scale_mat(10.0)
        self.scene_light.ShadowNearClippingInSunDirection.value = 0.1
        #self.scene_light.ShadowFarClippingInSunDirection.value = 10.0
        self.scene_light.ShadowMaxDistance.value = 10.0 # maximal distance, the shadow is visible
        PARENT_NODE.Children.value.append(self.scene_light)
        loader = avango.gua.nodes.TriMeshLoader()

        self.skate_transform = avango.gua.nodes.TransformNode(Name="skate_transform")
        self.skateboard = loader.create_geometry_from_file("kawaii_skateboard", "data/skateboard/kawaii_skateboard.obj", avango.gua.LoaderFlags.DEFAULTS)
        #skateboard.Material.value.set_uniform("Color", avango.gua.Vec4(1.0,0.153,1.0,1.0))
        self.skate_parent = avango.gua.nodes.TransformNode(Name="skate_parent")
        self.skate_transform.Children.value = [self.skateboard]
        self.skate_transform.Transform.value = avango.gua.make_scale_mat(0.05) * avango.gua.make_rot_mat(180.0,0,1,0)# * avango.gua.make_trans_mat(0,10,0)
        self.skate_parent.Children.value.append(self.skate_transform)
        PARENT_NODE.Children.value.append(self.skate_parent)

        for _node in self.skateboard.Children.value:
            _node.Material.value.set_uniform("Emissivity", 0.20) # 20% self-lighting
            _node.Material.value.EnableBackfaceCulling.value = False
            _node.Material.value.set_uniform("Color", avango.gua.Vec4(1.0,0.153,1.0,1.0))

        self.scooter_transform = avango.gua.nodes.TransformNode(Name="scooter_transform")
        self.scooter = loader.create_geometry_from_file("kawaii_scooter", "data/kawaii_scooter/scooter_super.obj", avango.gua.LoaderFlags.DEFAULTS)
        #skateboard.Material.value.set_uniform("Color", avango.gua.Vec4(1.0,0.153,1.0,1.0))
        self.scooter_parent = avango.gua.nodes.TransformNode(Name="scooter_parent")
        self.scooter_transform.Children.value = [self.scooter]
        self.scooter_transform.Transform.value = avango.gua.make_scale_mat(0.05) * avango.gua.make_trans_mat(-10,-35,-20)
        self.scooter_parent.Children.value.append(self.scooter_transform)
        PARENT_NODE.Children.value.append(self.scooter_parent)

        for _node in self.scooter.Children.value:
            _node.Material.value.set_uniform("Emissivity", 0.20) # 20% self-lighting
            _node.Material.value.EnableBackfaceCulling.value = False
            _node.Material.value.set_uniform("Color", avango.gua.Vec4(0.0,0.206,0.209,1.0))

        #self.bike_transform = avango.gua.nodes.TransformNode(Name = "bike_trans")
        #self.bike = loader.create_geometry_from_file("kawaii_bike", "data/bike/kawaii_bike.obj", avango.gua.LoaderFlags.DEFAULTS)
        #self.bike_transform.Children.value.append(self.bike)
        #self.bike_transform.Transform.value = avango.gua.make_scale_mat(0.025)
        #PARENT_NODE.Children.value.append(self.bike_transform)

        #for _node in self.bike.Children.value:
        #    _node.Material.value.set_uniform("Emissivity", 0.20) # 20% self-lighting
        #    _node.Material.value.EnableBackfaceCulling.value = False
        #    _node.Material.value.set_uniform("Color", avango.gua.Vec4(0.0,1.0,1.0,1.0))


        ##todo: don't forget to uncomment the finish line
        #self.finish_line = loader.create_geometry_from_file("kawaii_finish_line", "data/objects/cube.obj")
        #self.finish_line.Material.value.set_uniform("kawaii_squares", "data/textures/chessboard.jpg")
        #self.finish_line.Material.value.set_uniform("Color", avango.gua.Vec4(1,1,1,0.5))
        #self.finish_line.Transform.value = avango.gua.make_trans_mat(0,0,-0.4) * avango.gua.make_rot_mat(90,0,1,0) * avango.gua.make_scale_mat(2,2,0.1)
        #PARENT_NODE.Children.value.append(self.finish_line)

        self.landscape = loader.create_geometry_from_file("kawaii_landscape", "data/Racetrack/Racetrack.obj", avango.gua.LoaderFlags.DEFAULTS  | avango.gua.LoaderFlags.LOAD_MATERIALS)
        self.landscape.Transform.value = avango.gua.make_trans_mat(-8.0,-22.25,22.0)
        PARENT_NODE.Children.value.append(self.landscape)

        self.senpai = loader.create_geometry_from_file("kawaii_senpai", "data/Senpiiix3/Senpi.obj", avango.gua.LoaderFlags.DEFAULTS)
        self.senpai.Transform.value = avango.gua.make_trans_mat(-2,-0.25,1.25) * avango.gua.make_rot_mat(85,0,1,0) *  avango.gua.make_scale_mat(0.25)
        PARENT_NODE.Children.value.append(self.senpai)

        self.collision_shape = loader.create_geometry_from_file("kawaii_collision_shape", "data/Racetrack/Collision_Shape.obj", avango.gua.LoaderFlags.DEFAULTS  | avango.gua.LoaderFlags.LOAD_MATERIALS | avango.gua.LoaderFlags.MAKE_PICKABLE)
        self.collision_shape.Transform.value = avango.gua.make_trans_mat(-8.0,-21.45,22.0)
        self.collision_shape.Material.value.set_uniform("Color", avango.gua.Vec4(1,1,1,0.5))
        PARENT_NODE.Children.value.append(self.collision_shape)

    def getSkateboard(self):
        return self.skate_parent

    def getScooter(self):
        return self.scooter_parent