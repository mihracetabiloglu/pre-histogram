
from sdks.novavision.src.helper.package import PackageHelper
from components.Histogram.src.models.PackageModel import PackageModel, PackageConfigs, HistogramOutputs, HistogramResponse, HistogramExecutor, ConfigExecutor, OutputData, OutputImage

def build_response(context):
    outputData = OutputData(value=context.out)
    outputImage = OutputImage(value=context.image)
    Outputs = HistogramOutputs(outputData=outputData, outputImage=outputImage)
    histogramResponse = HistogramResponse(outputs=Outputs)
    histogramExecutor = HistogramExecutor(value=histogramResponse)
    executor = ConfigExecutor(value=histogramExecutor)
    packageConfigs = PackageConfigs(executor=executor)
    package = PackageHelper(packageModel=PackageModel, packageConfigs=packageConfigs)
    packageModel = package.build_model(context)
    return packageModel