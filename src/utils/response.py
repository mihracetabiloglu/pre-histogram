
from sdks.novavision.src.helper.package import PackageHelper
from components.PreHistogram.src.models.PackageModel import PackageModel, PackageConfigs, HistogramOutputs, HistogramResponse, HistogramExecutor, EqualizationExecutor, EqualizationResponse, EqualizationOutputs, ConfigExecutor, OutputData, OutputImage

def build_response_histogram(context):
    outputData = OutputData(value=context.out)
    outputImage = OutputImage(value=context.image)
    histogramoutputs = HistogramOutputs(outputData=outputData, outputImage=outputImage)
    histogramResponse = HistogramResponse(outputs=histogramoutputs)
    histogramExecutor = HistogramExecutor(value=histogramResponse)
    executor = ConfigExecutor(value=histogramExecutor)
    packageConfigs = PackageConfigs(executor=executor)
    package = PackageHelper(packageModel=PackageModel, packageConfigs=packageConfigs)
    packageModel = package.build_model(context)
    return packageModel


def build_response_equalization(context):
    outputImage = OutputImage(value=context.image)
    equalizationoutputs = EqualizationOutputs(outputImage=outputImage)
    equalizationResponse = EqualizationResponse(outputs=equalizationoutputs)
    equalizationExecutor = EqualizationExecutor(value=equalizationResponse)
    executor = ConfigExecutor(value=equalizationExecutor)
    packageConfigs = PackageConfigs(executor=executor)
    package = PackageHelper(packageModel=PackageModel, packageConfigs=packageConfigs)
    packageModel = package.build_model(context)
    return packageModel
