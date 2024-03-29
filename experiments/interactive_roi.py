# Requires dipy.align.cc_residuals from imaffine branch
from experiments.registration.dataset_info import *
from experiments.registration.semi_synthetic import *
import nibabel as nib
import dipy.viz.regtools as rt
import experiments.registration.regviz as rv
import dipy.align.cc_residuals as ccr
from experiments.registration.rcommon import readAntsAffine
import dipy.align.vector_fields as vfu
from numpy.testing import (assert_equal,
                           assert_almost_equal, 
                           assert_array_equal,
                           assert_array_almost_equal,
                           assert_raises)

def check_affine_fit(x, y, x_name="", y_name="", force_reference=-1):
    alpha, beta, x_fit, y_fit, ref, mse = ccr.affine_fit(x, y, force_reference)
    x_fit = np.array(x_fit)
    y_fit = np.array(y_fit)
    #verify optimality
    main_title = ""
    if ref == 0: # fit y as a function of x
        main_title = y_name+" as a function of "+x_name
        assert_almost_equal(x.dot(x)*alpha + x.sum()*beta - x.dot(y), 0)
        assert_almost_equal(x.sum()*alpha + len(y) * beta - y.sum(), 0)
        figure()
        scatter(x,y)
        plot(x_fit, y_fit)
        title(main_title)
        xlabel(x_name)
        ylabel(y_name)
    else: # Fit x as a function of y
        main_title = x_name+" as a function of "+y_name
        assert_almost_equal(y.dot(y)*alpha + y.sum()*beta - y.dot(x), 0)
        assert_almost_equal(y.sum()*alpha + len(x) * beta - x.sum(), 0)
        figure()
        scatter(y,x)
        plot(y_fit, x_fit)
        title(main_title)
        xlabel(y_name)
        ylabel(x_name)
    print(main_title + ". MSE: "+str(mse)+". alpha: "+str(alpha)+". beta: "+str(beta) )


def check_linear_fit(x, y, x_name="", y_name="", force_reference=-1):
    x /= np.linalg.norm(x)
    y /= np.linalg.norm(y)
    alpha, x_fit, y_fit, ref, mse = ccr.linear_fit(x, y, force_reference)
    x_fit = np.array(x_fit)
    y_fit = np.array(y_fit)
    #verify optimality
    main_title = ""
    if ref == 0: # fit y as a function of x
        main_title = y_name+" as a function of "+x_name
        assert_almost_equal(x.dot(y) - alpha * x.dot(x), 0)
        figure()
        scatter(x,y)
        plot(x_fit, y_fit)
        title(main_title)
        xlabel(x_name)
        ylabel(y_name)
    else: # Fit x as a function of y
        main_title = x_name+" as a function of "+y_name
        assert_almost_equal(x.dot(y) - alpha * y.dot(y), 0)
        figure()
        scatter(y,x)
        plot(y_fit, x_fit)
        title(main_title)
        xlabel(y_name)
        ylabel(x_name)
    print(main_title + ". MSE: "+str(mse)+". alpha: "+str(alpha))


def analyze_roi(p, delta, mod1, ss_mod1, mod1_name, mod2, ss_mod2, mod2_name, residuals, check_function):
    px = p[0]
    py = p[1]
    pz = p[2]
    roi = np.zeros_like(residuals)
    roi[(px-delta):(px+delta+1), (py-delta):(py+delta+1), (pz-delta):(pz+delta+1)] = 1
    rt.plot_slices(residuals_nb, cmap=None)
    rt.plot_slices((roi+0.1)*residuals_nb, cmap=None)

    samples = roi*residuals_nb
    samples = samples[roi!=0].reshape(-1)

    x = mod1[roi!=0].reshape(-1)
    y = mod2[roi!=0].reshape(-1)

    check_function(x, y, mod1_name, mod2_name, 0)
    check_function(x, y, mod1_name, mod2_name, 1)
    
    x_ss_t1 = mod1[roi!=0].reshape(-1)
    y_ss_t1 = ss_mod1[roi!=0].reshape(-1)
    check_function(x_ss_t1, y_ss_t1, mod1_name, "F["+mod2_name+"]", 0)
    check_function(x_ss_t1, y_ss_t1, mod1_name, "F["+mod2_name+"]", 1)

    x_ss_t2 = mod2[roi!=0].reshape(-1)
    y_ss_t2 = ss_mod2[roi!=0].reshape(-1)
    check_function(x_ss_t2, y_ss_t2, mod2_name, "F["+mod1_name+"]", 0)
    check_function(x_ss_t2, y_ss_t2, mod2_name, "F["+mod1_name+"]", 1)


# Load data
t1_name = t1_name = get_brainweb("t1", "strip")
t1_nib = nib.load(t1_name)
t1 = t1_nib.get_data().squeeze()
t1 = t1.astype(np.float64)

t2_name = t2_name = get_brainweb("t2", "strip")
t2_nib = nib.load(t2_name)
t2 = t2_nib.get_data().squeeze()
t2 = t2.astype(np.float64)


