import numpy as np

# cell_traj is a list, each element is a nx2 matrix representing points
def space_motor_to_img(cell_traj):
    traj_img = []
    for i in range(len(cell_traj)):
        cell_traj[i] = np.array(cell_traj[i])
        if cell_traj[i].shape[1] != 2:
            cell_traj[i] = np.transpose(cell_traj[i])
            t = np.transpose(np.array([-cell_traj[:,1], cell_traj[:,0]])) + 1
            traj_img.append(t)
    return traj_img

# renturn prob_on, ink_off_page
# cell_traj should be a list, each element is an nx2 matrix representing points
def render_image(cell_traj, epsilon, blur_sigma, PM):
    traj_img = space_motor_to_img(cell_traj)
    

# x: [n x 1] data
# lind [k x 1] linear indices in x
# inkval [k x 1] to be added to data, at index lind
def seqadd(x, lind, inkval):
    return x

def check_bounds(myt, imsize):
    pass

def pari_dist(D):
    pass



