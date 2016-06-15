from tomograph import ParallelComputedTomography as PCT
from skimage.measure import compare_ssim as ssim
import numpy as np
from skimage.transform import rescale
from skimage.io import imread
import time


def mse(img1, img2):
    err = np.sum((img1.astype("float") - img2.astype("float")) ** 2)
    err /= float(img1.shape[0] * img1.shape[1])
    return err


def calculate_diff(img1, img2):
    length = len(img1)
    diff_sum = 0
    for i in range(0, length):
        for j in range(0, length):
            if abs(img1[i, j] - img2[i, j]) > 0.05:
                diff_sum += 1
    # return (diff_sum/img1.size) * 100.0
    return diff_sum/float(img1.size) * 100.0



originalImage = imread("test_data/phantom.png", as_grey=True)

fi = open("results.txt", 'a')

fi.write("\n\nScans number (detectors=250,alpha=180):\n")
for testing_value in range(10, 361, 10):
    start = time.time()
    pct = PCT(250, 180, testing_value)
    pct.our_create_sinogram(originalImage)
    pct.filter()
    restored = pct.our_restore_img_bp()
    restored = rescale(restored, scale=len(originalImage)/float(250))
    print '{0}, take: {1:.2}s'.format(testing_value, time.time() - start)
    fi.write('{0}:{1:.3f}\n'.format(testing_value, ssim(originalImage, restored)))

fi.close()