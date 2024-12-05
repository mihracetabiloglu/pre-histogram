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
    name: Literal["ChannelRedTrue"] = "ChannelRedTrue"
    value: Literal["True"] = "True"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"
    class Config:
        title = "Enable"

class ChannelRedFalse(Config):
    name: Literal["ChannelRedFalse"] = "ChannelRedFalse"
    value: Literal["False"] = "False"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"
    class Config:
        title = "Disable"

class ChannelGreenTrue(Config):
    name: Literal["ChannelGreenTrue"] = "ChannelGreenTrue"
    value: Literal["True"] = "True"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"
    class Config:
        title = "Enable"

class ChannelGreenFalse(Config):
    name: Literal["ChannelGreenFalse"] = "ChannelGreenFalse"
    value: Literal["False"] = "False"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"
    class Config:
        title = "Disable"

class ChannelBlueTrue(Config):
    name: Literal["ChannelBlueTrue"] = "ChannelBlueTrue"
    value: Literal["True"] = "True"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"
    class Config:
        title = "Enable"

class ChannelBlueFalse(Config):
    name: Literal["ChannelBlueFalse"] = "ChannelBlueFalse"
    value: Literal["False"] = "False"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"
    class Config:
        title = "Disable"

class ChannelGrayScaleTrue(Config):
    name: Literal["ChannelGrayScaleTrue"] = "ChannelGrayScaleTrue"
    value: Literal["True"] = "True"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"
    class Config:
        title = "Enable"

class ChannelGrayScaleFalse(Config):
    name: Literal["ChannelGrayScaleFalse"] = "ChannelGrayScaleFalse"
    value: Literal["False"] = "False"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"
    class Config:
        title = "Disable"

class ChannelRed(Config):
    name: Literal["ConfigRed"] = "ConfigRed"
    value: Union[ChannelRedTrue, ChannelRedFalse]
    type: Literal["object"] = "object"
    field: Literal["dependentDropdownlist"] = "dependentDropdownlist"
    class Config:
        title = "Red Channel"

class ChannelGreen(Config):
    name: Literal["ConfigGreen"] = "ConfigGreen"
    value: Union[ChannelGreenTrue, ChannelGreenFalse]
    type: Literal["object"] = "object"
    field: Literal["dependentDropdownlist"] = "dependentDropdownlist"
    class Config:
        title = "Green Channel"

class ChannelBlue(Config):
    name: Literal["ConfigBlue"] = "ConfigBlue"
    value: Union[ChannelBlueTrue, ChannelBlueFalse]
    type: Literal["object"] = "object"
    field: Literal["dependentDropdownlist"] = "dependentDropdownlist"
    class Config:
        title = "Blue Channel"

class ChannelGrayScale(Config):
    name: Literal["ConfigGrayScale"] = "ConfigGrayScale"
    value: Union[ChannelGrayScaleTrue, ChannelGrayScaleFalse]
    type: Literal["object"] = "object"
    field: Literal["dependentDropdownlist"] = "dependentDropdownlist"
    class Config:
        title = "Gray Scale Channel"

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
    name: Literal["PlotImageFalse"] = "PlotImageFalse"
    value: Literal["False"] = "False"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"
    class Config:
        title="Disable"

class PlotImage(Config):
    name: Literal["PlotImage"] = "PlotImage"
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