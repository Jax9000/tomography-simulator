from scipy.ndimage import rotate
from scipy.fftpack import fftshift, fft, ifft

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

    def filter(self):
        x, y = self._sinogram.shape
        sinogram = self._sinogram.copy()
        n = 2048.0
        sinogram.resize((n, y))
        f = fftshift(abs(np.mgrid[-1:1:2 / n])).reshape(-1, 1)
        projection = fft(sinogram, axis=0) * np.tile(f, (1, y))
        self._sinogram = np.real(ifft(projection, axis=0))[:x]
        self._sinogram /= np.amax(self._sinogram)
        return self._sinogram

    @staticmethod
    def show(img, title="Plot"):
        imshow(img, cmap=plt.cm.Greys_r)
        plt.title(title)
        plt.axis('off')
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

        img = rotate(img, self._alpha, reshape=False)
        # img = rotate(img, 180)
        img /= self._scans
        img /= np.amax(img)
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
# originalImage = imread("test_data/phantom.png", as_grey=True)
#
# pct = ParallelComputedTomography(100, 179, 90)
#
# sinogram = pct.our_create_sinogram(originalImage)
# print np.amax(sinogram)
# plt.subplot(121)
# pct.show(sinogram, "Raw sinogram")
#
#
# sinogram = pct.filter()
# print np.amax(sinogram)
# plt.subplot(122)
# pct.show(sinogram, "Filtered sinogram")
# restored = pct.our_restore_img_bp();
#
# plt.figure(2)
# plt.subplot(121)
# pct.show(restored, "Restored")
#
#
#
# imkwargs = dict(vmin=0, vmax=1)
# restored = rescale(restored, scale=len(originalImage)/100.0)
# plt.subplot(122)
# dif = abs(originalImage - restored)
# dif /= np.amax(dif)
# plt.imshow(dif , cmap=plt.cm.Greys_r, **imkwargs)
# plt.title("Diff")
# plt.axis('off')
# plt.show()
#
# print (1 - (np.sum(dif) / dif.size)) * 100


# endregion