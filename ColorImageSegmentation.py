import numpy as np
import cv2
import matplotlib.pyplot as plt
import os


def segment_rust(img_path: str,
                 save_output=False,
                 save_dir="../dataset/outputs/"):

    # OpenCV by default reads images in BGR format
    img_path = os.path.join(img_path)
    rust = cv2.imread(img_path)

    if rust is None:
        raise "Image is None!"

    # Convert to HSV space to segmentation
    rust_hsv = cv2.cvtColor(rust, cv2.COLOR_BGR2HSV)

    # Apply a threshold to the green channel to extract the leaves mask
    lower_leaf = np.array([30, 25, 25])
    upper_leaf = np.array([90, 255, 255])

    # Apply a threshold to the red channel to extract the rust pests mask
    lower_pest = np.array([90, 60, 30])
    upper_pest = np.array([130, 255, 255])

    rust_mask = cv2.inRange(rust_hsv, lower_leaf, upper_leaf)
    pest_mask = cv2.inRange(rust_hsv, lower_pest, upper_pest)

    # Create a black background image with the same size as the main image
    background = np.zeros(rust.shape, dtype=np.uint8)

    # Apply color image segmentation to the main image using the rust mask
    rust_color = (128, 0, 0)  # Red color
    rust_masked_img = cv2.bitwise_and(background, background, mask=rust_mask)
    rust_masked_img[rust_mask != 0] = rust_color

    # Apply color image segmentation to the main image using the pests mask
    pest_color = (0, 128, 0)  # Green color
    pest_masked_img = cv2.bitwise_and(background, background, mask=pest_mask)
    pest_masked_img[pest_mask != 0] = pest_color

    # Combine the segmented images
    color_segmented = cv2.add(rust_masked_img, pest_masked_img)
    green_and_red_idx = np.logical_and(np.array(pest_mask != 0),
                                       np.array(rust_mask != 0))
    color_segmented[green_and_red_idx] = rust_color

    if save_output:
        # Create directory if not exists
        if not os.path.exists(save_dir):
            os.mkdir(save_dir)

        # Get output file name to save
        file_name = img_path.split("/")[-1].split(".")[0]
        output_path = os.path.join(save_dir, file_name + ".png")

        # Save the combined segmented image
        cv2.imwrite(output_path, color_segmented)

    return pest_masked_img


# Calculate pixel-wise accuracy with having segmented image and ground truth
def accuracy(seg, gt):
    assert seg.shape == gt.shape, "Output and ground truth don't have same shape"
    correct_pixels = 0
    total_pixels = seg.shape[0] * seg.shape[1]
    for i in range(seg.shape[0]):
        for j in range(seg.shape[1]):
            if np.all(seg[i, j] == gt[i, j]):
                correct_pixels += 1
    accuracy = correct_pixels / total_pixels
    # print(f"Pixel-wise accuracy: {accuracy * 100:.3f} %")
    return accuracy


# Get the absolute path of the current module
current_dir = os.path.abspath(os.path.dirname(__file__))

# Change the current directory to the path of the current module
os.chdir(current_dir)
pest = segment_rust("../dataset/images/004461.JPG")
cv2.imshow("pest", pest)
cv2.waitKey(0)
