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
        return self._ids
    
    def get_invscales_type(self):
        return self._invscales_type

    def get_shapes_type(self):
        return self._shapes_type

    def get_R(self):
        return self._R

    def set_ids(self, ids):
        self._ids = ids
    
    def set_invscales_type(self, invscales_type):
        self._invscales_type = invscales_type

    def set_shapes_type(self, shapes_type):
        self._shapes_type = shapes_type

    def set_R(self, R):
        self._R = R

    def get_num_substrokes(self):
        return len(self._ids)

    def get_motor_spline(self):
        pass

    @staticmethod
    def loadobj(X):
        return copy.deepcopy(X)

    @staticmethod
    def needs_update(_, event):
        event.AffectedObject.cache_current = False
