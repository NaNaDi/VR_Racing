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
    mf_pick_result_up = avango.gua.MFPickResult()


    ## constructor
    def __init__(self):
        self.super(GroundFollowing).__init__()


    def my_constructor(self,
        SCENEGRAPH = None,
        START_MATRIX = avango.gua.make_identity_mat(),
        ):

        ### parameters ###
        self.fall_velocity = 0.00003 # in meter/sec

        self.pick_length = 100.0 # in meter
        self.pick_direction_y_down = avango.gua.Vec3(0.0,-1.0,0.0)
        self.pick_direction_y_up = avango.gua.Vec3(0.0,1.0,0.0)


        ### variables ###
        self.fall_vec = avango.gua.Vec3()

        self.rising_vec = avango.gua.Vec3()

        self.lf_time = time.time()

        self.has_failed = False

        self.sf_mat.value = START_MATRIX

        ## init internal sub-classes
        self.gravity_intersection_down = Intersection()
        self.gravity_intersection_down.my_constructor(SCENEGRAPH, self.sf_mat, self.pick_length, self.pick_direction_y_down)

        #self.gravity_intersection_up = Intersection()
        #self.gravity_intersection_up.my_constructor(SCENEGRAPH, self.sf_mat, self.pick_length, self.pick_direction_y_up)

        ## init field connections
        self.mf_pick_result_down.connect_from(self.gravity_intersection_down.mf_pick_result)
        #self.mf_pick_result_up.connect_from(self.gravity_intersection_up.mf_pick_result)

        ## set initial state  
        self.sf_modified_mat.value = START_MATRIX

        self.always_evaluate(True)
        

    ###  callback functions ###
    def evaluate(self): # evaluated once every frame if any input field has changed

        self.lf_time = time.time() # save absolute time of last frame (required for frame-rate independent mapping)
        if len(self.mf_pick_result_down.value) > 0 and len(self.mf_pick_result_up.value) == 0: # intersection found
            ## compute gravity response
            _pick_result_down = self.mf_pick_result_down.value[0] # get first intersection target from list
            #print("down", len(self.mf_pick_result_down.value))
            #print("down", _pick_result_down.WorldPosition.value)
            #_distance = _pick_result_down.Distance.value # distance from ray matrix to intersection point
            _world_pos = _pick_result_down.WorldPosition.value
            _distance = (self.sf_mat.value.get_translate() - _world_pos).length()
            _distance -= 0.02 # subtract half avatar height from distance
            _distance -= self.fall_velocity

            print("down distance:",_distance)

            if _distance > 0.01: # avatar above ground
                self.fall_vec.y = self.fall_velocity * -1.0
                print("down fall_vec.y", self.fall_vec.y)
                self.sf_modified_mat.value = \
                    avango.gua.make_trans_mat(self.fall_vec) * \
                    self.sf_mat.value

            else: # avatar (almost) on ground
                self.fall_vec.y = 0.0
                print("You failed")
            
            #print(self.fall_vec)

            

            print(self.sf_modified_mat.value)

        #elif len(self.mf_pick_result_up.value) > 1: # intersection found
        #    ## compute gravity response
        #    _pick_result_up = self.mf_pick_result_up.value[1] # get first intersection target from list
        #    #print("up", len(self.mf_pick_result_up.value))
        #    #print("up", _pick_result_up.WorldPosition.value)
        #    _distance = _pick_result_up.Distance.value # distance from ray matrix to intersection point
        #    _distance += 0.025 # subtract half avatar height from distance
        #    _distance += self.fall_velocity
#
        #    print("up distance:",_distance)
#
        #    if _distance > 0.01: # avatar above ground
         #       self.rising_vec.y = self.fall_velocity
#
        #    else: # avatar (almost) on ground
        #        self.rising_vec.y = 0.0
            
        #    #print(self.rising_vec)

        #    self.sf_modified_mat.value = \
        #        avango.gua.make_trans_mat(self.rising_vec) * \
        #        self.sf_mat.value              
            
        else: # no intersection found
            self.sf_modified_mat.value = self.sf_mat.value # no changes needed