from stroke.stroke import stroke
import numpy as np
import UtilMP as UtilMP

class motor_program():
    def __init__(self, args):
        if type(args) == int:
            pass

        self._image = None
        self._strokes = None
        self._fixed_parameters = None
        self._listener_handle = None
        self._epsilon = None
        self._blur_sigma = None
        self._affine_transformation = None
        self._num_strokes = None
        self._prob_img = None
        self._ink_off_page = None
        self._motor = None
        self._motor_warped = None
        self._cache_grand_current = None
        self._cache_noise_current = False
        self._cache_prob_img_motor = None
        self._cache_prob_img = None
        self._cache_ink_off_page = None

    #

    # oldMP -> newMP
    def load_legacy(self, oldMP):
        self._image = oldMP._image
        self._fixed_parameters = oldMP._fixed_parameters
        self._epsilon = oldMP._epsilon
        self._blur_sigma = oldMP._blur_sigma
        self._affine_transformation = oldMP._affine_transformation
        self._strokes = oldMP._strokes
        for i in range(self._num_strokes):
            self._strokes[i] = stroke()
            self._strokes[i].load_legacy(oldMP._strokes[i])

    # selective deep copy
    def copy_element(self):
        pass

    # get number of strokes
    def get_num_strokes(self):
        self._num_strokes = len(self._strokes)
        return self._num_strokes
    
    # get pen trajectory (un-warped)
    def get_motor(self):
        ns = get_num_strokes()
        self._motor = []
        for i in range(ns):
            self._motor.append(self._strokes[i]._motor)
        return self._motor

    # get pen trajectory (warped)
    def get_motor_warped(self):
        self._motor_warped = apply_warp(self)
        return self._motor_warped

    # get probability map of image
    def get_prob_img(self):
        if self.get_cache_grand_current(self):
            self._prob_img = self._cache_prob_img
        else:
            result = apply_render(self)
            self._prob_img = result[0]
            self._ink_off_page = result[1]
            self._cache_prob_img = self._prob_img
            self._cache_ink_off_page = self._ink_off_page
            self._cache_prob_img_motor = self._motor
            self._cache_noise_current = True

    # is there ink off of the page?
    def get_ink_off_page(self):
        if get_cache_grand_current(self):
            self._ink_off_page = self._cache_ink_off_page
        else:
            result = apply_render(self)
            self._prob_img = result[0]
            self._ink_off_page = result[1]
            self._cache_prob_img = self._prob_img
            self._cache_ink_off_page = self._ink_off_page
            self._cache_prob_img_motor = self._motor
            self._cache_noise_current = True

    # is the cache is up to date
    def get_cache_grand_current(self):
        out = self._cache_noise_current
        return (out and (self._cache_prob_img_motor == self._motor))
        
    # helper function
    def all_same(present):
        item = present[0]
        allsame = True
        for i in range(len(item)):
            if item != present[i]:
                allsame = False
                break
        return allsame

    # return true if all the relations (in list_sid) are set and non-empty
    def has_relations(self, list_sid):
        if list_sid is None:
            list_sid = [i for i in range(self._num_strokes)]
        
        present = [False for i in range(len[list_sid])]
        count = 0
        for i in list_sid:
            present[count] = self._strokes[i]._R is not None
            count += 1

        if not (allSame(present)):
            print("error, all relaions should be present or not")

        return present[0]

    # set all relations to the empty relation
    def clear_relations(self):
        for i in range(self._num_strokes):
            self._strokes[i]._R = None

    # remove memory-heavy image matrices from the class
    def lightweight(self):
        self._cache_prob_img = None
        self._image = None
        self._cache_noise_current = False

    def clear_shape_type(self):
        for i in range(self._num_strokes):
            self._strokes[i]._shape_type = None
    


    # apply affine transformation to the stroke trajectories
    # and return a nested cell aray
    def apply_warp(self):
        motor_unwarped = self._motor
        if np.all(self._affine_transformation) == 0:
            motor_warped = motor_unwarped
            return
        
        cell_traj = UtilMP.flatten_substrokes(motor_unwarped)
        com = com_char(cell_traj)
        B = np.zeros(4)
        B[0:2] = self._affine_transformation[0:2]
        b[2:4] = (self._affine_transformation[2:4] - self._affine_transformation[0:2]) * com
        motor_warped = UtilMP.apply_each_substroke(motor_unwarped, self.affine_warp)
        return motor_warped


    # Affine warp defined by
    # A(1) * [x y] + [A(2) A(3)]
    # OR
    # A(1:2) .* [x y] + [A(3) A(4)]
    # 
    # Input
    # stk [n x 2] stroke
    # A : [3x1 or 4x1] affine warp
    @staticmethod
    def affine_warp(stk, affine):
        n = stk.shape[0]
        if affine.shape[0] == 3:
            stk = affine[0] * stk
            stk = stk + affine[1:3]
        else:
            stk = affine[0:1] * stk
            stk = stk + affine[2:4]


    # apply affine warp and render the image 
    def apply_render(self):
        self._motor_warped = apply_warp(self)
        flat_warped = UtilMP.flatten_substrokes(self._motor_warped)
        result = render_image(flat_warped, self._epsilon, self._blur_sigma, self._fixed_parameters)
        pimg = result[0]
        ink_off_page = result[1]
        return result
    