import os
import sys
import cv2
import json
import requests

sys.path.append(os.path.join(os.path.dirname(__file__),'../../../'))

from sdks.novavision.src.media.image import Image
from sdks.novavision.src.base.model import Image as ImageModel

from components.Histogram.src.models.PackageModel import PackageConfigs, ConfigExecutor, PackageModel, HistogramExecutor, HistogramInputs, HistogramConfigs, HistogramRequest, InputImage
from components.Histogram.src.models.PackageModel import ChannelRed, ChannelGreen, ChannelBlue, ChannelGrayScale, PixelMin, PixelMax, PlotImage
from components.Histogram.src.models.PackageModel import ChannelRedTrue, ChannelGreenTrue, ChannelBlueTrue, ChannelGrayScaleTrue, PlotImageTrue

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

    channelRedTrue = ChannelRedTrue(value="True")
    channelGreenTrue = ChannelGreenTrue(value="True")
    channelBlueTrue = ChannelBlueTrue(value="True")
    channelGrayScaleTrue = ChannelGrayScaleTrue(value="True")

    channelRed = ChannelRed(value=channelRedTrue)
    channelBlue = ChannelBlue(value=channelBlueTrue)
    channelGreen = ChannelGreen(value=channelGreenTrue)
    channelGrayScale = ChannelGrayScale(value=channelGrayScaleTrue)

    pixelMin = PixelMin(value=0)
    pixelMax = PixelMax(value=255)
    
    plotImageTrue = PlotImageTrue(value="True") 
    plotImage = PlotImage(value=plotImageTrue)

    histogramInputs = HistogramInputs(inputImage=inputImage)
    histogramConfigs = HistogramConfigs(channelRed=channelRed, channelGreen=channelGreen, channelBlue=channelBlue, channelGrayScale=channelGrayScale, pixelMin=pixelMin, pixelMax=pixelMax, plotImage=plotImage)
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