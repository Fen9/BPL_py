import copy

class stroke():
    def __init__(self):
        self._my_type
        self._lh
        self._R
        self._ids
        self._invscales_type
        self._shapes_type
        self._pos_token
        self._invscale_token
        self._shapes_token
        self._nsub
        self._motor
        self._motor_spline
        self._cache_current
        self._cache_motor
        self._cache_motor_spline
        self._cache_current = False
        self._cache_motor
        self._cache_motor_spline
        self._eval_spot_token
        self._po

    def load_legacy(self, oldS):
        self._my_type = copy.deepcopy(oldS._my_type)
        self._pos_token = copy.deepcopy(oldS._pos_token)
        self._invscale_token = copy.deepcopy(oldS._invscale_token)
        self._shapes_token = copy.deepcopy(oldS._shapes_token)

    def get_ids(self):
        if self._ids == None:
            self._ids = copy.deepcopy(self._my_type._ids)
        out = self._ids
        return out
    
    def get_invscales_type(self):
        if self._invscales_type == None:
            self._invscales_type = copy.deepcopy(self._my_type.invscales_type)
        out = self._invscales_type
        return out

    def get_shapes_type(self):
        if self._shapes_type == None:
            self._shapes_type = copy.deepcopy(self._my_type._shapes_type)
        out = self._shapes_type
        return out

    def get_R(self):
        if self._R == None:
            self._R = copy.deepcopy(self._my_type._R)
        out = self._R
        if len(self._R) == 0 and self._my_type._R._type == 'mid':
            out._eval_spot_token = copy.deepcopy(self._eval_spot_token)
        return out

    def set_ids(self, ids):
        self._my_type._ids = ids
    
    def set_invscales_type(self, invscales_type):
        self._my_type._invscales_type = invscales_type

    def set_shapes_type(self, shapes_type):
        self._my_type._shapes_type = shapes_type

    def set_R(self, R):
        self._my_type._R = R
        if len(self._my_type._R) == 0 and self._my_type._R._type == 'mid':
            self._my_type._R._eval_spot_token = []
            self._eval_spot_token = R._eval_spot_token

    def get_num_substrokes(self):
        return len(self._ids)

    def get_motor(self):
        motor = None
        if self._cache_current:
            motor = self._cache_motor
        else:
            motor, motor_spline = vanilla_to_motor(self._shapes_token, self._invscales_token, self._pos_token)
            self._cache_motor = motor
            self._cache_motor_spline = motor_spline
            self._cache_current = True
        return motor

    def get_motor_spline(self):
        motor_spline = None
        if self._cache_current:
            motor_spline = self._cache_motor_spline
        else:
            motor, motor_spline = vanilla_to_motor(self._shapes_token, self._invscales_token, self._pos_token)
            self._cache_motor = motor
            self._cache_motor_spline = motor_spline
            self._cache_current = True
        return motor

    def get_eval_spot_token(self):
        out = self._eval_spot_token
        return out

    def on_listener(self):
        pass

    def save_obj(self):
        pass

    @staticmethod
    def loadobj(X):
        return copy.deepcopy(X)

    @staticmethod
    def needs_update(_, event):
        event.AffectedObject.cache_current = False


def vanilla_to_motor(vanilla_shapes, invscales, firest_ops):
    if np.all(vanilla_shapes==0) or np.all(invscales == 0) or np.all(first_ops==0):
        motor = []
        motor_spline = []
        return motor, motor_spline

        ncpt, _, n = vanilla_shapes.shape
        for i in range(0, n):
            vanilla_shapes[:,:,i] = invscales[i] * vanilla_shapes[:,:i]

        vanilla_traj = np.array((n, 1))