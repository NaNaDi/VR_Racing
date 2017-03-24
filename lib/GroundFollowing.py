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
    mf_pick_result = avango.gua.MFPickResult()


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
        self.pick_direction = avango.gua.Vec3(0.0,-1.0,0.0)


        ### variables ###
        self.fall_vec = avango.gua.Vec3()

        self.lf_time = time.time()


        ## init internal sub-classes
        self.gravity_intersection = Intersection()
        self.gravity_intersection.my_constructor(SCENEGRAPH, self.sf_mat, self.pick_length, self.pick_direction)

        ## init field connections
        self.mf_pick_result.connect_from(self.gravity_intersection.mf_pick_result)

        ## set initial state  
        self.sf_modified_mat.value = START_MATRIX

        self.always_evaluate(True)
        

    ###  callback functions ###
    def evaluate(self): # evaluated once every frame if any input field has changed
    
        self.lf_time = time.time() # save absolute time of last frame (required for frame-rate independent mapping)
        #print(len(self.mf_pick_result.value))
        if len(self.mf_pick_result.value) > 0: # intersection found
            ## compute gravity response
            _pick_result = self.mf_pick_result.value[0] # get first intersection target from list
            print(_pick_result)
            _distance = _pick_result.Distance.value # distance from ray matrix to intersection point
            _distance -= 0.025 # subtract half avatar height from distance
            _distance -= self.fall_velocity

            if _distance > 0.01: # avatar above ground
                self.fall_vec.y = self.fall_velocity * -1.0

            else: # avatar (almost) on ground
                self.fall_vec.y = 0.0
            
            #print(self.fall_vec)

            self.sf_modified_mat.value = \
                avango.gua.make_trans_mat(self.fall_vec) * \
                self.sf_mat.value                
            
        else: # no intersection found
            self.sf_modified_mat.value = self.sf_mat.value # no changes needed