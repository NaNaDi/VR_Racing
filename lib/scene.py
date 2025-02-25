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
        self.scene_light.Type.value = avango.gua.LightType.SUN
        self.scene_light.Color.value = avango.gua.Color(0.9, 0.9, 0.9)
        self.scene_light.Brightness.value =5.0
        self.scene_light.Falloff.value = 1.0 # exponent
        self.scene_light.EnableShadows.value = True
        #self.scene_light.ShadowMapSize.value = 1024
        #self.scene_light.Transform.value = \
        #    avango.gua.make_trans_mat(0.0, 15.0, 30.0) * \
        #    avango.gua.make_scale_mat(80.0)
        self.scene_light.ShadowNearClippingInSunDirection.value = 0.1
        #self.scene_light.ShadowFarClippingInSunDirection.value = 10.0
        self.scene_light.ShadowMaxDistance.value = 10.0 # maximal distance, the shadow is visible
        PARENT_NODE.Children.value.append(self.scene_light)

        loader = avango.gua.nodes.TriMeshLoader()

        self.skate_transform = avango.gua.nodes.TransformNode(Name="skate_transform")
        self.skateboard = loader.create_geometry_from_file("kawaii_skateboard", "data/skateboard/kawaii_skateboard.obj", avango.gua.LoaderFlags.DEFAULTS)
        self.skateboard.Transform.value = avango.gua.make_rot_mat(180.0,0,1,0) * avango.gua.make_scale_mat(0.05)
        #skateboard.Material.value.set_uniform("Color", avango.gua.Vec4(1.0,0.153,1.0,1.0))
        #self.skate_parent = avango.gua.nodes.TransformNode(Name="skate_parent")
        self.skate_transform.Children.value = [self.skateboard]
        ##comment from Andre: initial position in transform node here
        self.skate_transform.Transform.value = avango.gua.make_trans_mat(0,-0.25,0) * avango.gua.make_rot_mat(90, 0, 1, 0)# * avango.gua.make_scale_mat(0.05) * avango.gua.make_rot_mat(180.0,0,1,0)
        #self.skate_parent.Children.value.append(self.skate_transform)
        PARENT_NODE.Children.value.append(self.skate_transform)

        for _node in self.skateboard.Children.value:
            _node.Material.value.set_uniform("Emissivity", 0.20) # 20% self-lighting
            _node.Material.value.EnableBackfaceCulling.value = False
            _node.Material.value.set_uniform("Color", avango.gua.Vec4(1.0,0.153,1.0,1.0))

        self.scooter_transform = avango.gua.nodes.TransformNode(Name="scooter_transform")
        self.scooter = loader.create_geometry_from_file("kawaii_scooter", "data/kawaii_scooter/scooter_super.obj", avango.gua.LoaderFlags.DEFAULTS)
        self.scooter.Transform.value = avango.gua.make_trans_mat(0,-0.2,0) * avango.gua.make_rot_mat(-90, 0, 1, 0) * avango.gua.make_scale_mat(0.05)
        #skateboard.Material.value.set_uniform("Color", avango.gua.Vec4(1.0,0.153,1.0,1.0))
        #self.scooter_parent = avango.gua.nodes.TransformNode(Name="scooter_parent")
        self.scooter_transform.Children.value = [self.scooter]
        #self.scooter_transform.Transform.value *= avango.gua.make_trans_mat(0, 0, 0.5)
        ## todo: trans * rot * scale
        self.scooter_transform.Transform.value = avango.gua.make_trans_mat(0, 0,-0.5 ) * avango.gua.make_rot_mat(90, 0, 1, 0) #  * avango.gua.make_trans_mat(-10,-35,-20)
        #self.scooter_parent.Children.value.append(self.scooter_transform)
        PARENT_NODE.Children.value.append(self.scooter_transform)

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
        self.finish_line = loader.create_geometry_from_file("kawaii_finish_line", "data/objects/cube.obj", avango.gua.LoaderFlags.DEFAULTS)
        self.finish_line.Transform.value = avango.gua.make_trans_mat(0,0,-0.4) * avango.gua.make_rot_mat(90,0,1,0) * avango.gua.make_scale_mat(2,2,0.01)
        #self.finish_line.Material.value.set_uniform("kawaii_squares", "data/textures/chessboard.jpg")
        self.finish_line.Material.value.set_uniform("ColorMap", "data/textures/chessboard.jpg")
        self.finish_line.Material.value.set_uniform("Color", avango.gua.Vec4(1,1,1,0.5))
        PARENT_NODE.Children.value.append(self.finish_line)

        self.landscape = loader.create_geometry_from_file("kawaii_landscape", "data/Racetrack/Racetrack.obj", avango.gua.LoaderFlags.DEFAULTS | avango.gua.LoaderFlags.LOAD_MATERIALS | avango.gua.LoaderFlags.MAKE_PICKABLE)
        self.landscape.Transform.value = avango.gua.make_trans_mat(-8.0,-21.00,22.0)
        PARENT_NODE.Children.value.append(self.landscape)

        #### hack
        self.landscape.Children.value[0].Name.value = 'street'
        self.landscape.Children.value[1].Name.value = 'meadow'
        self.landscape.Children.value[0].Tags.value = ['STREET_TO_PICK']
        #self.landscape.Children.value[1].Material.value.set_uniform("Color", avango.gua.Vec4(1,1,1,1))
        #self.landscape.Children.value[1].Material.value.set_uniform("ColorMap", "data/textures/grass.jpg")
        ####

        self.senpai = loader.create_geometry_from_file("kawaii_senpai", "data/Senpiiix3/Senpi.obj", avango.gua.LoaderFlags.DEFAULTS)
        self.senpai.Transform.value = avango.gua.make_trans_mat(-2,-0.25,1.25) * avango.gua.make_rot_mat(85,0,1,0) *  avango.gua.make_scale_mat(0.25)
        PARENT_NODE.Children.value.append(self.senpai)

        #self.collision_shape = loader.create_geometry_from_file("kawaii_collision_shape", "data/Racetrack/Collision_Shape.obj", avango.gua.LoaderFlags.DEFAULTS  | avango.gua.LoaderFlags.LOAD_MATERIALS | avango.gua.LoaderFlags.MAKE_PICKABLE)
        #self.collision_shape.Transform.value = avango.gua.make_trans_mat(-8.0,-20.25,22.0)
        #self.collision_shape.Material.value.set_uniform("Color", avango.gua.Vec4(1,1,1,0.5))
        #PARENT_NODE.Children.value.append(self.collision_shape)

        #self.countdown_box_scooter = loader.create_geometry_from_file("countdown_scooter", "data/objects/cube.obj", avango.gua.LoaderFlags.DEFAULTS)
        #self.countdown_box_scooter.Transform.value = avango.gua.make_trans_mat(0,30,25) * avango.gua.make_scale_mat(30) * avango.gua.make_rot_mat(-45.0, 0.5, 0, 0)
        #self.countdown_box_scooter.Material.value.set_uniform("ColorMap", "data/textures/DH216SN.png")
        #self.scooter_transform.Children.value.append(self.countdown_box_scooter)

        ##skate boxes
        self.countdown_box_skate3 = loader.create_geometry_from_file("countdown_skate", "data/objects/cube.obj", avango.gua.LoaderFlags.DEFAULTS)
        self.countdown_box_skate3.Transform.value = avango.gua.make_trans_mat(0,0.75,0) * avango.gua.make_rot_mat(-90,0,0,1) * avango.gua.make_scale_mat(2)
        self.countdown_box_skate3.Material.value.set_uniform("ColorMap", "data/textures/countdown_textures/kawaiicountdown3.png")
        self.countdown_box_skate3.Material.value.set_uniform("Color", avango.gua.Vec4(1,1,1,0))
        self.skate_transform.Children.value.append(self.countdown_box_skate3)

        self.countdown_box_skate2 = loader.create_geometry_from_file("countdown_skate", "data/objects/cube.obj", avango.gua.LoaderFlags.DEFAULTS)
        self.countdown_box_skate2.Transform.value =avango.gua.make_trans_mat(0,0.75,0) * avango.gua.make_rot_mat(-90,0,0,1) *avango.gua.make_scale_mat(2)
        self.countdown_box_skate2.Material.value.set_uniform("ColorMap", "data/textures/countdown_textures/kawaiicountdown2.png")
        self.countdown_box_skate2.Material.value.set_uniform("Color", avango.gua.Vec4(1,1,1,0))
        self.skate_transform.Children.value.append(self.countdown_box_skate2)

        self.countdown_box_skate1 = loader.create_geometry_from_file("countdown_skate", "data/objects/cube.obj", avango.gua.LoaderFlags.DEFAULTS)
        self.countdown_box_skate1.Transform.value =avango.gua.make_trans_mat(0,0.75,0) * avango.gua.make_rot_mat(-90,0,0,1) *avango.gua.make_scale_mat(2)
        self.countdown_box_skate1.Material.value.set_uniform("ColorMap", "data/textures/countdown_textures/kawaiicountdown1.png")
        self.countdown_box_skate1.Material.value.set_uniform("Color", avango.gua.Vec4(1,1,1,0))
        self.skate_transform.Children.value.append(self.countdown_box_skate1)

        self.countdown_box_skatego = loader.create_geometry_from_file("countdown_skate", "data/objects/cube.obj", avango.gua.LoaderFlags.DEFAULTS)
        self.countdown_box_skatego.Transform.value =avango.gua.make_trans_mat(0,0.75,0) * avango.gua.make_rot_mat(-90,0,0,1) *avango.gua.make_scale_mat(2)
        self.countdown_box_skatego.Material.value.set_uniform("ColorMap", "data/textures/countdown_textures/kawaiicountdowngo.png")
        self.countdown_box_skatego.Material.value.set_uniform("Color", avango.gua.Vec4(1,1,1,0))
        self.skate_transform.Children.value.append(self.countdown_box_skatego)

        self.countdown_box_skatewin = loader.create_geometry_from_file("countdown_skate", "data/objects/cube.obj", avango.gua.LoaderFlags.DEFAULTS)
        self.countdown_box_skatewin.Transform.value =avango.gua.make_trans_mat(0,0.75,0) * avango.gua.make_rot_mat(-90,0,0,1) *avango.gua.make_scale_mat(2)
        self.countdown_box_skatewin.Material.value.set_uniform("ColorMap", "data/textures/countdown_textures/kawaiicountdownWIN.png")
        self.countdown_box_skatewin.Material.value.set_uniform("Color", avango.gua.Vec4(1,1,1,0))
        self.skate_transform.Children.value.append(self.countdown_box_skatewin)

        self.countdown_box_skateloose = loader.create_geometry_from_file("countdown_skate", "data/objects/cube.obj", avango.gua.LoaderFlags.DEFAULTS)
        self.countdown_box_skateloose.Transform.value =avango.gua.make_trans_mat(0,0.75,0) * avango.gua.make_rot_mat(-90,0,0,1) *avango.gua.make_scale_mat(2)
        self.countdown_box_skateloose.Material.value.set_uniform("ColorMap", "data/textures/countdown_textures/kawaiicountdownLOOSER.png")
        self.countdown_box_skateloose.Material.value.set_uniform("Color", avango.gua.Vec4(1,1,1,0))
        self.skate_transform.Children.value.append(self.countdown_box_skateloose)

        ##scooter boxes
        self.countdown_box_scooter3 = loader.create_geometry_from_file("countdown_scooter", "data/objects/cube.obj", avango.gua.LoaderFlags.DEFAULTS)
        self.countdown_box_scooter3.Transform.value = avango.gua.make_trans_mat(0,0.75,0) * avango.gua.make_rot_mat(-90,0,0,1) * avango.gua.make_scale_mat(2)
        self.countdown_box_scooter3.Material.value.set_uniform("ColorMap", "data/textures/countdown_textures/kawaiicountdown3.png")
        self.countdown_box_scooter3.Material.value.set_uniform("Color", avango.gua.Vec4(1,1,1,0))
        self.scooter_transform.Children.value.append(self.countdown_box_scooter3)

        self.countdown_box_scooter2 = loader.create_geometry_from_file("countdown_scooter", "data/objects/cube.obj", avango.gua.LoaderFlags.DEFAULTS)
        self.countdown_box_scooter2.Transform.value =avango.gua.make_trans_mat(0,0.75,0) * avango.gua.make_rot_mat(-90,0,0,1) *avango.gua.make_scale_mat(2)
        self.countdown_box_scooter2.Material.value.set_uniform("ColorMap", "data/textures/countdown_textures/kawaiicountdown2.png")
        self.countdown_box_scooter2.Material.value.set_uniform("Color", avango.gua.Vec4(1,1,1,0))
        self.scooter_transform.Children.value.append(self.countdown_box_scooter2)

        self.countdown_box_scooter1 = loader.create_geometry_from_file("countdown_scooter", "data/objects/cube.obj", avango.gua.LoaderFlags.DEFAULTS)
        self.countdown_box_scooter1.Transform.value =avango.gua.make_trans_mat(0,0.75,0) * avango.gua.make_rot_mat(-90,0,0,1) *avango.gua.make_scale_mat(2)
        self.countdown_box_scooter1.Material.value.set_uniform("ColorMap", "data/textures/countdown_textures/kawaiicountdown1.png")
        self.countdown_box_scooter1.Material.value.set_uniform("Color", avango.gua.Vec4(1,1,1,0))
        self.scooter_transform.Children.value.append(self.countdown_box_scooter1)

        self.countdown_box_scootergo = loader.create_geometry_from_file("countdown_scooter", "data/objects/cube.obj", avango.gua.LoaderFlags.DEFAULTS)
        self.countdown_box_scootergo.Transform.value =avango.gua.make_trans_mat(0,0.75,0) * avango.gua.make_rot_mat(-90,0,0,1) *avango.gua.make_scale_mat(2)
        self.countdown_box_scootergo.Material.value.set_uniform("ColorMap", "data/textures/countdown_textures/kawaiicountdowngo.png")
        self.countdown_box_scootergo.Material.value.set_uniform("Color", avango.gua.Vec4(1,1,1,0))
        self.scooter_transform.Children.value.append(self.countdown_box_scootergo)

        self.countdown_box_scooterwin = loader.create_geometry_from_file("countdown_scooter", "data/objects/cube.obj", avango.gua.LoaderFlags.DEFAULTS)
        self.countdown_box_scooterwin.Transform.value =avango.gua.make_trans_mat(0,0.75,0) * avango.gua.make_rot_mat(-90,0,0,1) *avango.gua.make_scale_mat(2)
        self.countdown_box_scooterwin.Material.value.set_uniform("ColorMap", "data/textures/countdown_textures/kawaiicountdownWIN.png")
        self.countdown_box_scooterwin.Material.value.set_uniform("Color", avango.gua.Vec4(1,1,1,0))
        self.scooter_transform.Children.value.append(self.countdown_box_scooterwin)

        self.countdown_box_scooterloose = loader.create_geometry_from_file("countdown_scooter", "data/objects/cube.obj", avango.gua.LoaderFlags.DEFAULTS)
        self.countdown_box_scooterloose.Transform.value =avango.gua.make_trans_mat(0,0.75,0) * avango.gua.make_rot_mat(-90,0,0,1) *avango.gua.make_scale_mat(2)
        self.countdown_box_scooterloose.Material.value.set_uniform("ColorMap", "data/textures/countdown_textures/kawaiicountdownLOOSER.png")
        self.countdown_box_scooterloose.Material.value.set_uniform("Color", avango.gua.Vec4(1,1,1,0))
        self.scooter_transform.Children.value.append(self.countdown_box_scooterloose)

    def getSkateboard(self):
        return self.skate_transform

    def getScooter(self):
        return self.scooter_transform