# Apply the transfer
t2_lab = t2.astype(np.int32)
means_t2t1, vars_t2t1 = get_mean_transfer(t2_lab, t1)
ss_t1 = means_t2t1[t2_lab]

t1_lab = t1.astype(np.int32)
means_t1t2, vars_t1t2 = get_mean_transfer(t1_lab, t2)
ss_t2 = means_t1t2[t1_lab]

# Compute residuals of locally affine fit on T1 and T2
radius = 4
residuals_nb = ccr.compute_cc_residuals(t1, t2, radius, 1)
residuals_nb = np.array(residuals_nb)

# Compute residuals of locally affine fit on F(T1) and T2
radius = 4
residuals_t2 = ccr.compute_cc_residuals(ss_t2, t2, radius, 1)
residuals_t2 = np.array(residuals_t2)

# Compute residuals of locally affine fit on T1 and F[T2]
radius = 4
residuals_t1 = ccr.compute_cc_residuals(t1, ss_t1, radius, 1)
residuals_t1 = np.array(residuals_t1)


# Prepare interactive graphs
global_figure = None
global_map = None
sel_x = None
sel_y = None

def draw_affine_fit(ax, x, x_name, y, y_name):
    # Affine fit
    alpha, beta, x_fit, y_fit, ref, mse = ccr.affine_fit(x, y, 0)
    x_fit, y_fit = np.array(x_fit), np.array(y_fit)
    
    font = {'family' : 'serif',
            'color'  : 'black',
            'weight' : 'normal',
            'size'   : 16,}
    
    main_title = y_name+" as a function of "+x_name
    ax.cla()
    ax.scatter(x, y)
    ax.plot(x_fit, y_fit)
    ax.grid(True)
    ax.set_title(main_title, fontdict=font)
    ax.set_xlabel(x_name, fontdict=font)
    ax.set_ylabel(y_name, fontdict=font)

def draw_rect(event):
    global global_figure
    global sel_x
    global sel_y
    if event.inaxes != global_figure.axes[0]:
        return
    global global_map
    side = 9
    px, py = int(event.xdata), int(event.ydata)
    
    img0 = global_map['img0']
    img0_name = global_map['img0_name']
    img1 = global_map['img1']
    img1_name = global_map['img1_name']
    shape = img0.shape
    residuals = global_map['residuals']
    slice_type = global_map['slice_type']
    slice_index = global_map['slice_index']
    if slice_index is None:
        slice_index = img0.shape[slice_type]//2
    
    subsample0=None
    subsample1=None
    x, y, z = None, None, None
    ax = global_figure.add_subplot(1,3,1)
    if slice_type==0:
        ax.imshow(residuals_nb[slice_index,:,:].T, origin='lower')
        x, y, z = slice_index, px, py
    elif slice_type==1:
        ax.imshow(residuals_nb[:,slice_index,:].T, origin='lower')
        x, y, z = px, slice_index, py
    else:
        ax.imshow(residuals_nb[:,:,slice_index].T, origin='lower')
        x, y, z = px, py, slice_index
    print("V[%d,%d,%d]=%f\n"%(x,y,z,residuals[x,y,z]))
    minx, maxx = max(0, x-side//2), min(shape[0]-1, x+side//2)
    miny, maxy = max(0, y-side//2), min(shape[1]-1, y+side//2)
    minz, maxz = max(0, z-side//2), min(shape[2]-1, z+side//2)
    
    sel_x=img0[minx:(maxx+1), miny:(maxy+1), minz:(maxz+1)]
    sel_x = sel_x.reshape(-1)
    sel_y=img1[minx:(maxx+1), miny:(maxy+1), minz:(maxz+1)]
    sel_y = sel_y.reshape(-1)
    ax = global_figure.add_subplot(1,3,2)
    draw_affine_fit(ax, sel_x, img0_name, sel_y, img1_name)
    ax = global_figure.add_subplot(1,3,3)
    draw_affine_fit(ax, sel_y, img1_name, sel_x, img0_name)    
    
    ax = global_figure.get_axes()[0]
    R = Rectangle((px-side//2,py-side//2), side, side, facecolor='none', linewidth=3, edgecolor='#DD0000')
    if len(ax.artists)>0:
        ax.artists[-1].remove()
    ax.add_artist(R)
    draw()

def run_interactive(img0, img0_name, img1, img1_name, residuals, slice_type=1, slice_index=None):
    global global_figure
    global global_map
    
    global_figure = figure()
    ax = global_figure.add_subplot(1,3,1)
    ax.imshow(residuals[:,residuals.shape[1]//2,:].transpose(), origin='lower')
    global_map = {'img0':img0,
                  'img0_name':img0_name,
                  'img1':img1,
                  'img1_name':img1_name,
                  'residuals':residuals,
                  'slice_type':slice_type,
                  'slice_index':slice_index}
    global_figure.canvas.mpl_connect('button_press_event', draw_rect)
    
run_interactive(t1, "T1", t2, "T2", residuals_nb, 1, None)
