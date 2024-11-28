"""
Image to RGB channel histogram data.   
"""

import os
import cv2
import matplotlib.pyplot as plt

def img2histogram(image):
    """
    Load an image and compute histograms for the Red, Green, and Blue channels.
    
    Args:
        image (str): CV2 MatLike image file.
    
    Returns:
        dict: A dictionary containing histograms for 'red', 'green', and 'blue' channels.
    """
    
    if image is None: raise ValueError(f"Image not found")
    
    blue_channel, green_channel, red_channel = cv2.split(image)
    
    histogram_red = cv2.calcHist([red_channel], [0], None, [256], [0, 256])
    histogram_green = cv2.calcHist([green_channel], [0], None, [256], [0, 256])
    histogram_blue = cv2.calcHist([blue_channel], [0], None, [256], [0, 256])
    
    histogram_red = cv2.normalize(histogram_red, histogram_red).flatten()
    histogram_green = cv2.normalize(histogram_green, histogram_green).flatten()
    histogram_blue = cv2.normalize(histogram_blue, histogram_blue).flatten()
    
    return {
        'red': histogram_red,
        'green': histogram_green,
        'blue': histogram_blue
    }

def plot_histogram(histograms):
    """
    Plot the RGB histograms.
    
    Args:
        histograms (dict): Dictionary containing 'red', 'green', and 'blue' histograms.
    """
    plt.figure(figsize=(10, 6))
    
    # Plot each channel's histogram
    plt.plot(histograms['red'], color='red', label='Red Channel')
    plt.plot(histograms['green'], color='green', label='Green Channel')
    plt.plot(histograms['blue'], color='blue', label='Blue Channel')
    
    # Add labels and title
    plt.title('RGB Histogram')
    plt.xlabel('Pixel Intensity')
    plt.ylabel('Frequency')
    plt.legend()
    plt.grid(True)
    
    # Show the plot
    plt.show()

if __name__ == "__main__":
    script_dir = os.path.dirname(__file__)
    image_path = "../resources/yorkshire_terrier.jpg"
    relative_path = os.path.join(script_dir, image_path)
    image = cv2.imread(relative_path) 

    plot_histogram(img2histogram(image))
