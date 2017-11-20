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
import math

class Server(avango.script.Script):

    trans_mat = avango.avango.gua.SFMatrix4()
    scooter_trans_mat = avango.avango.gua.SFMatrix4()
    ground_following_vertical_mat = avango.avango.gua.SFMatrix4()
    scooter_ground_following_vertical_mat = avango.avango.gua.SFMatrix4()
    #TimeIn = avango.SFFloat()

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
        self.scooter_old_rotation = avango.gua.Quat()
        self.old_leg_pos = 0.0
        self.scooter_old_leg_pos = 0.0

        #self.navigation = Navigation()

        self.navigation_node = avango.gua.nodes.TransformNode()

        self.velocity = 0.0
        self.scooter_velocity = 0.0

        self.scooter_first = False
        self.scooter_second = False

        self.skate_first = False
        self.skate_second = False

        self.scooter_mode = 0 # 0 = start; 1 = first half; 2 = second half; 3 = finish
        self.skate_mode = 0

        #self.rotation_offset = avango.gua.make_rot_mat(90,0,1,0)

        ## init server viewing setup
        self.serverViewingSetup = SimpleViewingSetup(
            SCENEGRAPH = self.scenegraph,
            WINDOW_RESOLUTION = avango.gua.Vec2ui(1200, 1200),
            SCREEN_DIMENSIONS = avango.gua.Vec2(100.0, 120.0),
            NAVIGATION_MATRIX = \
                avango.gua.make_trans_mat(0.0,30.0,0.0) * \
                avango.gua.make_rot_mat(90.0,-1,0,0),
            PROJECTION_MODE = avango.gua.ProjectionMode.ORTHOGRAPHIC,
            )
        #self.serverViewingSetup.camera_node.Transform.value *= avango.gua.make_trans_mat(30, 0, 0)


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

        self.scooter_sensor = avango.daemon.nodes.DeviceSensor(DeviceService = avango.daemon.DeviceService())
        self.scooter_sensor.Station.value = "scooter_pointer"

        self.scooter_leg_sensor = avango.daemon.nodes.DeviceSensor(DeviceService = avango.daemon.DeviceService())
        self.scooter_leg_sensor.Station.value = "scooter_leg_pointer"

        ## init scene
        self.scene = Scene(PARENT_NODE = self.nettrans)
        self.finish_position = self.scene.finish_line.WorldTransform.value.get_translate().x

        self.inter_diff_front = 0.0
        self.inter_diff_left = 0.0
        self.inter_diff_right = 0.0

        self.scooter_old_position = avango.gua.make_identity_mat()
        self.track_counter = 0

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
        #print(self.skate_trans.Transform.value.get_translate())
        self.groundFollowing.my_constructor(SCENEGRAPH = self.scenegraph, START_MATRIX = avango.gua.make_trans_mat(self.skate_trans.Transform.value.get_translate()))
        self.ground_following_vertical_mat.connect_from(self.groundFollowing.sf_modified_mat)
        #skate_acceleration.my_constructor(PARENT_NODE = self.nettrans, LEG_NODE = self.skate_trans)

        ## scooter ground following
        self.scooter_trans = self.scene.getScooter()
        self.scooter_trans_mat.connect_from(self.scooter_sensor.Matrix)
        self.scooter_groundFollowing = GroundFollowing()
        self.scooter_groundFollowing.my_constructor(SCENEGRAPH = self.scenegraph, START_MATRIX = avango.gua.make_trans_mat(self.scooter_trans.Transform.value.get_translate()))
        self.scooter_ground_following_vertical_mat.connect_from(self.scooter_groundFollowing.sf_modified_mat)


        self.timer = avango.nodes.TimeSensor()

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

    def detect_finish(self, _finish_position, _object_position, _mode):
        if _object_position < _finish_position:
            if _mode == 0:
                _mode = 1
            elif _mode == 2:
                _mode = 3
        if _object_position > _finish_position:
            if _mode == 1:
                _mode = 2
        #print("mode: ", _mode)
        return _mode

    def is_on_track(self, _object, _intersection_world_y):
        print("diff:", _object.WorldTransform.value.get_translate().y - _intersection_world_y)
        if (_object.WorldTransform.value.get_translate().y - _intersection_world_y) < 2.5:
            if self.track_counter == 50 and self.groundFollowing.get_hit_wall_front() == False and self.groundFollowing.get_hit_wall_left() == False and self.groundFollowing.get_hit_wall_right() == False:
                self.scooter_old_position = _object.Transform.value
                self.track_counter = 0
            else:
                self.track_counter += 1
            return True
        else:
            print("is not on track")
            self.velocity = 0.0
            _object.Transform.value = self.scooter_old_position
            return False

    def evaluate(self):
        #print("time: ", self.timer.Time.value)
        leg_pos = self.leg_sensor.Matrix.value.get_translate().z
        scooter_leg_pos = self.scooter_leg_sensor.Matrix.value.get_translate().z
        #always keep updating skateboard position for ground following
        self.groundFollowing.sf_mat.value = self.skate_trans.Transform.value
        self.scooter_groundFollowing.sf_mat.value = self.scooter_trans.Transform.value
        ##todo: ground following
        #self.skate_trans.Transform.value *= self.ground_following_vertical_mat.value
        #print(self.ground_following_vertical_mat.value)
        if len(self.groundFollowing.mf_pick_result_front.value) > 0:
            _intersection = self.groundFollowing.mf_pick_result_front.value[0].WorldPosition.value
            _inter_diff = _intersection.z - self.skate_trans.WorldTransform.value.get_translate().z
            if (_inter_diff - self.velocity) > 0:
                self.skate_trans.Transform.value *= avango.gua.make_trans_mat(0,0,_inter_diff)
                self.velocity = 0.0
        if self.groundFollowing.get_hit_wall_front() == False and self.groundFollowing.get_hit_wall_left() == False and self.groundFollowing.get_hit_wall_right() == False:
            if leg_pos<self.old_leg_pos:
                self.old_leg_pos=leg_pos
            if leg_pos<0.1 and leg_pos>-0.1 and self.old_leg_pos != 0.0 and self.old_leg_pos < -0.1:
                #self.skate_trans.Transform.value += avango.gua.make_trans_mat(0,0,self.old_leg_pos)
                self.velocity += self.old_leg_pos
                self.old_leg_pos=0.0
            if self.velocity < 0.0:
                self.skate_trans.Transform.value *= avango.gua.make_trans_mat(0,0,self.velocity*0.1)
                self.velocity += 0.0000005
            else:
                self.velocity = 0.0
        #elif self.groundFollowing.get_hit_wall_front:
        #    self.skate_trans.Transform.value *= avango.gua.make_trans_mat(0,0,0.2)
        #    self.velocity = 0.0
        #elif self.groundFollowing.get_hit_wall_right:
        #    self.skate_trans.Transform.value *= avango.gua.make_trans_mat(0.2,0,0)
        #    self.velocity = 0.0
        #elif self.groundFollowing.get_hit_wall_left:
        #    self.skate_trans.Transform.value *= avango.gua.make_trans_mat(-0.2, 0, 0)
        #    self.velocity = 0.0
        print(len(self.scooter_groundFollowing.mf_pick_result_down.value))
        if len(self.scooter_groundFollowing.mf_pick_result_down.value)>0:
            print("pick result down")
            if self.is_on_track(self.scooter_trans, self.scooter_groundFollowing.mf_pick_result_down.value[0].WorldPosition.value.y):
                print("is on track")
                ## scooter navigation
                if len(self.scooter_groundFollowing.mf_pick_result_front.value) > 0:
                    _intersection = self.scooter_groundFollowing.mf_pick_result_front.value[0].WorldPosition.value ## get the pick result to the front
                    _scooter_world_x = self.scooter_trans.Transform.value.get_translate().x
                    _scooter_world_z = self.scooter_trans.Transform.value.get_translate().z
                    self.inter_diff_front = math.sqrt(math.pow((_scooter_world_x - _intersection.x), 2) + math.pow((_scooter_world_z - _intersection.z), 2)) * 0.75
                    #print("inter_diff_front: ", self.inter_diff_front)
                    #_inter_diff = _intersection.z - self.scooter_trans.Transform.value.get_translate().z
                    #_inter_diff = self.scooter_groundFollowing.get_distance()
                    #print("inter_diff", _inter_diff)
                    #print("velocity", self.velocity)
                    if (self.inter_diff_front - self.velocity) <= 0 and self.velocity > 0:
                        print("velocity is greater than inter_diff_front")
                        self.scooter_trans.Transform.value *= avango.gua.make_trans_mat(0,0,_inter_diff * -1)
                        self.scooter_velocity = 0.0
                #else:
                #    print("Oh no! How could this happen?  front :O")
                #    print("velocity: ", self.velocity)
                #    self.scooter_trans.Transform.value *= avango.gua.make_trans_mat(0,0,0.25)
                #    self.scooter_velocity = 0.0
                if len(self.scooter_groundFollowing.mf_pick_result_left.value) > 0:
                    _intersection = self.scooter_groundFollowing.mf_pick_result_left.value[0].WorldPosition.value ## get the pick result to the front
                    _scooter_world_x = self.scooter_trans.Transform.value.get_translate().x
                    _scooter_world_z = self.scooter_trans.Transform.value.get_translate().z
                    self.inter_diff_left = math.sqrt(math.pow((_scooter_world_x - _intersection.x), 2) + math.pow((_scooter_world_z - _intersection.z), 2)) * 0.75
                    #print("inter_diff_left: ", self.inter_diff_left)
                    #_inter_diff = _intersection.z - self.scooter_trans.Transform.value.get_translate().z
                    #_inter_diff = self.scooter_groundFollowing.get_distance()
                    #print("inter_diff", _inter_diff)
                    #print("velocity", self.velocity)
                    #if (self.inter_diff_left - self.velocity) <= 0 and self.velocity > 0:
                    #    print("velocity is greater than inter_diff_left")
                    #    self.scooter_trans.Transform.value *= avango.gua.make_trans_mat(_inter_diff,0,0)
                    #    self.scooter_velocity = 0.0
                #else:
                #    print("Oh no! How could this happen? left :O")
                #    print("velocity: ", self.velocity)
                #    self.scooter_trans.Transform.value *= avango.gua.make_trans_mat(0,0,0.25)
                #    self.scooter_velocity = 0.0
                if len(self.scooter_groundFollowing.mf_pick_result_right.value) > 0:
                    _intersection = self.scooter_groundFollowing.mf_pick_result_right.value[0].WorldPosition.value ## get the pick result to the front
                    _scooter_world_x = self.scooter_trans.Transform.value.get_translate().x
                    _scooter_world_z = self.scooter_trans.Transform.value.get_translate().z
                    self.inter_diff_right = math.sqrt(math.pow((_scooter_world_x - _intersection.x), 2) + math.pow((_scooter_world_z - _intersection.z), 2)) * 0.75
                    #print("inter_diff_right: ", self.inter_diff_right)
                    #_inter_diff = _intersection.z - self.scooter_trans.Transform.value.get_translate().z
                    #_inter_diff = self.scooter_groundFollowing.get_distance()
                    #print("inter_diff", _inter_diff)
                    #print("velocity", self.velocity)
                    #if (self.inter_diff_right - self.velocity) <= 0 and self.velocity > 0:
                    #    print("velocity is greater than inter_diff_right")
                    #    self.scooter_trans.Transform.value *= avango.gua.make_trans_mat(_inter_diff * -1,0,0)
                    #    self.scooter_velocity = 0.0
                #else:
                #    print("Oh no! How could this happen? right :O")
                #    print("velocity: ", self.velocity)
                #    self.scooter_trans.Transform.value *= avango.gua.make_trans_mat(0,0,0.25)
                #    self.scooter_velocity = 0.0

                #print("hit_front: ", self.scooter_groundFollowing.get_hit_wall_front())
                #print("hit_left: ", self.scooter_groundFollowing.get_hit_wall_left())
                #print("hit_right: ", self.scooter_groundFollowing.get_hit_wall_right())
                if self.scooter_groundFollowing.get_hit_wall_front() == False and self.scooter_groundFollowing.get_hit_wall_right() == False and self.scooter_groundFollowing.get_hit_wall_left() == False:
                    #print("no wall hit")
                    if self.inter_diff_front <= 15 or self.inter_diff_front >= -15:
                        #print("inter diff front below threshold") 
                        #self.scooter_trans.Transform.value *= avango.gua.make_trans_mat(0,0, -_inter_diff * 1.25)
                        if scooter_leg_pos<self.scooter_old_leg_pos:
                            self.scooter_old_leg_pos=scooter_leg_pos
                        if scooter_leg_pos<0.1 and scooter_leg_pos>-0.1  and self.scooter_old_leg_pos != 0.0  and self.scooter_old_leg_pos < -0.1:
                            self.scooter_velocity += self.scooter_old_leg_pos *-0.5
                            self.scooter_old_leg_pos=0.0
                        if self.scooter_velocity > 0.0:
                            self.scooter_trans.Transform.value *= avango.gua.make_trans_mat(0,0,self.scooter_velocity*-0.3)
                            self.scooter_velocity -= 0.000005
                        else:
                            self.scooter_velocity = 0.0
                    else:
                        #print("inter diff front above threshold")
                        self.scooter_trans.Transform.value *= avango.gua.make_trans_mat(0,0,0.75)
                elif self.scooter_groundFollowing.get_hit_wall_front():
                    ## wall hit
                    #print("oh no, we hit the wall")
                    self.scooter_trans.Transform.value *= avango.gua.make_rot_mat(180, 0, 1, 0)

                    #print("backwards intersection")
                    if len(self.scooter_groundFollowing.mf_pick_result_front.value) > 0:
                        #print("Yaayy pick result")
                        _intersection = self.scooter_groundFollowing.mf_pick_result_front.value[0].WorldPosition.value ## get the pick result to the front
                        _scooter_world_x = self.scooter_trans.Transform.value.get_translate().x
                        _scooter_world_z = self.scooter_trans.Transform.value.get_translate().z
                        self.inter_diff_front = math.sqrt(math.pow((_scooter_world_x - _intersection.x), 2) + math.pow((_scooter_world_z - _intersection.z), 2)) * 0.75
                        #print("go backwards", self.inter_diff_front)
                        #_inter_diff = self.scooter_groundFollowing.get_distance()
                        if self.inter_diff_front <= 10 or self.inter_diff_front >= -10: 
                            #print("pick result and threshold is fine for going backwards")
                            self.scooter_trans.Transform.value *= avango.gua.make_trans_mat(0,0, -self.inter_diff_front * 1.25)
                        else:
                            #print("pick result but threshold is not fine for going backwards")
                            self.scooter_trans.Transform.value *= avango.gua.make_trans_mat(0,0,-0.75)
                    else:
                        ##no pick result
                        print("no pick result but wall hit :(")
                        self.scooter_trans.Transform.value *= avango.gua.make_trans_mat(0,0,-0.25)
                    self.scooter_trans.Transform.value *= avango.gua.make_rot_mat(180, 0, 1, 0)
                    self.scooter_velocity = 0.0

                elif self.scooter_groundFollowing.get_hit_wall_right():
                    self.scooter_trans.Transform.value *= avango.gua.make_trans_mat(-0.25,0,0)
                    self.scooter_velocity = 0.0

                elif self.scooter_groundFollowing.get_hit_wall_left():
                    self.scooter_trans.Transform.value *= avango.gua.make_trans_mat(0.25,0,0)
                    self.scooter_velocity = 0.0



                self.scooter_mode = self.detect_finish(self.finish_position, self.scooter_trans.WorldTransform.value.get_translate().x, self.scooter_mode)
                self.skate_mode = self.detect_finish(self.finish_position, self.skate_trans.WorldTransform.value.get_translate().x, self.skate_mode)
                _is_scooter_finish = False
                if self.scooter_mode == 3:
                    _is_scooter_finish = True
                if _is_scooter_finish:
                    if not self.skate_first:
                        self.scooter_first = True
                        print("##################Yuuuhuuuu!!!###########")
                        print("time: ", self.timer.Time.value)
                    else:
                        print("------------------Buuuuuuuuuh!!!------------")
                        print("time: ", self.timer.Time.value)
                _is_skate_finish = False
                if self.skate_mode == 3:
                    _is_skate_finish = True
                if _is_skate_finish:
                    if not self.scooter_first:
                        print("##################Kawaii_Skate_Yuuuhuuuu!!!###########")
                        print("time: ", self.timer.Time.value)
                    else:
                        print("------------------Kawaii_Skate_Buuuuuuuuuh!!!------------")
                        print("time: ", self.timer.Time.value)


    @field_has_changed(trans_mat)
    def trans_mat_changed(self):
        _rot = self.trans_mat.value.get_rotate()
        _rot_y = self.old_rotation.y
        _rot_z = self.old_rotation.z
        #_rot_z = avango.gua.make_rot_mat(self.old_rotation.z, 0, 0, 1)
        #self.skate_trans.Transform.value *= avango.gua.make_inverse_mat(_rot_z)
        #self.skate_trans.Transform.value *= avango.gua.make_rot_mat(_rot.z, 0, 1, 0) * avango.gua.make_rot_mat(_rot.z, 0, 0, 1)
        self.skate_trans.Transform.value *= avango.gua.make_inverse_mat(avango.gua.make_rot_mat(_rot_z, 0, 1, 0))
        self.skate_trans.Transform.value *= avango.gua.make_rot_mat(_rot.z, 0, 1, 0)# * avango.gua.make_rot_mat(_rot.z, 0, 1, 0)# * avango.gua.make_rot_mat(_rot_y, 0, 1, 0)
        self.old_rotation = self.skate_trans.Transform.value.get_rotate()

    @field_has_changed(ground_following_vertical_mat)
    def ground_following_vertical_mat_changed(self):
        #pass
        _shift_y = self.ground_following_vertical_mat.value.get_translate().y
        if not math.isnan(_shift_y) and _shift_y<1.0 and _shift_y >-1.0:
            #print(self.skate_trans.Transform.value)
            #pass
            self.skate_trans.Transform.value *= avango.gua.make_trans_mat(0,_shift_y,0)
            #print(_shift_y)

    ##same for scooter
    @field_has_changed(scooter_trans_mat)
    def scooter_trans_mat_changed(self):
        _rot = self.scooter_trans_mat.value.get_rotate()
        _rot_y = self.scooter_old_rotation.y
        _rot_z = self.scooter_old_rotation.z

        #print(_rot.z)

        #_result = avango.gua.make_rot_mat(self.old_rotation.z, 0, 0, 1)
        #self.scooter_trans.Transform.value *= avango.gua.make_inverse_mat(avango.gua.make_rot_mat(_rot_z, 0, 1, 0))
        self.scooter_trans.Transform.value *= avango.gua.make_rot_mat(_rot.z, 0, 1, 0)# * avango.gua.make_rot_mat(_rot.z, 0, 0, 1)
        #self.scooter_trans.Transform.value *= avango.gua.make_inverse_mat(avango.gua.make_rot_mat(_result.Matrix.value.z, 0, 0, 1))
        ##

        #print("rotation: ", _rot.z)
        #if _rot.z > 0.1 or _rot.z < -0.1:
        #    self.scooter_trans.Transform.value *= avango.gua.make_inverse_mat(avango.gua.make_rot_mat(_rot_z, 0, 1, 0))
        #    self.scooter_trans.Transform.value *= avango.gua.make_rot_mat(_rot.z, 0, 1, 0)# * avango.gua.make_rot_mat(_rot_y, 0, 1, 0)
        #    self.scooter_old_rotation = self.scooter_trans.Transform.value.get_rotate()

        ##better rotation according to Tim
        #_sensor_trans = self.scooter_trans_mat.value.get_translate()
        #_sensor_shifted_trans = _sensor_trans * avango.gua.Vec3(0,1,0)
        #_trans_vector = _sensor_trans - _sensor_shifted_trans
        #print("c: ", 1-_trans_vector.y)
        #print("trans: ", _trans_vector.y)
        ##_result = math.acos(_sensor_trans.x * _trans_vector.x + _sensor_trans.z * _trans_vector.z)
        #_result = math.acos((2 - math.pow(1-_trans_vector.y,2)) / (2))
        
        # I have no idea what I'm doing here
        #print("_trans_vector.x: ",  math.acos((2 - math.pow(_trans_vector.x,2)) / (2)))
        #print("_trans_vector.y: ",  math.acos((2 - math.pow(_trans_vector.y,2)) / (2)))
        #print("_trans_vector.z: ",  math.acos((2 - math.pow(_trans_vector.z,2)) / (2)))

        #print("resulting angle: ", _result)

        ## put the whole shit on the rotation, yeah!
        #self.scooter_trans.Transform.value *= avango.gua.make_inverse_mat(avango.gua.make_rot_mat(_rot_z, 0, 1, 0))
        #self.scooter_trans.Transform.value *= avango.gua.make_rot_mat(_result, 0, 1, 0)
        self.scooter_old_rotation = self.scooter_trans.Transform.value.get_rotate()

    @field_has_changed(scooter_ground_following_vertical_mat)
    def scooter_ground_following_vertical_mat_changed(self):
        #pass
        _shift_y = self.scooter_ground_following_vertical_mat.value.get_translate().y
        if not math.isnan(_shift_y) and _shift_y<1.0 and _shift_y >-1.0:
            #print(self.skate_trans.Transform.value)
            #pass
            self.scooter_trans.Transform.value *= avango.gua.make_trans_mat(0,_shift_y,0)
            #print(_shift_y)



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
    #server.my_constructor(SERVER_IP = "141.54.147.32") # boreas
    #server.my_constructor(SERVER_IP = "141.54.147.49") # minos
    #server.my_constructor(SERVER_IP = "141.54.147.57") #orestes
    server.my_constructor(SERVER_IP = "141.54.147.45") #kronos
    #server.my_constructor(SERVER_IP = "141.54.147.28") #artemis
    #server.my_constructor(SERVER_IP = "141.54.147.27") #arachne


