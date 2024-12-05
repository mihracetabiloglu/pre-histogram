"""
    Image to RGB & GrayScale histogram data.   
"""

import os
import sys
import cv2
import numpy as np
import matplotlib.pyplot as plt

sys.path.append(os.path.join(os.path.dirname(__file__), '../../../../'))

from sdks.novavision.src.media.image import Image
from sdks.novavision.src.base.response import Response
from sdks.novavision.src.base.component import Component
from sdks.novavision.src.helper.executor import Executor
from components.Histogram.src.utils.response import build_response
from components.Histogram.src.models.PackageModel import PackageModel

class Histogram(Component):
    """
    This class initializes the configuration for computing image histograms, 
    including RGB and Grayscale channels. It processes the input image, extracts 
    histogram data for selected channels, and optionally generates a matplotlib plot 
    as an image representation. 
    """

    def __init__(self, request, bootstrap):
        super.__init__(request)
        self.request.model = PackageModel(**(self.request.data))
        self.initialize_request_data(request=request, bootstrap=bootstrap)
        self.channelRed = self.request.get_param("channelRed")
        self.channelGreen = self.request.get_param("channelGreen")
        self.channelBlue = self.request.get_param("channelBlue")
        self.channelGrayScale = self.request.get_param("channelGrayScale")
        self.pixelMin = self.request.get_param("pixelMin")
        self.pixelMax = self.request.get_param("pixelMax")
        self.plotImage = self.request.get_param("plotImage")
        self.image = self.request.get_param("inputImage")

        self.channels = []        
        if self.channelRed.value   : self.channels.append(0)
        if self.channelGreen.value : self.channels.append(1)
        if self.channelBlue.value  : self.channels.append(2)        

    @staticmethod
    def bootstrap() -> dict:
        return {}

    def run(self):
        img = Image.get_frame(img=self.image, redis_db=self.redis_db)
        if not img: return None
        
        """ RGB & GrayScale Data Output : list[list[float]] """
        self.out = self.img2hist(self.image.value, self.channels, self.channelGrayScale.value, self.pixelMin.value, self.pixelMax.value)
        
        """ MathPlot Image Generation : If plot image checkbox checked """
        if self.plotImage.value: 
            self.image.value = self.hist2plot(self.out)
            self.image = Image.set_frame(img=img, package_uID=self.uID, redis_db=self.redis_db)
        
        packageModel = build_response(context=self)
        return Response(model=packageModel, bootstrap=self.bootstrap).response()

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
        out = [None, None, None, None]

        # Clamp pixel value range
        pixmax = max(pixmin, min(pixmax + 1, 256))
        pixmin = max(0, min(pixmin, pixmax))

        # Compute RGB channel histograms if channels are specified
        if channels:
            for channel in channels:
                if channel in [0, 1, 2]:  # Ensure valid channel index
                    cvchannel = 2 - channel # RGB to BGR issues -> [0,1,2] to [2,1,0]
                    hist = cv2.calcHist([image], [cvchannel], None, [pixmax - pixmin], [pixmin, pixmax])
                    hist = cv2.normalize(hist, hist).flatten().tolist()
                    out[channel] = hist

        # Compute grayscale histogram if requested
        if grayscale:
            gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            gray_hist = cv2.calcHist([gray_image], [0], None, [pixmax - pixmin], [pixmin, pixmax])
            gray_hist = cv2.normalize(gray_hist, gray_hist).flatten().tolist()
            out[3] = gray_hist

        return out

    def hist2plot(self, hdata):
        plt.figure(figsize=(10, 6))
        
        # Plot each channel's histogram
        plt.plot(hdata[0], color='red',   label='Red Channel')
        plt.plot(hdata[1], color='green', label='Green Channel')
        plt.plot(hdata[2], color='blue',  label='Blue Channel')
        plt.plot(hdata[3], color='black', label='GrayScale')
        
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