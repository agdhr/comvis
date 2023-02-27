import numpy as np
import cv2

filename = '05-transparent/20230119/ARABIKA/JA05S01_20230119_223328_segmented_transparent.png'
def color_features(filename):
    img = cv2.imread(filename)
    if img is None:
        return
    # Convert BGR to HSV colorspace
    # Split the channels - h,s,v
    b, g, r = cv2.split(img)

    # Initialize the color feature
    color_feature = []
    N = r.shape[0] * r.shape[1]
    # The first central moment - ave rage
    r_mean = np.mean(r)  # np.sum(h)/float(N)
    g_mean = np.mean(g)  # np.sum(s)/float(N)
    b_mean = np.mean(b)  # np.sum(v)/float(N)
    color_feature.extend([r_mean, g_mean, b_mean])
    print('R mean       =', r_mean)
    print('G mean       =', g_mean)
    print('B mean       =', b_mean)

color_features(filename)