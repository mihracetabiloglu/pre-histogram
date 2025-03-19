import os
import sys
import cv2

sys.path.append(os.path.join(os.path.dirname(__file__), '../../../../'))

from sdks.novavision.src.media.image import Image
from sdks.novavision.src.base.model import Image as ImageModel
from sdks.novavision.src.base.response import Response
from sdks.novavision.src.base.component import Component
from sdks.novavision.src.helper.executor import Executor
from components.Histogram.src.utils.response import build_response
from components.Histogram.src.models.PackageModel import PackageModel


class Equalization(Component):
    """
    This executor applies histogram equalization to grayscale or RGB images
    using OpenCV's equalizeHist() function.
    """

    def __init__(self, request, bootstrap):
        super().__init__(request)
        self.request.model = PackageModel(**(self.request.data))
        self.initialize_request_data(request=request, bootstrap=bootstrap)
        self.image = self.request.get_param("inputImage")
        self.equalize_gray = self.request.get_param("configEqualizationGrayScale") == "True"
        self.equalize_rgb = self.request.get_param("configEqualizationRGB") == "True"
        self.plot_histogram = self.request.get_param("configPlotHistogram") == "True"

    @staticmethod
    def bootstrap() -> dict:
        return {}

    def run(self):
        img = Image.get_frame(img=self.image, redis_db=self.redis_db)
        if not img: return None

        processed_img = self.apply_equalization(img.value)
        output_image = Image.set_frame(img=Image(value=processed_img), package_uID=self.uID, redis_db=self.redis_db)
        packageModel = build_response(context=self)
        packageModel.outputs = {"outputImage": output_image}
        return Response(model=packageModel, bootstrap=self.bootstrap).response()

    def apply_equalization(self, image):
        if self.equalize_gray:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            equalized_gray = cv2.equalizeHist(gray)
            return cv2.cvtColor(equalized_gray, cv2.COLOR_GRAY2BGR)

        if self.equalize_rgb:
            img_yuv = cv2.cvtColor(image, cv2.COLOR_BGR2YUV)
            img_yuv[:, :, 0] = cv2.equalizeHist(img_yuv[:, :, 0])
            return cv2.cvtColor(img_yuv, cv2.COLOR_YUV2BGR)

        return image

if "__main__" == __name__:
    Executor(sys.argv[1]).run()