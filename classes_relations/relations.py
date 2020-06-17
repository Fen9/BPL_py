import spline.bspline as bspline
class relation():
    def __init__(self):
        self._type = ''
        self._num_prev
        self._types_allow = ['unihist','start','end','mid']

    def valid_type(self):
        out = None
        return out


class relation_attach(relation):
    def __init__(self):
        self._attach_spot
        self._type
        self._num_prev
    
    
class relation_attach_along(relation):
    def __init__(self):
        self._type = 'mid'
        self._nsub
        self._subid_spot
        self._num_prev
        self._eval_spot_type
        self._eval_spot_token

def getAttachPoint(r, previous_strokes):
    if r['type'] == 'unihist':
        return r['gpos']
    elif r['type'] == 'start':
        return previous_strokes[r['attach_spot']]._motor[0][0,:]
    elif r['type'] == 'end':
        return previous_strokes[r['attach_spot']]._motor[-1][-1,:]
    elif r['type'] == 'mid':
        bspline = previous_strokes[r['attach_spot']].motor_spline[: ,: ,r['subid_spot']]
        return bspline.bspline_eval(r['eval_spot_token'], bspline)

