# **Pre-Histogram**

## **Histogram (Component)**

The Histogram executor processes images to compute and visualize RGB and Grayscale histogram data. Histogram data represents the normalized frequency of pixel values within the image. The output data format is explained in the "Histogram Outputs" section. You can select the channels and pixel interval to be processed. Additionally, there is an option to plot the data as a Matplotlib image.

#### **Histogram Inputs:**
* [InputImage]: Image

#### **Histogram Outputs:**
* [OutputData]: List[List[float]] - 2D float array containing histogram data  
* [OutputImage]: Image - Optional plot output image

> **OutputData Format:** `List[List[float]]`  
`OutputData` contains four sub-arrays:  
- `red`: Red channel histogram data  
- `green`: Green channel histogram data  
- `blue`: Blue channel histogram data  
- `grayscale`: Grayscale channel histogram data  

**Channel Histogram Data Example:**  
`channelData` is a list of float values representing the normalized frequency of pixel values.  
For instance:  
`channelData[12]` indicates the probability that a pixel has a value of 12.

- `channelData[index]`: Probability that a pixel has a value of "index"  
- `channelData[x]`: Probability that a pixel has a value of "x"

> **Note:** If the pixel values are clamped using `pixelMin` and `pixelMax`, the `channelData` will have "0" for each index below the `pixelMin` value, and the list will end at the `pixelMax` index.

* **OutputImage Format:** Matplotlib graph

#### **Histogram Configurations:**
* [ConfigChannelRed]: Dropdown list - Enable/Disable  
* [ConfigChannelGreen]: Dropdown list - Enable/Disable  
* [ConfigChannelBlue]: Dropdown list - Enable/Disable  
* [ConfigChannelGrayScale]: Dropdown list - Enable/Disable  
* [ConfigPixelMin]: Text input - Integer value between 0 and 255  
* [ConfigPixelMax]: Text input - Integer value between 0 and 255  
* [ConfigPlotImage]: Dropdown list - Enable/Disable
