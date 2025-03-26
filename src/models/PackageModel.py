from pydantic import Field, validator
from typing import List, Optional, Union, Literal

from sdks.novavision.src.base.model import Package, Image, Inputs, Configs, Outputs, Response, Request, Output, Input, Config

class InputImage(Input):
    name: Literal["inputImage"] = "inputImage"
    value: Union[List[Image], Image]
    type: str = "object"

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
    value: Union[List]
    type: Literal["list"] = "list"

class OutputImage(Output):
    name: Literal["outputImage"] = "outputImage"
    value: Union[List[Image],Image]
    type: str = "object"

    @validator("type", pre=True, always=True)
    def set_type_based_on_value(cls, value, values):
        value = values.get('value')
        if isinstance(value, Image):
            return "object"
        elif isinstance(value, list):
            return "list"

    class Config:
        title = "Image"

class ConfigChannelRedTrue(Config):
    name: Literal["configChannelRedTrue"] = "configChannelRedTrue"
    value: Literal["True"] = "True"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"
    class Config:
        title = "Enable"

class ConfigChannelRedFalse(Config):
    name: Literal["configChannelRedFalse"] = "configChannelRedFalse"
    value: Literal["False"] = "False"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"
    class Config:
        title = "Disable"

class ConfigChannelGreenTrue(Config):
    name: Literal["configChannelGreenTrue"] = "configChannelGreenTrue"
    value: Literal["True"] = "True"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"
    class Config:
        title = "Enable"

class ConfigChannelGreenFalse(Config):
    name: Literal["configChannelGreenFalse"] = "configChannelGreenFalse"
    value: Literal["False"] = "False"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"
    class Config:
        title = "Disable"

class ConfigChannelBlueTrue(Config):
    name: Literal["configChannelBlueTrue"] = "configChannelBlueTrue"
    value: Literal["True"] = "True"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"
    class Config:
        title = "Enable"

class ConfigChannelBlueFalse(Config):
    name: Literal["configChannelBlueFalse"] = "configChannelBlueFalse"
    value: Literal["False"] = "False"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"
    class Config:
        title = "Disable"

class ConfigChannelGrayScaleTrue(Config):
    name: Literal["configChannelGrayScaleTrue"] = "configChannelGrayScaleTrue"
    value: Literal["True"] = "True"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"
    class Config:
        title = "Enable"

class ConfigChannelGrayScaleFalse(Config):
    name: Literal["configChannelGrayScaleFalse"] = "configChannelGrayScaleFalse"
    value: Literal["False"] = "False"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"
    class Config:
        title = "Disable"

class ConfigChannelRed(Config):
    name: Literal["configChannelRed"] = "configChannelRed"
    value: Union[ConfigChannelRedTrue, ConfigChannelRedFalse]
    type: Literal["object"] = "object"
    field: Literal["dropdownlist"] = "dropdownlist"
    class Config:
        title = "Red Channel"

class ConfigChannelGreen(Config):
    name: Literal["configChannelGreen"] = "configChannelGreen"
    value: Union[ConfigChannelGreenTrue, ConfigChannelGreenFalse]
    type: Literal["object"] = "object"
    field: Literal["dropdownlist"] = "dropdownlist"
    class Config:
        title = "Green Channel"

class ConfigChannelBlue(Config):
    name: Literal["configChannelBlue"] = "configChannelBlue"
    value: Union[ConfigChannelBlueTrue, ConfigChannelBlueFalse]
    type: Literal["object"] = "object"
    field: Literal["dropdownlist"] = "dropdownlist"
    class Config:
        title = "Blue Channel"

class ConfigChannelGrayScale(Config):
    name: Literal["configChannelGrayScale"] = "configChannelGrayScale"
    value: Union[ConfigChannelGrayScaleTrue, ConfigChannelGrayScaleFalse]
    type: Literal["object"] = "object"
    field: Literal["dropdownlist"] = "dropdownlist"
    class Config:
        title = "Gray Scale Channel"

class ConfigPixelMin(Config):
    name: Literal["configPixelMin"] = "configPixelMin"
    value: int = Field(ge=0, le=255, default=0)
    type: Literal["number"] = "number"
    field: Literal["textInput"] = "textInput"
    placeHolder: Literal["[0-255]"] = "[0-255]"
    class Config:
        title="Pixel Minimum Value"

class ConfigPixelMax(Config):
    name: Literal["configPixelMax"] = "configPixelMax"
    value: int = Field(ge=0, le=255, default=255)
    type: Literal["number"] = "number"
    field: Literal["textInput"] = "textInput"
    placeHolder: Literal["[0-255]"] = "[0-255]"
    class Config:
        title="Pixel Maximum Value"

class ConfigPlotImageTrue(Config):
    name: Literal["configPlotImageTrue"] = "configPlotImageTrue"
    value: Literal["True"] = "True"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"
    class Config:
        title="Enable"

