import os
import sys
import cv2
import json
import requests

sys.path.append(os.path.join(os.path.dirname(__file__),'../../../'))

from sdks.novavision.src.media.image import Image
from sdks.novavision.src.base.model import Image as ImageModel

from components.PreHistogram.src.models.PackageModel import PackageConfigs, ConfigExecutor, PackageModel, HistogramExecutor, HistogramInputs, HistogramConfigs, HistogramRequest, InputImage
from components.PreHistogram.src.models.PackageModel import ConfigChannelRed, ConfigChannelGreen, ConfigChannelBlue, ConfigChannelGrayScale, ConfigPixelMin, ConfigPixelMax, ConfigPlotImage
from components.PreHistogram.src.models.PackageModel import ConfigChannelRedTrue, ConfigChannelGreenTrue, ConfigChannelBlueTrue, ConfigChannelGrayScaleTrue, ConfigPlotImageTrue

ENDPOINT_URL = "http://127.0.0.1:8000/api"

def infer():
    imread = cv2.imread("/opt/project/components/Histogram/resources/yorkshire_terrier.jpg")
    image_obj = ImageModel(
        name="DemoImage",
        uID="001",
        mimeType="image/jpg",
        encoding="bytes",
        value=imread,
        type="Image"
    )
    image_obj = Image.encode64(image_obj)
    inputImage = InputImage(value=image_obj)

    channelRedTrue = ConfigChannelRedTrue(value="True")
    channelGreenTrue = ConfigChannelGreenTrue(value="True")
    channelBlueTrue = ConfigChannelBlueTrue(value="True")
    channelGrayScaleTrue = ConfigChannelGrayScaleTrue(value="True")

    channelRed = ConfigChannelRed(value=channelRedTrue)
    channelBlue = ConfigChannelBlue(value=channelBlueTrue)
    channelGreen = ConfigChannelGreen(value=channelGreenTrue)
    channelGrayScale = ConfigChannelGrayScale(value=channelGrayScaleTrue)

    pixelMin = ConfigPixelMin(value=0)
    pixelMax = ConfigPixelMax(value=255)
    
    plotImageTrue = ConfigPlotImageTrue(value="True")
    plotImage = ConfigPlotImage(value=plotImageTrue)

    histogramInputs = HistogramInputs(inputImage=inputImage)
    histogramConfigs = HistogramConfigs(configChannelRed=channelRed, configChannelGreen=channelGreen, configChannelBlue=channelBlue, configChannelGrayScale=channelGrayScale, configPixelMin=pixelMin, configPixelMax=pixelMax, configPlotImage=plotImage)
    histogramRequest =  HistogramRequest(inputs=histogramInputs, configs=histogramConfigs)
    histogramExecutor = HistogramExecutor(value=histogramRequest)
    executor = ConfigExecutor(value=histogramExecutor)
    packageConfigs = PackageConfigs(executor=executor)
    request = PackageModel(configs=packageConfigs, name="Histogram")

    request_json = json.loads(request.json())
    response = requests.post(ENDPOINT_URL, json=request_json)
    print(response.raise_for_status())
    print(response.json())

if __name__ =="__main__":
    infer()