import os
import sys
import cv2
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Arka plan render modu (headless)
import matplotlib.pyplot as plt

sys.path.append(os.path.join(os.path.dirname(__file__), '../../../../'))

from sdks.novavision.src.media.image import Image
from sdks.novavision.src.base.model import Image as ImageModel
from sdks.novavision.src.base.component import Component
from sdks.novavision.src.helper.executor import Executor

from components.PreHistogram.src.utils.response import build_response_histogram
from components.PreHistogram.src.models.PackageModel import PackageModel

class HistogramExecutor(Component):
    """
    This class initializes the configuration for computing image histograms, 
    including RGB and Grayscale channels. It processes the input image, extracts 
    histogram data for selected channels, and optionally generates a matplotlib plot 
    as an image representation. 
    """

    def __init__(self, request, bootstrap):
        super().__init__(request, bootstrap)
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
        # DÜZELTME 1: Parametre sayısı fonksiyon tanımına uygun hale getirildi
        self.out = self.img2hist(img.value, self.channels, self.channelGrayScale, self.pixelMin, self.pixelMax)
        self.outputData = self.out

        """ MathPlot Image Generation : If plot image checkbox checked """
        if self.plotImage: 
            # DÜZELTME 1: Parametre sayısı fonksiyon tanımına uygun hale getirildi
            img.value = self.hist2plot(self.out, self.channels, self.channelGrayScale, self.pixelMin, self.pixelMax)
            self.image = Image.set_frame(img=img, package_uID=self.uID, redis_db=self.redis_db)
        
        self.outputImage = self.image
        
        packageModel = build_response_histogram(context=self)
        return packageModel

    def img2hist(self, image, channels=None, grayscale=False, pixmin=0, pixmax=255):
        out = [[], [], [], []]

        if channels:
            for channel in channels:
                if channel in [0, 1, 2]:
                    cvchannel = 2 - channel  # RGB -> BGR dönüşümü
                    hist = cv2.calcHist([image], [cvchannel], None, [pixmax - pixmin], [pixmin, pixmax])
                    hist = hist.flatten()

                    if hist.max() > 0:
                       hist = hist / hist.max()

                    hist = hist.tolist()
                    empty = [0] * pixmin
                    out[channel] = empty + hist

        if grayscale:
            gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            gray_hist = cv2.calcHist([gray_image], [0], None, [pixmax - pixmin], [pixmin, pixmax])
            gray_hist = gray_hist.flatten()

            if gray_hist.max() > 0:
                gray_hist = gray_hist / gray_hist.max()

            gray_hist = gray_hist.tolist()
            empty = [0] * pixmin
            out[3] = empty + gray_hist

        return out

    def hist2plot(self, hdata, channels: list, grayscale=False, pixmin=0, pixmax=255):
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.set_xlim(pixmin, pixmax)

        # Plot each channel's histogram
        if 0 in channels and len(hdata[0]) > 0: 
            ax.plot(hdata[0], color='red', label='Red Channel')
        if 1 in channels and len(hdata[1]) > 0: 
            ax.plot(hdata[1], color='lime', label='Green Channel')
        if 2 in channels and len(hdata[2]) > 0: 
            ax.plot(hdata[2], color='blue', label='Blue Channel')
        if grayscale and len(hdata[3]) > 0: 
            ax.plot(hdata[3], color='black', label='GrayScale')

        ax.set_title('Histogram')
        ax.set_xlabel('Pixel Intensity')
        ax.set_ylabel('Frequency')
        ax.legend()
        ax.grid(True)

        fig.tight_layout()
        fig.canvas.draw()

        # DÜZELTME 2: Güncel Matplotlib buffer yöntemi
        buf = fig.canvas.buffer_rgba()
        img_rgba = np.asarray(buf)
        img_bgr = cv2.cvtColor(img_rgba, cv2.COLOR_RGBA2BGR)

        plt.close(fig)
        return img_bgr

if "__main__" == __name__:
    Executor(sys.argv[1]).run()