import numbers

from pydantic import Field, validator
from typing import List, Optional, Union, Any, Dict,Literal

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

class Percent(Config):
    """
        The image is resized preserving the aspect ratio.
    """
    name: Literal["Percent"] = "Percent"
    value: int = Field(ge=10, le=500, default=100)
    type: Literal["number"] = "number"
    field: Literal["textInput"] = "textInput"
    placeHolder: Literal["[10-500]"] = "[10-500]"
    class Config:
        title="Percentage (%)"

class ScalingInputs(Inputs):
    inputImage: InputImage


class ScalingConfigs(Configs):
    percent: Percent


class ScalingOutputs(Outputs):
    outputImage: OutputImage


class ScalingRequest(Request):
    inputs: Optional[ScalingInputs]
    configs: ScalingConfigs
    class Config:
        schema_extra = {
            "target": "configs"
        }


class ScalingResponse(Response):
    outputs: ScalingOutputs


class ScalingExecutor(Config):
    name: Literal["Scaling"] = "Scaling"
    value: Union[ScalingRequest, ScalingResponse]
    type: Literal["object"] = "object"
    field: Literal["option"] = "option"

    class Config:
        title = "Scaling"
        schema_extra = {
            "target": {
                "value": 0
            }
        }

class ConfigExecutor(Config):
    name: Literal["ConfigExecutor"] = "ConfigExecutor"
    value: Union[ScalingExecutor]
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
    name: Literal["Scaling"] = "Scaling"
    uID = "1221112"