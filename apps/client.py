
import requests
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__),'../../../'))
import cv2
import json
from components.Histogram.src.models.PackageModel import PackageConfigs,ConfigExecutor,PackageModel,HistogramExecutor,HistogramInputs,HistogramConfigs,HistogramRequest,InputImage
from components.Histogram.src.models.PackageModel import ChannelRed, ChannelGreen, ChannelBlue, ChannelGrayScale, PixelMin, PixelMax, PlotImage

from sdks.novavision.src.base.model import Image,  Request
from sdks.novavision.src.media.image import Image as image

ENDPOINT_URL = "http://127.0.0.1:8000/api"

def infer():
    imread = cv2.imread("/opt/project/components/Histogram/resources/yorkshire_terrier.jpg")
    image_obj = Image(
        name="DemoImage",
        uID="001",
        mimeType="image/jpg",
        encoding="bytes",
        value=imread,
        type="Image"
    )
    image_obj = image.encode64(image_obj)
    inputImage = InputImage(value=image_obj)

    channelRed = ChannelRed(value=True)
    channelBlue = ChannelBlue(value=True)
    channelGreen = ChannelGreen(value=True)
    channelGrayScale = ChannelGrayScale(value=True)
    pixelMin = PixelMin(value=0)
    pixelMax = PixelMax(value=255)
    plotImage = PlotImage(value=True)

    histogramInputs = HistogramInputs(inputImage=inputImage)
    histogramConfigs = HistogramConfigs(channelRed=channelRed, channelGreen=channelGreen, channelBlue=channelBlue, channelGrayScale=channelGrayScale, pixelMin=pixelMin, pixelMax=pixelMax, plotImage=plotImage)
    histogramRequest =  HistogramRequest(inputs= histogramInputs, configs= histogramConfigs)
    histogramExecutor = HistogramExecutor(value= histogramRequest)
    executor = ConfigExecutor(value=histogramExecutor)
    packageConfigs = PackageConfigs(executor=executor)
    request = PackageModel(configs=packageConfigs, name="Histogram")

    request_json = json.loads(request.json())
    response = requests.post(ENDPOINT_URL, json = request_json)
    print(response.raise_for_status())
    print(response.json())


if __name__ =="__main__":
    infer()