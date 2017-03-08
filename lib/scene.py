import avango
import avango.script
import avango.gua
from lib.GuaVe import GuaVE

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

        skate_transform = avango.gua.nodes.TransformNode()
        skateboard = loader.create_geometry_from_file("kawaii_skateboard", "data/skateboard/kawaii_skateboard.obj", avango.gua.LoaderFlags.DEFAULTS)
        #skateboard.Material.value.set_uniform("Color", avango.gua.Vec4(1.0,0.153,1.0,1.0))
        skate_transform.Children.value.append(skateboard)
        skate_transform.Transform.value = avango.gua.make_scale_mat(0.025)
        graph.Root.value.Children.value.append(skate_transform)

        for _node in skateboard.Children.value:
            _node.Material.value.set_uniform("Emissivity", 0.20) # 20% self-lighting
            _node.Material.value.EnableBackfaceCulling.value = False
            _node.Material.value.set_uniform("Color", avango.gua.Vec4(1.0,0.153,1.0,1.0))

        bike_transform = avango.gua.nodes.TransformNode()
        bike = loader.create_geometry_from_file("kawaii_bike", "data/bike/kawaii_bike.obj", avango.gua.LoaderFlags.DEFAULTS)
        bike_transform.Children.value.append(bike)
        bike_transform.Transform.value = avango.gua.make_scale_mat(0.025)
        graph.Root.value.Children.value.append(bike_transform)

        for _node in bike.Children.value:
            _node.Material.value.set_uniform("Emissivity", 0.20) # 20% self-lighting
            _node.Material.value.EnableBackfaceCulling.value = False
            _node.Material.value.set_uniform("Color", avango.gua.Vec4(0.0,1.0,1.0,1.0))