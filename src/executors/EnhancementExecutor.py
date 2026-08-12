import os
import sys
import cv2
import numpy as np

sys.path.append(os.path.join(os.path.dirname(__file__), '../../../../'))

from sdks.novavision.src.media.image import Image
from sdks.novavision.src.base.component import Component
from sdks.novavision.src.helper.executor import Executor
from components.PreHistogram.src.utils.response import build_response_contrast_enhancement
from components.PreHistogram.src.models.PackageModel import PackageModel


class EnhancementExecutor(Component):
    """
    This class applies histogram normalization (linear stretching) similar to 
    GIMP's Auto Levels algorithm. It finds the min/max pixel values in the 
    image and linearly stretches them to the [0-255] range; it optionally 
    clips extreme values (clip_limit), increases or decreases the contrast 
    using a multiplier (contrast_multiplier), and applies brightness 
    normalization via midtone (gamma) correction (normalize_brightness).

    Attributes
    ----------
    request : object
        Request parameters.

    Methods
    -------
    apply_contrast_enhancement(image):
        Applies linear histogram stretching to the input image.
    """

    def __init__(self, request, bootstrap):
        super().__init__(request, bootstrap)
        self.request.model = PackageModel(**(self.request.data))
        self.image = self.request.get_param("inputImage")

        self.clip_limit = self._read_int_param("contrastClipLimit", default=0)
        self.contrast_multiplier = self._read_float_param("contrastMultiplier", default=1.0)
        self.normalize_brightness = self._read_bool_param("configNormalizeBrightness", default=False)

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

    def _read_float_param(self, param_name, default=0.0):
        raw_value = self._read_config_value(param_name)
        if raw_value is None:
            return default
        if isinstance(raw_value, str):
            try:
                return float(raw_value)
            except ValueError:
                return default
        return float(raw_value)

    def apply_contrast_enhancement(self, image):
        """
        Linear stretching is applied independently to each channel (BGR) for color images, 
        and to the single channel for grayscale images.
        """
        is_color = len(image.shape) == 3 and image.shape[2] >= 3

        if is_color:
            channels = list(cv2.split(image))
        else:
            channels = [image]

        stretched_channels = []
        for ch in channels:
            stretched_channels.append(self._stretch_channel(ch))

        if is_color:
            out = cv2.merge(stretched_channels[:3])
            if image.shape[2] == 4:
                out = cv2.merge([*cv2.split(out), channels[3]])
        else:
            out = stretched_channels[0]

        if self.normalize_brightness:
            out = self._apply_midtone(out, gamma=1.3)

        return out

    def _stretch_channel(self, channel):
        flat = channel.flatten().astype(np.float32)

        if self.clip_limit > 0:
            lower = np.percentile(flat, self.clip_limit)
            upper = np.percentile(flat, 100 - self.clip_limit)
        else:
            lower = float(flat.min())
            upper = float(flat.max())

        if upper <= lower:
            return channel.copy()

        stretched = (channel.astype(np.float32) - lower) / (upper - lower) * 255.0
        stretched = stretched * self.contrast_multiplier
        stretched = np.clip(stretched, 0, 255).astype(np.uint8)
        return stretched

    def _apply_midtone(self, image, gamma=1.3):
        inv_gamma = 1.0 / gamma
        table = np.array(
            [((i / 255.0) ** inv_gamma) * 255 for i in range(256)]
        ).astype(np.uint8)
        return cv2.LUT(image, table)

    def run(self):
        """
        Executes the contrast enhancement (linear histogram stretching) process.
        """
        img = Image.get_frame(img=self.image, redis_db=self.redis_db)
        img.value = self.apply_contrast_enhancement(img.value)
        self.image = Image.set_frame(img=img, package_uID=self.uID, redis_db=self.redis_db)
        packageModel = build_response_contrast_enhancement(context=self)
        return packageModel


if __name__ == "__main__":
    Executor(sys.argv[1]).run()