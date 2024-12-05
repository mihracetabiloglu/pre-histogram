# Histogram

This Python module processes images to compute and visualize RGB and Grayscale histograms. 
1. **Purpose**:  
   The `Histogram` class extracts histogram data for the RGB and Grayscale channels of an image. It allows users to specify pixel intensity ranges and optionally generates a histogram plot using Matplotlib.

2. **Features**:  
   - Computes normalized histograms for specified RGB channels (Red, Green, Blue) and Grayscale.  
   - Supports pixel intensity range customization (`pixelMin`, `pixelMax`).  
   - Optionally generates a visual plot of the histogram data and converts it into an image.  

3. **Core Functions**:  
   - **`img2hist`**: Calculates histograms for specified channels and Grayscale, normalizing the results.  
   - **`hist2plot`**: Visualizes the computed histograms using Matplotlib and converts the plot to an OpenCV-compatible image format.  

4. **Usage**:  
   - Pass an image and configuration parameters (e.g., selected channels, pixel intensity range) to the `Histogram` class.  
   - The `run` method processes the image, computes histogram data, and returns the results.  
   - If enabled, a histogram plot is generated as an image.

5. **Integration**:  
   Designed to be used within a larger application framework, it integrates with custom components for image processing, response building, and external configurations.