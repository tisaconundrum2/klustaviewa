import numpy as np


# Color creation routines
# -----------------------
def hue(H):
    H = H.reshape((-1, 1))
    R = np.abs(H * 6 - 3) - 1;
    G = 2 - np.abs(H * 6 - 2);
    B = 2 - np.abs(H * 6 - 4);
    return np.clip(np.hstack((R,G,B)), 0, 1)
    
def hsv_to_rgb(HSV):
    a = HSV[:,1].reshape((-1, 1))
    b = HSV[:,2].reshape((-1, 1))
    a = np.tile(a, (1, 3))
    b = np.tile(b, (1, 3))
    return ((hue(HSV[:,0]) - 1) * a + 1) * b

def generate_hsv(n0=20):
    H = np.linspace(0., 1., n0)
    i = np.arange(n0)
    H = H[~((i==5) | (i==7) | (i==10) | (i==12) | (i==15) |(i==17) | (i==18) | (i==19))]
    # H = H[((i==15) |(i==17) | (i==18) | (i==19))]

    H = np.repeat(H, 4)
    
    n = len(H)
    S = np.ones(n)
    V = np.ones(n)
    # change V for half of the colors
    V[1::2] = .75
    # change S for half of the colors
    S[2::4] = .75
    S[3::4] = .75
    
    hsv = np.zeros((n, 3))
    hsv[:,0] = H
    hsv[:,1] = S
    hsv[:,2] = V

    return hsv

    
# Global variables with all colors
# --------------------------------
# generate a list of RGB values for each color
hsv = generate_hsv()
COLORS_COUNT = len(hsv)
# Permutation.
step = 17  # needs to be prime with COLORS_COUNT
perm = np.mod(np.arange(0, step * 24, step), 24)
perm = np.hstack((2 * perm, 2 * perm + 1))
hsv = hsv[perm, ...]
hsv = np.clip(hsv, 0, 1)
COLORMAP = hsv_to_rgb(hsv)
COLORMAP = np.clip(COLORMAP, 0, 1)
COLORMAP = np.vstack(((1., 1., 1.), COLORMAP))

# HSV shifts
shifts = np.array([
                   [0, -.5, .5],    # highlight
                   [0, 0, 0],       # normal
                   [0, -.2, -.2],    # gradient
                   [0, -.4, -.4],    # gradient
                   [0, -.6, -.6],    # gradient
                   ]).T
SHIFTLEN = shifts.shape[1]                   
# First shift: normal color.
# Second shift: highlight.
# Other shifts: gradients.
COLORMAP_TEXTURE = np.zeros((SHIFTLEN, hsv.shape[0] + 1, 3))
hsv_shifted = np.clip(hsv.reshape((-1, 3, 1)) + shifts.reshape((1, 3, -1)), 
    0, 1)
for i in xrange(SHIFTLEN):
    COLORMAP_TEXTURE[i, ...] = np.vstack(((1., 1., 1.), 
        np.clip(hsv_to_rgb(hsv_shifted[:, :, i]), 0, 1)))

def next_color(color):
    return np.mod(color, COLORS_COUNT) + 1
