import numbers

from pydantic import Field, validator
from typing import List, Optional, Union, Any, Dict, Literal

from sdks.novavision.src.base.model import Package, Image, Param, Inputs, Configs, Outputs, Response, Request, Output, Input,Config

class InputImage(Input):
    name: Literal["inputImage"] = "inputImage"
    value: Union[List[Image],Image]
    type = "object"

    @validator("type", pre=True, always=True)
    def set_type_based_on_value(cls, value, values):
        value = values.get('value')
        if isinstance(value, Image):
            return "object"
        elif isinstance(value, list):
            return "list"
    class Config:
        title = "Image"

class OutputImage(Output):
    name: Literal["outputImage"] = "outputImage"
    value: Union[List[Image],Image]
    type = "object"

    @validator("type", pre=True, always=True)
    def set_type_based_on_value(cls, value, values):
        value = values.get('value')
        if isinstance(value, Image):
            return "object"
        elif isinstance(value, list):
            return "list"
    class Config:
        title = "Image"

class OutputData(Output):
    name: Literal["outputData"] = "outputData"
    value: List[List]
    type: Literal["list"] = "list"

class PixelMin(Config):
    name: Literal["PixelMin"] = "PixelMin"
    value: int = Field(ge=0, le=255, default=0)
    type: Literal["number"] = "number"
    field: Literal["textInput"] = "textInput"
    placeHolder: Literal["[0-255]"] = "[0-255]"
    class Config:
        title="Pixel Minimum Value"

class PixelMax(Config):
    name: Literal["PixelMax"] = "PixelMax"
    value: int = Field(ge=0, le=255, default=255)
    type: Literal["number"] = "number"
    field: Literal["textInput"] = "textInput"
    placeHolder: Literal["[0-255]"] = "[0-255]"
    class Config:
        title="Pixel Maximum Value"

class ChannelRed(Config):
    name: Literal["True"] = "True"
    value: Literal[True] = True
    type: Literal["bool"] = "bool"
    field: Literal["option"] = "option"
    class Config:
        title="Red Channel"

class ChannelGreen(Config):
    name: Literal["True"] = "True"
    value: Literal[True] = True
    type: Literal["bool"] = "bool"
    field: Literal["option"] = "option"
    class Config:
        title="Green Channel"

class ChannelBlue(Config):
    name: Literal["True"] = "True"
    value: Literal[True] = True
    type: Literal["bool"] = "bool"
    field: Literal["option"] = "option"
    class Config:
        title="Blue Channel"

class ChannelGrayScale(Config):
    name: Literal["True"] = "True"
    value: Literal[True] = True
    type: Literal["bool"] = "bool"
    field: Literal["option"] = "option"
    class Config:
        title="Gray Scale Channel"

class PlotImage(Config):
    name: Literal["False"] = "False"
    value: Literal[False] = False
    type: Literal["bool"] = "bool"
    field: Literal["option"] = "option"
    class Config:
        title="Generate Plot Image"

class HistogramInputs(Inputs):
    inputImage: InputImage

class HistogramMaskInputs(Inputs):
    inputImage: InputImage
    inputMask: InputImage

class HistogramOutputs(Outputs):
    outputData: OutputData
    outputImage: OutputImage

class HistogramConfigs(Configs):
    channelRed : ChannelRed
    channelGreen : ChannelGreen
    channelBlue : ChannelBlue
    channelGrayScale : ChannelGrayScale
    pixelMin : PixelMin
    pixelMax : PixelMax
    plotImage : PlotImage

class HistogramRequest(Request):
    inputs: Optional[HistogramInputs]
    configs: HistogramConfigs
    class Config:
        schema_extra = {
            "target": "configs"
        }

class HistogramMaskRequest(Request):
    inputs: Optional[HistogramMaskInputs]
    configs: HistogramConfigs
    class Config:
        schema_extra = {
            "target": "configs"
        }

class HistogramResponse(Response):
    outputs: HistogramOutputs

class HistogramExecutor(Config):
    """
        Image to histogram list by channels.
    """
    name: Literal["Histogram"] = "Histogram"
    value: Union[HistogramRequest, HistogramResponse]
    type: Literal["object"] = "object"
    field: Literal["option"] = "option"

    class Config:
        title = "Histogram"
        schema_extra = {
            "target": {
                "value": 0
            }
        }

class HistogramMaskExecutor(Config):
    """
        Image to histogram list by channels, with Mask.
    """
    name: Literal["Histogram"] = "Histogram"
    value: Union[HistogramMaskRequest, HistogramResponse]
    type: Literal["object"] = "object"
    field: Literal["option"] = "option"

    class Config:
        title = "HistograMask"
        schema_extra = {
            "target": {
                "value": 0
            }
        }

class ConfigExecutor(Config):
    name: Literal["ConfigExecutor"] = "ConfigExecutor"
    value: Union[HistogramExecutor, HistogramMaskExecutor]
    type: Literal["executor"] = "executor"
    field: Literal["dependentDropdownlist"] = "dependentDropdownlist"

    class Config:
        title = "Task"
        schema_extra = {
            "target": "value"
        }

class PackageConfigs(Configs):
    executor: ConfigExecutor

class PackageModel(Package):
    configs: PackageConfigs
    type: Literal["component"] = "component"
    name: Literal["Histogram"] = "Histogram"
    uID = "1221112"