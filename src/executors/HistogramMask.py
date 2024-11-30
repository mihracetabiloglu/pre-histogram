"""
Image to RGB channel histogram data.   
"""

import os
import sys
import cv2
import numpy as np

sys.path.append(os.path.join(os.path.dirname(__file__), '../../../../'))

from sdks.novavision.src.media.image import Image
from sdks.novavision.src.base.response import Response
from sdks.novavision.src.base.component import Component
from sdks.novavision.src.helper.executor import Executor
from components.Histogram.src.utils.response import build_response
from components.Histogram.src.models.PackageModel import PackageModel

class HistogramMask(Component):
    def __init__(response, ):
        pass
    
    def img2hist(img, channel):
        pass

    def hist2plot(hdata):
        pass
    
    def run():

        pass

if "__main__" == __name__:
    Executor(sys.argv[1]).run()