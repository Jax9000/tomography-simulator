from scipy.misc import imresize
from scipy.ndimage import rotate

import numpy as np
import matplotlib.pyplot as plt

from matplotlib.pyplot import imshow
from skimage.transform import iradon, radon, rescale
from skimage.io import  imread
from enum import Enum


class Filter(Enum):
    none = None
    ramp = "ramp"
    shepp_logan =  "shepp-logan"
    cosine = "cosine"
    hamming = "hamming"
    hann = "hann"


class ParallelComputedTomography:

    # region Constructor and helpers
    def __init__(self, detectors, alpha, scans):
        self._detectors = detectors
        self._alpha = alpha
        self._scans = scans
        self._sinogram = np.array([])
        self._original_image = np.array([])
        self._restored_image = np.array([])

    def __setup(self, img, detectors, alpha, scans):
        self._original_image = img
        if detectors != 0:
            self._detectors = detectors
        if alpha != 0:
            self._alpha = alpha
        if scans != 0:
            self._scans = scans

    def get_difference(self):
        img = self._original_image
        scale = 1.0 * len(self._restored_image) / len(img)
        rimg = rescale(img, scale=scale)

        return rimg - self._restored_image

    def __filter(self, function):
        m, n = self._sinogram.shape
        theta = np.linspace(0, self._alpha, self._scans, endpoint=False)

    @staticmethod
    def show(img, title="Title"):
        imshow(img, cmap=plt.cm.Greys_r)
        plt.title(title)
        # plt.show()
    # endregion

    # region Use external libraries.
    def sinogram_radon(self, img, detectors=0, alpha=0, scans=0):
        self.__setup(img, detectors, alpha, scans)

        self._original_image = img
        scale = 1.0*self._detectors/len(img)
        img = rescale(img, scale=scale)

        theta = np.linspace(0., float(self._alpha), self._scans, endpoint=False)
        # print theta
        self._sinogram = radon(img, theta=theta, circle=True)
        return self._sinogram

    def restore_img_fbp(self, filter=Filter.ramp):
        theta = np.linspace(0., float(self._alpha), self._scans, endpoint=False)
        self._restored_image = iradon(self._sinogram, theta=theta, circle=True, filter=filter)
        return self._restored_image
    # endregion

    def our_create_sinogram(self, img, detectors=0, alpha=0, scans=0):
        self.__setup(img, detectors, alpha, scans)

        self._original_image = img
        scale = 1.0*self._detectors/len(img)
        img = rescale(img, scale=scale)


        result = []
        for angle in np.linspace(0, self._alpha , self._scans):
            rotated_img = rotate(img, angle, reshape=False)
            result.append(self.__scan_step(rotated_img))

        result = result[::-1]
        self._sinogram = np.array(result).transpose()
        self._sinogram = self._sinogram[::-1]
        return self._sinogram

    def our_restore_img_bp(self):
        det = self._detectors
        img = np.zeros(det*det).reshape((det, det))
        angle = float(self._alpha)/self._scans

        for i in range(0, self._scans):
            row = (self._sinogram[:,i])
            img += row
            img = rotate(img, -angle, reshape=False)


        img = rotate(img, 180)
        img /= self._scans
        self._restored_image = img
        return img

    def __calculate_ray_value(self, column, img):
        value = 0
        for i in range(0, self._detectors):
            value += img[i, column]
        # probably not necessary division
        # value /= self._detectors
        return value

    def __scan_step(self, img):
        vector = []
        for i in range(0, self._detectors):
            vector.append(self.__calculate_ray_value(i, img))
        return vector

# region Testy
pct = ParallelComputedTomography(70, 180, 90)
originalImage = imread("test_data/test02.png", as_grey=True)
pct.our_create_sinogram(originalImage)

restored = pct.restore_img_fbp(Filter.none)
plt.figure(4)
plt.subplot(221)
pct.show(restored, "Lib restored none filter")

restored = pct.restore_img_fbp(Filter.hamming)
plt.figure(4)
plt.subplot(222)
pct.show(restored, "Lib restored hamming")

restored = pct.our_restore_img_bp();


restoredMax = np.amax(restored)
restored = restored / restoredMax
restored /=2
plt.subplot(223)
pct.show(restored, "My restored none filter")

plt.subplot(224)
imkwargs = dict(vmin=0.3, vmax=1)
plt.figure(6)
originalImage = rescale(originalImage, scale=0.35)
plt.imshow(abs(originalImage -restored), cmap=plt.cm.Greys_r, **imkwargs)

plt.show()


# endregion