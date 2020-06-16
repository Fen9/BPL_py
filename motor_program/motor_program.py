from stroke.stroke import stroke

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
        self._prob_pixel = None
        self._ink_off_page = None
        self._motor_warped = None
        self._cache_grand_current = None
        self._cache_noise_current = None
        self._cache_prob_pixel_motor = None
        self._cache_ink_off_page = None

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