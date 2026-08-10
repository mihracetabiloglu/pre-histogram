import os
import cv2
import matplotlib.pyplot as plt
import numpy as np

def img2hist(image, channels=None, grayscale=False, pixmin=0, pixmax=255):
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
    out = [[], [], [], []]

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

def hist2plot(hdata, channels:list=None, grayscale=False, pixmin=0, pixmax=255):
    plt.figure(figsize=(10, 6))

    plt.xlim(pixmin, pixmax)

    if pixmin > 0:
        for i in range(4):
            empty = [0] * pixmin
            hdata[i] = empty + hdata[i]

    # Plot each channel's histogram
    if channels.__contains__(0): plt.plot(hdata[0], color='red',   label='Red Channel')
    if channels.__contains__(1): plt.plot(hdata[1], color='lime', label='Green Channel')
    if channels.__contains__(2): plt.plot(hdata[2], color='blue',  label='Blue Channel')
    if grayscale: plt.plot(hdata[3], color='black', label='GrayScale')

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

if __name__ == "__main__":
    # Path to your image
    script_dir = os.path.dirname(__file__)
    image_path = "../resources/yorkshire_terrier.jpg"
    relative_path = os.path.join(script_dir, image_path)

    # Load the image
    image = cv2.imread(relative_path)

    if image is None:
        print("Image not found. Check the path!")
    else:
        channels = [0, 1, 2]
        grayscale = True
        pixmin = 0
        pixmax = 255

        # Compute histogram data and visualize it
        hdata = img2hist(image, channels=channels, grayscale=grayscale, pixmin=pixmin, pixmax=pixmax)
        hist_img = hist2plot(hdata, channels=channels, grayscale=grayscale, pixmin=pixmin, pixmax=pixmax)

        # Display the original image and histogram
        cv2.imshow("Histogram", hist_img)

        # Wait for key press and close windows
        cv2.waitKey(0)
        cv2.destroyAllWindows()


def test_histogram_reads_nested_boolean_config_values():
    import importlib.util
    import pathlib
    import sys
    import types

    def install_stub_modules():
        for name in ["sdks", "sdks.novavision", "sdks.novavision.src", "sdks.novavision.src.media", "sdks.novavision.src.base", "sdks.novavision.src.helper", "components", "components.PreHistogram", "components.PreHistogram.src", "components.PreHistogram.src.utils", "components.PreHistogram.src.models"]:
            if name not in sys.modules:
                sys.modules[name] = types.ModuleType(name)

        for name in ["sdks", "sdks.novavision", "sdks.novavision.src", "sdks.novavision.src.media", "sdks.novavision.src.base", "sdks.novavision.src.helper"]:
            module = sys.modules[name]
            module.__path__ = []

        image_module = types.ModuleType("sdks.novavision.src.media.image")

        class Image:
            @staticmethod
            def get_frame(**kwargs):
                return types.SimpleNamespace(value=kwargs.get("img"))

            @staticmethod
            def set_frame(**kwargs):
                return kwargs["img"]

        image_module.Image = Image
        sys.modules["sdks.novavision.src.media.image"] = image_module

        base_model_module = types.ModuleType("sdks.novavision.src.base.model")
        base_model_module.Image = object
        base_model_module.Package = object
        base_model_module.Inputs = object
        base_model_module.Configs = object
        base_model_module.Outputs = object
        base_model_module.Response = object
        base_model_module.Request = object
        base_model_module.Output = object
        base_model_module.Input = object
        base_model_module.Config = object
        sys.modules["sdks.novavision.src.base.model"] = base_model_module

        component_module = types.ModuleType("sdks.novavision.src.base.component")

        class Component:
            def __init__(self, request, bootstrap=None):
                self.request = request
                self.redis_db = None
                self.uID = None

            def initialize_request_data(self, request, bootstrap):
                return None

        component_module.Component = Component
        sys.modules["sdks.novavision.src.base.component"] = component_module

        executor_module = types.ModuleType("sdks.novavision.src.helper.executor")

        class Executor:
            def __init__(self, data):
                self.data = data

            def run(self):
                return None

        executor_module.Executor = Executor
        sys.modules["sdks.novavision.src.helper.executor"] = executor_module

        response_module = types.ModuleType("components.PreHistogram.src.utils.response")
        response_module.build_response_histogram = lambda context: {}
        sys.modules["components.PreHistogram.src.utils.response"] = response_module

        package_model_module = types.ModuleType("components.PreHistogram.src.models.PackageModel")

        class PackageModel:
            pass

        package_model_module.PackageModel = PackageModel
        sys.modules["components.PreHistogram.src.models.PackageModel"] = package_model_module

    install_stub_modules()

    module_path = pathlib.Path(__file__).resolve().parents[1] / "src" / "executors" / "Histogram.py"
    spec = importlib.util.spec_from_file_location("histogram_under_test", module_path)
    histogram_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(histogram_module)

    class DummyRequest:
        def __init__(self):
            self.data = {}

        def get_param(self, name):
            if name == "configChannelRed":
                return types.SimpleNamespace(value="True")
            if name == "configChannelGreen":
                return types.SimpleNamespace(value="False")
            if name == "configChannelBlue":
                return types.SimpleNamespace(value="True")
            if name == "configChannelGrayScale":
                return types.SimpleNamespace(value="False")
            if name == "configPixelMin":
                return 0
            if name == "configPixelMax":
                return 255
            if name == "configPlotImage":
                return types.SimpleNamespace(value="True")
            return None

    histogram = histogram_module.Histogram(DummyRequest(), bootstrap={})

    assert histogram.channelRed is True
    assert histogram.channelGreen is False
    assert histogram.channelBlue is True
    assert histogram.channelGrayScale is False
    assert histogram.plotImage is True
