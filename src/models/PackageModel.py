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

class OutputData(Output):
    name: Literal["outputData"] = "outputData"
    value: List[List]
    type: Literal["list"] = "list"

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

class ChannelRedTrue(Config):
    name: Literal["ChannelRed"] = "ChannelRed"
    value: Literal["True"] = "True"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"
    class Config:
        title = "Enable Red Channel"

class ChannelRedFalse(Config):
    name: Literal["ChannelRed"] = "ChannelRed"
    value: Literal["False"] = "False"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"
    class Config:
        title = "Disable Red Channel"

class ChannelGreenTrue(Config):
    name: Literal["ChannelGreen"] = "ChannelGreen"
    value: Literal["True"] = "True"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"
    class Config:
        title = "Enable Green Channel"

class ChannelGreenFalse(Config):
    name: Literal["ChannelGreen"] = "ChannelGreen"
    value: Literal["False"] = "False"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"
    class Config:
        title = "Disable Green Channel"

class ChannelBlueTrue(Config):
    name: Literal["ChannelBlue"] = "ChannelBlue"
    value: Literal["True"] = "True"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"
    class Config:
        title = "Enable Blue Channel"

class ChannelBlueFalse(Config):
    name: Literal["ChannelBlue"] = "ChannelBlue"
    value: Literal["False"] = "False"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"
    class Config:
        title = "Disable Blue Channel"

class ChannelGrayScaleTrue(Config):
    name: Literal["ChannelGrayScale"] = "ChannelGrayScale"
    value: Literal["True"] = "True"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"
    class Config:
        title = "Enable Gray Scale Channel"

class ChannelGrayScaleFalse(Config):
    name: Literal["ChannelGrayScale"] = "ChannelGrayScale"
    value: Literal["False"] = "False"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"
    class Config:
        title = "Disable Gray Scale Channel"

class ChannelRed(Config):
    name: Literal["ConfigRed"] = "ConfigRed"
    value: Union[ChannelRedTrue, ChannelRedFalse]
    type: Literal["object"] = "object"
    field: Literal["dependentDropdownlist"] = "dependentDropdownlist"
    class Config:
        title = "Red Channel Configuration"

class ChannelGreen(Config):
    name: Literal["ConfigGreen"] = "ConfigGreen"
    value: Union[ChannelGreenTrue, ChannelGreenFalse]
    type: Literal["object"] = "object"
    field: Literal["dependentDropdownlist"] = "dependentDropdownlist"
    class Config:
        title = "Green Channel Configuration"

class ChannelBlue(Config):
    name: Literal["ConfigBlue"] = "ConfigBlue"
    value: Union[ChannelBlueTrue, ChannelBlueFalse]
    type: Literal["object"] = "object"
    field: Literal["dependentDropdownlist"] = "dependentDropdownlist"
    class Config:
        title = "Blue Channel Configuration"

class ChannelGrayScale(Config):
    name: Literal["ConfigGrayScale"] = "ConfigGrayScale"
    value: Union[ChannelGrayScaleTrue, ChannelGrayScaleFalse]
    type: Literal["object"] = "object"
    field: Literal["dependentDropdownlist"] = "dependentDropdownlist"
    class Config:
        title = "Gray Scale Channel Configuration"

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

class PlotImageTrue(Config):
    name: Literal["PlotImage"] = "PlotImage"
    value: Literal["True"] = "True"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"
    class Config:
        title="Enable"

class PlotImageFalse(Config):
    name: Literal["PlotImage"] = "PlotImage"
    value: Literal["False"] = "False"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"
    class Config:
        title="Disable"

class PlotImage(Config):
    name: Literal["ConfigLips"] = "ConfigLips"
    value: Union[PlotImageTrue, PlotImageFalse]
    type: Literal["object"] = "object"
    field: Literal["dependentDropdownlist"] = "dependentDropdownlist"
    class Config:
        title = "Histogram Plot"

class HistogramInputs(Inputs):
    inputImage: InputImage

class HistogramConfigs(Configs):
    channelRed : ChannelRed
    channelGreen : ChannelGreen
    channelBlue : ChannelBlue
    channelGrayScale : ChannelGrayScale
    pixelMin : PixelMin
    pixelMax : PixelMax
    plotImage : PlotImage

class HistogramOutputs(Outputs):
    outputData: OutputData
    outputImage: OutputImage

class HistogramRequest(Request):
    inputs: Optional[HistogramInputs]
    configs: HistogramConfigs
    class Config:
        schema_extra = {
            "target": "configs"
        }

class HistogramResponse(Response):
    outputs: HistogramOutputs

class HistogramExecutor(Config):
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

class ConfigExecutor(Config):
    name: Literal["ConfigExecutor"] = "ConfigExecutor"
    value: Union[HistogramExecutor]
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