# PyElas

This is the Python version of libelas (LIBrary for Efficient LArge-scale Stereo matching) by Andreas Geiger.

Apart from fixing warnings reported by GCC on Linux, almost nothing has been changed on the original code.

This library depends on numpy, as it returns numpy, because the disparity maps are returned as numpy array.

The original library was released under the GNU General Public License, so this is as well.


## Usage
```python
import cv2
from elas import Elas

# Images can be loaded with any library, as long as they can be accessed with buffer protocol
left = cv2.imread('left.jpg')
right = cv2.imread('right.jpg')
# Images must be grayscale
# In particular, they must be 2D buffers, stored in row-major/C order
left = cv2.cvtColor(left, cv2.COLOR_BGR2GRAY)
right = cv2.cvtColor(right, cv2.COLOR_BGR2GRAY)

# Construct the Elas object. You can pass your customized parameters...
e = Elas()
# ...or, optionally, you can set parameters as object members.
# Then compute the disparities. The results will be returned as numpy arrays
disp_left, disp_right = e.process(left, right)
```

## Parameters

Parameter | Type | Description | Default value (robotics) | Defult value (Middlebury)
--------- | ---- | ----------- | ------------------------ | -------------------------
`disp_min` | int | Min disparity | 0 | 0
`disp_max` | int | Max disparity | 255 | 255
`support_threshold` | float | Max uniqueness ratio (best vs. second best support match) | 0.85 | 0.95
`support_texture` | int | Min texture for support points | 10 | 10
`candidate_stepsize` | int | Step size of regular grid on which support points are matched | 5 | 5
`incon_window_size` | int | Window size of inconsistent support point check | 5 | 5
`incon_threshold` | int | Disparity similarity threshold for support point to be considered consistent | 5 | 5
`incon_min_support` | int | Minimum number of consistent support points | 5 | 5
`add_corners` | bool | Add support points at image corners with nearest neighbor disparities | False | True
`grid_size` | int | Size of neighborhood for additional support point extrapolation | 20 | 20
`beta` | float | Image likelihood parameter | 0.02 | 0.02
`gamma` | float | Prior constant | 3 | 5
`sigma` | float | Prior sigma | 1 | 1
`sradius` | float | Prior sigma radius | 2 | 3
`match_texture` | int | Min texture for dense matching | 1 | 0
`lr_threshold` | int | Disparity threshold for left/right consistency check | 2 | 2
`speckle_sim_threshold` | float | Similarity threshold for speckle segmentation | 1 | 1
`speckle_size` | int | Maximal size of a speckle (small speckles get removed) | 200 | 200
`ipol_gap_width` | int | Interpolate small gaps (left<->right, top<->bottom) | 3 | 5000
`filter_median` | bool  | Optional median filter (approximated) | False | True
`filter_adaptive_mean` | bool  | Optional adaptive mean filter (approximated) | True | False
`postprocess_only_left` | bool  | Save time by not postprocessing the right image | True | False
`subsampling` | bool  | Save time by only computing disparities for each 2nd pixel | False | False
