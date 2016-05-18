from scipy.misc import imresize
from scipy.ndimage import rotate

import numpy as np
import matplotlib.pyplot as plt

from matplotlib.pyplot import imshow
from skimage.io import imread
from skimage.transform import iradon


class ParallelComputedTomography:
    def __init__(self, detectors, alpha, scans):
        self._detectors = detectors
        self._alpha = alpha
        self._scans = scans
        self._sinogram = np.array([])
        self._original_image = np.array([])
        self._restored_image = np.array([])


    def create_sinogram(self, img, detectors=0, alpha=0, scans=0):
        if detectors != 0:
            self._detectors = detectors
        if alpha != 0:
            self._alpha = alpha
        if scans != 0:
            self._scans = scans

        self._original_image = img
        img = imresize(img, (self._detectors, self._detectors))

        result = []
        for angle in np.linspace(0, self._alpha, self._scans):
            rotated_img = rotate(img, angle, reshape=False)
            result.append(self.__scan_step(rotated_img))

        self._sinogram = rotate(np.array(result), 90, reshape=False)
        return self._sinogram

    def restore_img_bp(self):
        det = self._detectors
        img = np.zeros(det*det).reshape((det, det))
        angle = float(self._alpha)/self._scans

        for i in range(0, self._scans):
            row = self._sinogram[i,:]

            img += row
            img = rotate(img, angle, reshape=False)

        img -= np.sum(self._original_image)
        img /= self._scans

        return img

    def sinogram_radon(self, img, detectors=0, alpha=0, scans=0):
        print "asd"

    def restore_img_fbp(self):
        theta = np.linspace(0., self._alpha, self._detectors, endpoint=False)
        reconstruction_fbp = iradon(self._sinogram, theta=theta, circle=True)
        return reconstruction_fbp

    def __calculate_ray_value(self, column, img):
        value = 0
        for i in range(0, self._detectors):
            value += img[i, int(round(column))]
        # probably not necessary division
        value /= self._detectors
        return value

    # parallel rays
    def __scan_step(self, img):
        vector = []
        for i in range(0, self._detectors):
            vector.append(self.__calculate_ray_value(i, img))
        return vector



pct = ParallelComputedTomography(200, 180, 180)

sinogram = pct.create_sinogram(imread("test_data/phantom.png", as_grey=True))
imshow(sinogram, cmap=plt.cm.Greys_r,
       extent=(0, 180, 0, sinogram.shape[0]), aspect='auto')
plt.show()

restored = pct.restore_img_bp()
imshow(restored, cmap=plt.cm.Greys_r,
       extent=(0, 180, 0, restored.shape[0]), aspect='auto')
plt.show()



