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
