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

from sdks.novavision.src.helper.package import PackageHelper
from components.Histogram.src.models.PackageModel import PackageModel, PackageConfigs, HistogramOutputs, HistogramResponse, HistogramExecutor, ConfigExecutor, OutputImage

class Histogram(Component):
    def __init__(response, ):
        pass
    
    def img2hist(img, channel):
        pass

    def hist2plot(hdata):
        pass

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