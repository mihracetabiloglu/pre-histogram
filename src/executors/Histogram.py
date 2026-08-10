import os
import sys
import cv2
import numpy as np
import matplotlib.pyplot as plt

sys.path.append(os.path.join(os.path.dirname(__file__), '../../../../'))

from sdks.novavision.src.media.image import Image
from sdks.novavision.src.base.model import Image as ImageModel
from sdks.novavision.src.base.component import Component
from sdks.novavision.src.helper.executor import Executor

from components.PreHistogram.src.utils.response import build_response_histogram
from components.PreHistogram.src.models.PackageModel import PackageModel

class Histogram(Component):
    """
    This class initializes the configuration for computing image histograms, 
    including RGB and Grayscale channels. It processes the input image, extracts 
    histogram data for selected channels, and optionally generates a matplotlib plot 
    as an image representation. 
    """

    def __init__(self, request, bootstrap):
        super().__init__(request)
        self.request.model = PackageModel(**(self.request.data))
        self.initialize_request_data(request=request, bootstrap=bootstrap)
        self.image = self.request.get_param("inputImage")
        self.channelRed = self._read_bool_param("configChannelRed")
        self.channelGreen = self._read_bool_param("configChannelGreen")
        self.channelBlue = self._read_bool_param("configChannelBlue")
        self.channelGrayScale = self._read_bool_param("configChannelGrayScale")
        # Regularize the pixel min-max value
        configPixelMin = self._read_int_param("configPixelMin", default=0)
        configPixelMax = self._read_int_param("configPixelMax", default=255)
        self.pixelMax = max(configPixelMin, min(configPixelMax + 1, 256))
        self.pixelMin = max(0, min(configPixelMin, configPixelMax))

        self.plotImage = self._read_bool_param("configPlotImage", default=True)

        self.channels = []

        if bool(self.channelRed):
           self.channels.append(0)

        if bool(self.channelGreen):
           self.channels.append(1)

        if bool(self.channelBlue):
           self.channels.append(2)

    @staticmethod
    def bootstrap(config: dict) -> dict:
        return {}

    def _read_config_value(self, param_name):
        value = self.request.get_param(param_name)
        while hasattr(value, "value"):
            value = value.value
        if isinstance(value, dict):
            return value.get("value", value)
        return value

    def _read_bool_param(self, param_name, default=False):
        raw_value = self._read_config_value(param_name)
        if raw_value is None:
            return default
        if isinstance(raw_value, bool):
            return raw_value
        if isinstance(raw_value, (int, float)):
            return bool(raw_value)
        if isinstance(raw_value, str):
            normalized = raw_value.strip().lower()
            if normalized in {"true", "1", "yes", "enable"}:
                return True
            if normalized in {"false", "0", "no", "disable"}:
                return False
        return default

    def _read_int_param(self, param_name, default=0):
        raw_value = self._read_config_value(param_name)
        if raw_value is None:
            return default
        if isinstance(raw_value, str):
            try:
                return int(raw_value)
            except ValueError:
                return default
        return int(raw_value)

    def run(self):
        img = Image.get_frame(img=self.image, redis_db=self.redis_db)
        
        """ RGB & GrayScale Data Output : list[list[float]] """
        self.out = self.img2hist(img.value, self.channels, self.channelGrayScale, self.pixelMin, self.pixelMax)
        #Self.out : Frame needed !!

        """ MathPlot Image Generation : If plot image checkbox checked """
        if self.plotImage: 
            img.value = self.hist2plot(self.out, self.channels, self.channelGrayScale, self.pixelMin, self.pixelMax)
            self.image = Image.set_frame(img=img, package_uID=self.uID, redis_db=self.redis_db)
        
        packageModel = build_response_histogram(context=self)
        return packageModel

    def img2hist(self, image, channels=None, grayscale=False, pixmin=0, pixmax=255):
        """
        Compute the histogram for specified channels in an image or for grayscale.

        Args:
        image (np.ndarray): OpenCV image in BGR format.
        channels (list[int] | None): List of channel indices to compute histograms for (0=Red, 1=Green, 2=Blue).
        grayscale (bool): If True, computes the histogram for the grayscale version of the image.
        pixmin (int): Minimum pixel value (inclusive).
        pixmax (int): Maximum pixel value (exclusive).

        Returns:
        list[list[float]]: A list of normalized histogram values for each channel:
            - Index 0: Red
            - Index 1: Green
            - Index 2: Blue
            - Index 3: Grayscale
        """
        # Output structure: [R_hist, G_hist, B_hist, Gray_hist]
        out = [[], [], [], []]

        # Compute RGB channel histograms if channels are specified
        if channels:
            for channel in channels:
                if channel in [0, 1, 2]:  # Ensure valid channel index
                    cvchannel = 2 - channel # RGB to BGR issues -> [0,1,2] to [2,1,0]
                    hist = cv2.calcHist([image], [cvchannel], None, [pixmax - pixmin], [pixmin, pixmax])
                    hist = hist.flatten()

                    if hist.max() > 0:
                       hist = hist / hist.max()

                    hist = hist.tolist()
                    out[channel] = hist
                    empty = [0] * pixmin
                    out[channel] = empty + out[channel]

        # Compute grayscale histogram if requested
        if grayscale:
            gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            gray_hist = cv2.calcHist([gray_image], [0], None, [pixmax - pixmin], [pixmin, pixmax])
            gray_hist = gray_hist.flatten()

            if gray_hist.max() > 0:
                gray_hist = gray_hist / gray_hist.max()

            gray_hist = gray_hist.tolist()
            out[3] = gray_hist
            empty = [0] * pixmin
            out[3] = empty + out[3]

        return out

    def hist2plot(self, hdata, channels:list, grayscale=False, pixmin=0, pixmax=255):
        plt.figure(figsize=(10, 6))

        plt.xlim(pixmin, pixmax)

        # Plot each channel's histogram
        if channels.__contains__(0): plt.plot(hdata[0], color='red',   label='Red Channel')
        if channels.__contains__(1): plt.plot(hdata[1], color='lime', label='Green Channel')
        if channels.__contains__(2): plt.plot(hdata[2], color='blue',  label='Blue Channel')
        if grayscale: plt.plot(hdata[3], color='black', label='GrayScale')

        # Add labels and title
        plt.title('Histogram')
        plt.xlabel('Pixel Intensity')
        plt.ylabel('Frequency')
        plt.legend()
        plt.grid(True)

        # Save the figure to a numpy array
        plt.tight_layout()
        canvas = plt.gca().figure.canvas
        canvas.draw()

        # Convert to numpy array
        img = np.frombuffer(canvas.tostring_rgb(), dtype=np.uint8)
        img = img.reshape(canvas.get_width_height()[::-1] + (3,))

        # Convert to BGR for OpenCV compatibility
        img_bgr = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

        plt.close()  # Close the plt figure
        return img_bgr

if "__main__" == __name__:
    Executor(sys.argv[1]).run()
