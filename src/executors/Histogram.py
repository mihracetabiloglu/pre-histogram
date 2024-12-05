"""
Image to RGB channel histogram data.   
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

from sdks.novavision.src.helper.package import PackageHelper
from components.Histogram.src.models.PackageModel import PackageModel, PackageConfigs, HistogramOutputs, HistogramResponse, HistogramExecutor, ConfigExecutor, OutputImage

class Histogram(Component):
    def __init__(response, ):
        pass
    
    def img2hist(image, channel, pixmin, pixmax):
        """
        Compute the histogram for a specific channel in an image.

        Args:
            image (np.ndarray): CV2 MatLike image.
            channel (int): Channel index (0=Red, 1=Green, 2=Blue, 3=Grayscale).

        Returns:
            list[float]: A list of normalized histogram values for the selected channel.
        """
        if image is None: return None
        if pixmin >= pixmax: return None  

        # Grayscale channel
        if channel == 3:
            gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            hdata = cv2.calcHist([gray_image], [0], None,  [pixmax - pixmin], [pixmin, pixmax])
        else:
            # Split channels
            channels = cv2.split(image)  # BGR order
            if channel not in [0, 1, 2]:
                raise ValueError("Channel must be 0 (Red), 1 (Green), 2 (Blue), or 3 (Grayscale).")
            
            # Mapping BGR to Red, Green, Blue
            bgr_to_rgb_mapping = [2, 1, 0]
            selected_channel = bgr_to_rgb_mapping[channel]
            
            # Compute histogram for the selected channel
            hdata = cv2.calcHist([channels[selected_channel]], [0], None, [pixmax - pixmin], [pixmin, pixmax])
        
        # Normalize and convert to list
        hdata = cv2.normalize(hdata, hdata).flatten().tolist()
        return hdata

    def hist2plot(hdata):
        plt.figure(figsize=(10, 6))
        
        # Plot each channel's histogram
        plt.plot(hdata[0], color='red', label='Red Channel')
        plt.plot(hdata[1], color='green', label='Green Channel')
        plt.plot(hdata[2], color='blue', label='Blue Channel')
        plt.plot(hdata[3], color='black', label='Gray Scale')
        
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

    def build_response(context):
        outputImage = OutputImage(value=context.image)
        Outputs = HistogramOutputs(outputImage=outputImage)
        histogramResponse = HistogramResponse(outputs=Outputs)
        histogramExecutor = HistogramExecutor(value=histogramResponse)
        executor = ConfigExecutor(value=histogramExecutor)
        packageConfigs = PackageConfigs(executor=executor)
        package = PackageHelper(packageModel=PackageModel, packageConfigs=packageConfigs)
        packageModel = package.build_model(context)
        return packageModel
    
    def run():

        pass




if "__main__" == __name__:
    Executor(sys.argv[1]).run()