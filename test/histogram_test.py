import os
import cv2
import matplotlib.pyplot as plt
import numpy as np

def img2hist(image, channels=None, grayscale=False, pixmin=0, pixmax=255):
    out = [None, None, None, None]
    pixmax = max(pixmin, min(pixmax + 1, 256))
    pixmin = max(0, min(pixmin, pixmax))

    if channels:
        for channel in channels:
            if channel in [0, 1, 2]:  # Ensure valid channel index
                cvchannel = 2 - channel  # RGB to BGR mapping
                hist = cv2.calcHist([image], [cvchannel], None, [pixmax - pixmin], [pixmin, pixmax])
                hist = cv2.normalize(hist, hist).flatten().tolist()
                out[channel] = hist

    if grayscale:
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray_hist = cv2.calcHist([gray_image], [0], None, [pixmax - pixmin], [pixmin, pixmax])
        gray_hist = cv2.normalize(gray_hist, gray_hist).flatten().tolist()
        out[3] = gray_hist

    return out

def hist2plot(hdata):
    plt.figure(figsize=(8, 6))

    if hdata[0]:plt.plot(hdata[0], color='red', label='Red Channel')
    if hdata[1]:plt.plot(hdata[1], color='green', label='Green Channel')
    if hdata[2]:plt.plot(hdata[2], color='blue', label='Blue Channel')
    if hdata[3]:plt.plot(hdata[3], color='black', label='GrayScale')
    
    plt.ylim(0, 1)

    plt.title('Histogram')
    plt.xlabel('Pixel Intensity')
    plt.ylabel('Frequency')
    plt.legend()
    plt.grid(True)

    plt.tight_layout()
    canvas = plt.gca().figure.canvas
    canvas.draw()
    img = np.frombuffer(canvas.tostring_rgb(), dtype=np.uint8)
    img = img.reshape(canvas.get_width_height()[::-1] + (3,))
    img_bgr = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    plt.close()
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
        hdata = img2hist(image, channels=[0, 1, 2], grayscale=True)
        hist_img = hist2plot(hdata)

        # Display the original image and histogram
        cv2.imshow("Histogram", hist_img)

        # Wait for key press and close windows
        cv2.waitKey(0)
        cv2.destroyAllWindows()