class ConfigPlotImageFalse(Config):
    name: Literal["configPlotImageFalse"] = "configPlotImageFalse"
    value: Literal["False"] = "False"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"
    class Config:
        title="Disable"

class ConfigPlotImage(Config):
    name: Literal["configPlotImage"] = "configPlotImage"
    value: Union[ConfigPlotImageTrue, ConfigPlotImageFalse]
    type: Literal["object"] = "object"
    field: Literal["dropdownlist"] = "dropdownlist"
    class Config:
        title = "Histogram Plot"


class ConfigConvertToGrayTrue(Config):
    name: Literal["configConvertToGrayTrue"] = "configConvertToGrayTrue"
    value: Literal["True"] = "True"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"

    class Config:
        title = "Convert to Grayscale: Yes"


class ConfigConvertToGrayFalse(Config):
    name: Literal["configConvertToGrayFalse"] = "configConvertToGrayFalse"
    value: Literal["False"] = "False"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"

    class Config:
        title = "Convert to Grayscale: No"


class ConfigConvertToGray(Config):
    name: Literal["convert_to_gray"] = "convert_to_gray"
    value: Union[ConfigConvertToGrayTrue, ConfigConvertToGrayFalse]
    type: Literal["object"] = "object"
    field: Literal["dropdownlist"] = "dropdownlist"

    class Config:
        title = "Convert To Grayscale"

class ConfigClipLimit(Config):
    name: Literal["clip_limit"] = "clip_limit"
    value: float
    type: Literal["number"] = "number"
    field: Literal["textInput"] = "textInput"

    class Config:
        title = "CLAHE Clip Limit"

class TileSize4x4(Config):
    name: Literal["tileSize4x4"] = "tileSize4x4"
    value: Literal["(4, 4)"] = "(4, 4)"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"

    class Config:
        title = "4 x 4"


class TileSize8x8(Config):
    name: Literal["tileSize8x8"] = "tileSize8x8"
    value: Literal["(8, 8)"] = "(8, 8)"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"

    class Config:
        title = "8 x 8"


class ConfigTileGridSize(Config):
    name: Literal["tile_grid_size"] = "tile_grid_size"
    value: Union[TileSize4x4, TileSize8x8]
    type: Literal["object"] = "object"
    field: Literal["dropdownlist"] = "dropdownlist"

    class Config:
        title = "Tile Grid Size"


class HistogramInputs(Inputs):
    inputImage: InputImage


class HistogramConfigs(Configs):
    configChannelRed : ConfigChannelRed
    configChannelGreen : ConfigChannelGreen
    configChannelBlue : ConfigChannelBlue
    configChannelGrayScale : ConfigChannelGrayScale
    configPixelMin : ConfigPixelMin
    configPixelMax : ConfigPixelMax
    configPlotImage : ConfigPlotImage

class HistogramOutputs(Outputs):
    outputData: OutputData
    outputImage: OutputImage

class HistogramRequest(Request):
    inputs: Optional[HistogramInputs]
    configs: HistogramConfigs
    class Config:
        json_schema_extra = {
            "target": "configs"
        }

class HistogramResponse(Response):
    outputs: HistogramOutputs


class EqualizationInputs(Inputs):
    inputImage: InputImage

class EqualizationConfigs(Configs):
    configClipLimit: ConfigClipLimit
    configTileGridSize: ConfigTileGridSize
    configConvertToGray: ConfigConvertToGray

class EqualizationOutputs(Outputs):
    outputImage: OutputImage

class EqualizationRequest(Request):
    inputs: Optional[EqualizationInputs]
    configs: EqualizationConfigs
    class Config:
        json_schema_extra = {
            "target": "configs"
        }

class EqualizationResponse(Response):
    outputs: EqualizationOutputs


class HistogramExecutor(Config):
    name: Literal["Histogram"] = "Histogram"
    value: Union[HistogramRequest, HistogramResponse]
    type: Literal["object"] = "object"
    field: Literal["option"] = "option"

    class Config:
        title = "Histogram"
        json_schema_extra = {
            "target": {
                "value": 0
            }
        }

class EqualizationExecutor(Config):
    name: Literal["Equalization"] = "Equalization"
    value: Union[EqualizationRequest, EqualizationResponse]
    type: Literal["object"] = "object"
    field: Literal["option"] = "option"
    class Config:
        title = "Equalization"
        json_schema_extra = {
            "target": {
                "value": 0
            }
        }

class ConfigExecutor(Config):
    name: Literal["ConfigExecutor"] = "ConfigExecutor"
    value: Union[HistogramExecutor,EqualizationExecutor]
    type: Literal["executor"] = "executor"
    field: Literal["dependentDropdownlist"] = "dependentDropdownlist"

    class Config:
        title = "Task"


class PackageConfigs(Configs):
    executor: ConfigExecutor

class PackageModel(Package):
    configs: PackageConfigs
    type: Literal["component"] = "component"
    name: Literal["Histogram"] = "Histogram"


