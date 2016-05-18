
from view import View
from tomograph import ParallelComputedTomography as CT
from tomograph import Filter
import numpy as np

class CTController:
    def __init__(self):
        self._view = View()
        self._ct = CT(200, 180, 180)
        self._img = np.array([])

    def image_file_loaded(self, img):
        self._img = img

    def button_pressed(self):
        vw = self._view
        ct = self._ct
        sinogram = ct.create_sinogram(self._img, vw.getDetectors(), vw.getAngle(), vw.getScans())
        reconstructed_img = ct.restore_img_fbp(Filter.ramp)
        diff = ct.getDifference()
        vw.setSubPlot(sinogram, 2)
        vw.setSubPlot(reconstructed_img, 3)
        vw.setSubPlot(diff, 4)
