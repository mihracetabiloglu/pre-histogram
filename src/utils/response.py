
from sdks.novavision.src.helper.package import PackageHelper
from components.PreHistogram.src.models.PackageModel import PackageModel, PackageConfigs, HistogramExecutorOutputs, HistogramExecutorResponse, HistogramExecutor, EqualizationExecutor, EqualizationExecutorResponse, EqualizationExecutorOutputs, ConfigExecutor, OutputData, OutputImage, EnhancementExecutor, EnhancementExecutorResponse, EnhancementExecutorOutputs


def build_response_histogram(context):
    outputData = OutputData(value=context.out)
    outputImage = OutputImage(value=context.image)
    histogramExecutoroutputs = HistogramExecutorOutputs(outputData=outputData, outputImage=outputImage)
    istogramExecutorResponse = HistogramExecutorResponse(outputs=histogramExecutoroutputs)
    histogramExecutor = HistogramExecutor(value=istogramExecutorResponse)
    executor = ConfigExecutor(value=histogramExecutor)
    packageConfigs = PackageConfigs(executor=executor)
    package = PackageHelper(packageModel=PackageModel, packageConfigs=packageConfigs)
    packageModel = package.build_model(context)
    return packageModel


def build_response_equalization(context):
    outputImage = OutputImage(value=context.image)
    equalizationoutputs = EqualizationExecutorOutputs(outputImage=outputImage)
    equalizationResponse = EqualizationExecutorResponse(outputs=equalizationoutputs)
    equalizationExecutor = EqualizationExecutor(value=equalizationResponse)
    executor = ConfigExecutor(value=equalizationExecutor)
    packageConfigs = PackageConfigs(executor=executor)
    package = PackageHelper(packageModel=PackageModel, packageConfigs=packageConfigs)
    packageModel = package.build_model(context)
    return packageModel


def build_response_contrast_enhancement(context):
    outputImage = OutputImage(value=context.image)
    enhancementOutputs = EnhancementExecutorOutputs(outputImage=outputImage)
    enhancementResponse = EnhancementExecutorResponse(outputs=enhancementOutputs)
    enhancementExecutor = EnhancementExecutor(value=enhancementResponse)
    executor = ConfigExecutor(value=enhancementExecutor)
    packageConfigs = PackageConfigs(executor=executor)
    package = PackageHelper(packageModel=PackageModel, packageConfigs=packageConfigs)
    packageModel = package.build_model(context)
    return packageModel