import numpy as np
import scipy.ndimage

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

# approximate equal
def aeq(x, y, tol=np.finfo(float).eps*(10**10)):
    if x.shape != y.shape:
        print("error: x, y should have the same shape")
        exit(-1)
    z = np.abs(x-y) < tol
    return np.all(z)

def sub2ind(array_shape, rows, cols):
    return rows*array_shape[1] + cols

def ind2sub(array_shape, ind):
    rows = (ind.astype('int') / array_shape[1])
    cols = (ind.astype('int') % array_shape[1]) # or numpy.mod(ind.astype('int'), array_shape[1])
    return (rows, cols)

def matlab_style_gauss2D(shape, sigma):
    """
    2D gaussian mask - should give the same result as MATLAB's
    fspecial('gaussian',[shape],[sigma])
    """
    m,n = [(ss-1.)/2. for ss in shape]
    y,x = np.ogrid[-m:m+1,-n:n+1]
    h = np.exp( -(x*x + y*y) / (2.*sigma*sigma) )
    h[ h < np.finfo(h.dtype).eps*h.max() ] = 0
    sumh = h.sum()
    if sumh != 0:
        h /= sumh
    return h

# renturn prob_on, ink_off_page
# cell_traj should be a list, each element is an nx2 matrix representing points
def render_image(cell_traj, epsilon, blur_sigma, PM):
    # convert to img space
    traj_img = space_motor_to_img(cell_traj)
    
    # draw trajectories on the img
    template = np.zeros(PM['imsize'])
    nsub = len(traj_img)
    ink_off_page = False
    for i in range(nsub):
        # ink model parameters
        ink = PM['ink_pp']
        max_dist = PM['ink_max_dist']
       
        # check bc
        myt = traj_img[i]   # should be np.array with shape (N,2)
        if myt.shape[1] != 2:
            print("myt shape:", myt.shape)
            myt = np.transpose(myt)

        out = check_bounds(myt, PM['imsize'])   # out is a list with len N
        if np.array(out).any():
            ink_off_page = true
            non_out_index = []
            for idx in range(len(out)):
                if out[idx] == 0:
                    non_out_index.append[idx]
        else:
            non_out_index = [i for i in range(len(out))]
        myt = myt[non_out_index, :]
        if myt.shape[0] == 0:
            continue

        # compute distance between each trajectory point and the next one
        if myt.shape[0] == 1:
            myink = ink
        else:
            dist = pair_dist(myt)       # dist is a np.array of shape (N-1,)
            for i in range(dist.shape[0]):
                if dist[i] > max_dist:
                    dist[i] = max_dist
            np.insert(dist, 0, dist[0])
            myink = np.multiply(dist, ink/max_dist)         # myink is a np.array of shape (N,1)

        # make sure we have the minimum amount of ink
        # if a particular trajectory is very small
        sumink = np.sum(myink)
        if aeq(sumink, 0):
            nink = np.prod(myink.shape)
            myink = np.ones(myink.shape) * (ink / nink)
        elif sumink < ink:
            myink = myink * (ink / sumink)
        # share ink with the neighboring 4 pixels
        x = myt[:,0]
        y = myt[:,1]
        xfloor = np.floor(x)
        yfloor = np.floor(y)
        xceil = np.ceil(x)
        yceil = np.ceil(y)
        x_c_ratio = x - xfloor
        y_c_ratio = y - yfloor
        x_f_ratio = 1 - x_c_ratio
        y_f_ratio = 1 - y_c_ratio
        # lin_ff = sub2ind(PM['imsize'], xfloor, yfloor)
        # lin_cf = sub2ind(PM['imsize'], xceil, yfloor)
        # lin_fc = sub2ind(PM['imsize'], xfloor, yceil)
        # lin_cc = sub2ind(PM['imsize'], xceil, yceil)

        # paint the image
        template = seqadd(template, xfloor, yfloor, np.multiply(np.multiply(myink, x_f_ratio), y_f_ratio))
        template = seqadd(template, xceil, yfloor, np.multiply(np.multiply(myink, x_f_ratio), y_f_ratio))
        template = seqadd(template, xfloor, yceil, np.multiply(np.multiply(myink, x_f_ratio), y_f_ratio))
        template = seqadd(template, xceil, yceil, np.multiply(np.multiply(myink, x_f_ratio), y_f_ratio))

    # filter the iamge to get the desired burhs-stroke size 
    a = PM['ink_a']
    b = PM['ink_b']
    H_broaden = np.multiply(np.array[[a/12., a/6., a/12],[a/6., 1.-a, a/6.], [a/12., a/6., a/12]], b)
    widen = template
    for i in range(PM['ink_ncon']):
        widen = scipy.ndimage.convolve(widen, H_broaden, mode='nearest')
    
    #threshold again
    for i in range(widen.shape[0]):
        for j in range(widen.shape[1]):
            widen[i][j] = widen[i][j] if widen[i][j] <= 1. else 1.

    # filter the image to get Gaussian
    # noise around the area wit hink
    pblur = widen
    if blur_sigma > 0:
        fsize = 11
        H_gaussian = matlab_style_gauss2D((fsize, fsize), blur_sigma)
        pblur = scipy.ndimage.convolve(pblur, H_gaussian, mode='nearest')
        pblur = scipy.ndimage.convolve(pblur, H_gaussian, mode='nearest')

    #final truncation
    for i in range(pblur.shape[0]):
        for j in range(pblur.shape[1]):
            if pblur[i][j] > 1.:
                pblur[i][j] = 1.
            elif pblur[i][j] < 0.:
                pblur[i][j] = 0.

    # probability of each pixel beign on
    prob_on = np.multiply(pblur, (1. - epsilon)) + np.multiply((1-pblur), epsilon)

    return [prob_on, ink_off_page]

# x: [n x 1] data
# lind [k x 1] linear indices in x
# inkval [k x 1] to be added to data, at index lind
def seqadd(data, xp, yp, inkval):
    if xp.shape[0] != yp.shape[0]:
        print("ERROR: xp and yp should have the same shape")
    if xp.shape[0] != inkval.shape[0]:
        print("ERROR: xp and inkval should have the same shape")
    data[xp, yp] = data[xp, yp] + inkval
    return data

def check_bounds(myt, imsize):
    xt = myt[:,0]
    yt = myt[:,1]
    out = []
    for i in range(myt.shape[0]):
        if (np.floor(xt[i]) < 1) or (np.ceil(xt[i]) > imsize[0]) or\
           (np.floor(yt[i]) < 1) or (np.ceil(yt[i]) > imsize[0]):
           out.append(1)
        else:
            out.append(0)
    return out

def pari_dist(D):
    x1 = D[0:-1, :]
    x2 = D[1:, :]
    z = np.sqrt(np.sum(np.square(x1-x2), axis=1))
    return z



