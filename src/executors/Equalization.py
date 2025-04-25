import os
import sys
import cv2
import numpy as np

sys.path.append(os.path.join(os.path.dirname(__file__), '../../../../'))

from sdks.novavision.src.media.image import Image
from sdks.novavision.src.base.component import Component
from sdks.novavision.src.helper.executor import Executor
from components.Histogram.src.utils.response import build_response_equalization
from components.Histogram.src.models.PackageModel import PackageModel


class Equalization(Component):
    """
    This class applies CLAHE (Contrast Limited Adaptive Histogram Equalization) to an image.

    Attributes
    ----------
    request : object
        request parameters

    Methods
    -------
    apply_clahe():
        Applies CLAHE to the input image.
    """

    def __init__(self, request, bootstrap):
        super().__init__(request, bootstrap)
        self.request.model = PackageModel(**(self.request.data))
        self.image = self.request.get_param("inputImage")
        self.clip_limit = self.request.get_param("clip_limit")
        self.tile_grid_size = self._parse_tile_size(self.request.get_param("tile_grid_size"))


    @staticmethod
    def bootstrap(config: dict) -> dict:
        return {}

    def _parse_tile_size(self, tile_size_str):
        return tuple(map(int, tile_size_str.strip("()").split(",")))

    def apply_clahe(self, image):
        if len(image.shape) == 3 and image.shape[2] == 3:
            image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        if len(image.shape) != 2:
            raise ValueError("CLAHE uygulanacak görüntü tek kanallı olmalıdır!")

        if image.dtype != np.uint8:
            image = np.clip(image, 0, 255)
            image = image.astype(np.uint8)

        clahe = cv2.createCLAHE(clipLimit=self.clip_limit, tileGridSize=self.tile_grid_size)
        return clahe.apply(image)

    def run(self):
        """
        Executes the CLAHE histogram equalization process.
        """
        img = Image.get_frame(img=self.image, redis_db=self.redis_db)
        img.value = self.apply_clahe(img.value)
        self.image = Image.set_frame(img=img, package_uID=self.uID, redis_db=self.redis_db)
        packageModel = build_response_equalization(context=self)
        return packageModel


if __name__ == "__main__":
    Executor(sys.argv[1]).run()
