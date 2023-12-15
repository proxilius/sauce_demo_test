import logging
import cv2
import numpy as np
from PIL import Image, ImageChops
from io import BytesIO

logging.basicConfig(
    filename="logfile.txt",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


def assert_and_log(self, condition, message):
    try:
        assert condition
        self.logger.info(message + " PASSED")
    except AssertionError as e:
        self.logger.error(message + " FAILED" + f": {str(e)}")


# Function to capture a screenshot
def capture_screenshot(driver, filename):
    screenshot = driver.get_screenshot_as_png()
    screenshot = Image.open(BytesIO(screenshot))
    screenshot.save(filename)


def compare_screenshots(image1_path, image2_path):
    # Read the images
    image1 = cv2.imread(image1_path)
    image2 = cv2.imread(image2_path)

    # Convert images to grayscale
    gray_image1 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
    gray_image2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)

    # Compute Structural Similarity Index (SSI)
    h, w = gray_image1.shape
    diff = cv2.subtract(gray_image1, gray_image2)
    err = np.sum(diff**2)
    mse = err / (float(h * w))
    threshold = 0.9  # You may need to adjust this threshold based on your needs
    print("MSE::: ", mse, "DIFFF::::", diff)
    return mse > threshold
