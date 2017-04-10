import avango
import avango.gua
import avango.script
from avango.script import field_has_changed
from lib.Intersection import Intersection

import time

class GroundFollowing(avango.script.Script):

    ## input fields
    sf_mat = avango.gua.SFMatrix4()

    ## ouput fields
    sf_modified_mat = avango.gua.SFMatrix4()

    ## internal fields
    mf_pick_result_down = avango.gua.MFPickResult()
    mf_pick_result_front = avango.gua.MFPickResult()
    mf_pick_result_left = avango.gua.MFPickResult()
    mf_pick_result_right = avango.gua.MFPickResult()


    ## constructor
    def __init__(self):
        self.super(GroundFollowing).__init__()


    def my_constructor(self,
        SCENEGRAPH = None,
        START_MATRIX = avango.gua.make_identity_mat(),
        ):

        ### parameters ###
        self.fall_velocity = 0.003 # in meter/sec

        self.pick_length = 100.0 # in meter
        self.pick_direction_y_down = avango.gua.Vec3(0.0,-1.0,0.0)
        self.pick_direction_z_front = avango.gua.Vec3(0.0,0.0,-1.0)
        self.pick_direction_x_left = avango.gua.Vec3(-1.0, 0.0, 0.0)
        self.pick_direction_x_right = avango.gua.Vec3(1.0,0.0,0.0)


        ### variables ###
        self.fall_vec = avango.gua.Vec3()

        self.rising_vec = avango.gua.Vec3()

        self.lf_time = time.time()

        self.has_failed = False

        self.sf_mat.value = START_MATRIX

        self.hit_wall = False

        ## init internal sub-classes
        self.gravity_intersection_down = Intersection()
        self.gravity_intersection_down.my_constructor(SCENEGRAPH, self.sf_mat, self.pick_length, self.pick_direction_y_down)

        self.gravity_intersection_front = Intersection()
        self.gravity_intersection_front.my_constructor(SCENEGRAPH, self.sf_mat, self.pick_length, self.pick_direction_z_front)

        self.gravity_intersection_left = Intersection()
        self.gravity_intersection_left.my_constructor(SCENEGRAPH, self.sf_mat, self.pick_length, self.pick_direction_x_left)

        self.gravity_intersection_right = Intersection()
        self.gravity_intersection_right.my_constructor(SCENEGRAPH, self.sf_mat, self.pick_length, self.pick_direction_x_right)

        ## init field connections
        self.mf_pick_result_down.connect_from(self.gravity_intersection_down.mf_pick_result)
        self.mf_pick_result_front.connect_from(self.gravity_intersection_front.mf_pick_result)
        self.mf_pick_result_left.connect_from(self.gravity_intersection_left.mf_pick_result)
        self.mf_pick_result_right.connect_from(self.gravity_intersection_right.mf_pick_result)
        #self.mf_pick_result_up.connect_from(self.gravity_intersection_up.mf_pick_result)

        ## set initial state  
        self.sf_modified_mat.value = START_MATRIX

        self.always_evaluate(True)
        

    ###  callback functions ###
    def evaluate(self): # evaluated once every frame if any input field has changed

        self.lf_time = time.time() # save absolute time of last frame (required for frame-rate independent mapping)
        if len(self.mf_pick_result_down.value) > 0: # intersection found
            ## compute gravity response
            _pick_result_down = self.mf_pick_result_down.value[0] # get first intersection target from list
            _world_pos = _pick_result_down.WorldPosition.value
            _distance = (self.sf_mat.value.get_translate() - _world_pos).length()
            _distance -= 0.1 # subtract half avatar height from distance
            _distance -= self.fall_velocity

            #print("down distance:",_distance)

            if _distance > 0.01: # avatar above ground
                print("hit ground")
                self.fall_vec.y = self.fall_velocity * -1.0
                self.sf_modified_mat.value = \
                    avango.gua.make_trans_mat(self.fall_vec) * \
                    self.sf_mat.value

            else: # avatar (almost) on ground
                self.fall_vec.y = 0.0
        else: # no intersection found
            self.sf_modified_mat.value = self.sf_mat.value # no changes needed

        if len(self.mf_pick_result_front.value) > 0:
            _pick_result_front = self.mf_pick_result_front.value[0]
            _world_pos = _pick_result_front.WorldPosition.value
            _distance = (self.sf_mat.value.get_translate() - _world_pos).length()
            _distance -= 0.2 # subtract half avatar height from distance
            _distance -= self.fall_velocity

            #print("front distance:",_distance)

            if _distance < -0.01: # avatar above ground
                self.hit_wall = True
                print("hit front")
                #print("True")

            else: # avatar (almost) on ground
                self.hit_wall = False
                #print("False")

        #if len(self.mf_pick_result_left.value) > 0:
        #    _pick_result_left = self.mf_pick_result_left.value[0]
        #    _world_pos = _pick_result_left.WorldPosition.value
        #    _distance = (self.sf_mat.value.get_translate() - _world_pos).length()
        #    _distance -= 0.2 # subtract half avatar height from distance
        #    _distance -= self.fall_velocity

        #    #print("left distance:",_distance)

        #    if _distance < -0.01: # avatar above ground
        #        self.hit_wall = True
        #        print("hit left")
                #print("True")
#
        #    else: # avatar (almost) on ground
        #        self.hit_wall = False
                #print("False")
#
        #if len(self.mf_pick_result_right.value) > 0:
        #    _pick_result_right = self.mf_pick_result_right.value[0]
        #    _world_pos = _pick_result_right.WorldPosition.value
        #    _distance = (self.sf_mat.value.get_translate() - _world_pos).length()
        #    _distance -= 0.2 # subtract half avatar height from distance
        #    _distance -= self.fall_velocity

        #    #print("left distance:",_distance)

        #    if _distance < -0.01: # avatar above ground
        #        self.hit_wall = True
        #        print("hit right")
        #        #print("True")
#
        #    else: # avatar (almost) on ground
        #        self.hit_wall = False
        #        #print("False")
            

    def get_hit_wall(self):
        return self.hit_wall
