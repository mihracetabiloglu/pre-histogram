import os
import cv2
import matplotlib.pyplot as plt
import numpy as np

def img2hist(image, channels=None, grayscale=False, pixmin=0, pixmax=255):
    """
    Compute the histogram for specified channels in an image or for grayscale.

    Args:
    image (np.ndarray): OpenCV image in BGR format.
    channels (list[int] | None): List of channel indices to compute histograms for (0=Red, 1=Green, 2=Blue).
    grayscale (bool): If True, computes the histogram for the grayscale version of the image.
    pixmin (int): Minimum pixel value (inclusive).
    pixmax (int): Maximum pixel value (exclusive).

    Returns:
    list[list[float]]: A list of normalized histogram values for each channel:
        - Index 0: Red
        - Index 1: Green
        - Index 2: Blue
        - Index 3: Grayscale
    """
    # Output structure: [R_hist, G_hist, B_hist, Gray_hist]
    out = [None, None, None, None]

    # Clamp pixel value range
    pixmax = max(pixmin, min(pixmax + 1, 256))
    pixmin = max(0, min(pixmin, pixmax))

    # Compute RGB channel histograms if channels are specified
    if channels:
        for channel in channels:
            if channel in [0, 1, 2]:  # Ensure valid channel index
                cvchannel = 2 - channel # RGB to BGR issues -> [0,1,2] to [2,1,0]
                hist = cv2.calcHist([image], [cvchannel], None, [pixmax - pixmin], [pixmin, pixmax])
                hist = cv2.normalize(hist, hist).flatten().tolist()
                out[channel] = hist

    # Compute grayscale histogram if requested
    if grayscale:
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray_hist = cv2.calcHist([gray_image], [0], None, [pixmax - pixmin], [pixmin, pixmax])
        gray_hist = cv2.normalize(gray_hist, gray_hist).flatten().tolist()
        out[3] = gray_hist

    return out

def hist2plot(hdata):
    plt.figure(figsize=(8, 6))
    
    # Plot each channel's histogram
    plt.plot(hdata[0], color='red',   label='Red Channel')
    plt.plot(hdata[1], color='green', label='Green Channel')
    plt.plot(hdata[2], color='blue',  label='Blue Channel')
    plt.plot(hdata[3], color='black', label='GrayScale')
    
    # Add labels and title
    plt.title('Histogram')
    plt.xlabel('Pixel Intensity')
    plt.ylabel('Frequency')
    plt.legend()
    plt.grid(True)
    
    # Save the figure to a numpy array
    plt.tight_layout()
    canvas = plt.gca().figure.canvas
    canvas.draw()
    
    # Convert to numpy array
    img = np.frombuffer(canvas.tostring_rgb(), dtype=np.uint8)
    img = img.reshape(canvas.get_width_height()[::-1] + (3,))
    
    # Convert to BGR for OpenCV compatibility
    img_bgr = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

    plt.close()  # Close the plt figure
    return img_bgr

if __name__ == "__main__":
    # Path to your image
    script_dir = os.path.dirname(__file__)
    image_path = "../resources/yorkshire_terrier.jpg"
    relative_path = os.path.join(script_dir, image_path)

    # Load the image
    image = cv2.imread(relative_path)

    if image is None:
        print("Image not found. Check the path!")
    else:
        # Compute histogram data and visualize it
        hdata = img2hist(image, channels=[0, 1, 2], grayscale=True, pixmin=0, pixmax=255)
        hist_img = hist2plot(hdata)

        # Display the original image and histogram
        cv2.imshow("Histogram", hist_img)

        # Wait for key press and close windows
        cv2.waitKey(0)
        cv2.destroyAllWindows()
