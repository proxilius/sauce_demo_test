import logging
import cv2
import numpy as np
from PIL import Image, ImageChops
from io import BytesIO
import os

import pytest

project_folder = os.getcwd()

# Define the relative path to the desired folder
relative_folder_path = "log_files"

# Build the full path to the folder within the project
folder_path = os.path.join(project_folder, relative_folder_path)
logging.basicConfig(
    filename="logfile.txt",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

import logging


def assert_and_log(condition, message):
    logging.basicConfig(
        filename="logfile.txt",
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )
    try:
        assert condition
        logging.info(message + " PASSED")
    except AssertionError as e:
        logging.error(message + " FAILED" + f": {str(e)}")
        raise AssertionError(f"Assertion failed: {message}")


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
    threshold = 1  # You may need to adjust this threshold based on your needs
    print("MSE::: ", mse)
    # assert not (float(mse) > float(threshold))
    return float(mse) > float(threshold)


def log_assert(expected, actual, message=""):
    print(f"\nEXPECTED:  |  {expected}  |")
    print(f"ACTUAL:      |  {actual}    |")
    try:
        # assert expected == actual
        pytest.assume(expected == actual)
        if expected == actual:
            print(f"Assertion passed: {message}")
    except AssertionError as e:
        raise AssertionError(f"Assertion failed: {message}")
