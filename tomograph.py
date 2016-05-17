from scipy.misc import imresize
from scipy.ndimage import rotate

import numpy as np


class ParallelComputedTomography:
    def __init__(self, detectors, alpha, scans):
        self._detectors = detectors
        self._alpha = alpha
        self._scans = scans

    def scan(self, img, detectors=0, alpha=0, scans=0):
        if detectors != 0:
            self._detectors = detectors
        if alpha != 0:
            self._alpha = alpha
        if scans != 0:
            self._scans = scans

        img = imresize(img, detectors)

        result = []
        for angle in np.linspace(0, alpha, scans):
            rotated_img = rotate(img, angle)
            result.append(self.__scan_step(rotated_img))
        return np.array(result)



    def __calculate_ray_value(self, column, img):
        value = 0
        for i in range(0, self.detectors):
            value += img[i, int(round(column))]
        # probably not necessary division
        value /= self.detectors
        return value

    # parallel rays
    def __scan_step(self, img):
        vector = []
        for i in range(0, self._detectors):
            vector.append(self.__calculate_ray_value(i, img))
        return vector




