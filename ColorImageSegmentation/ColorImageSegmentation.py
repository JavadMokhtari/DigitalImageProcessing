import numpy as np
import cv2
import os


def segment_rust(img_path: str,
                 save_output=False,
                 save_dir="../dataset/outputs/"):

    # OpenCV by default reads images in BGR format
    img_path = os.path.join(img_path)
    rust = cv2.imread(img_path)

    if rust is None:
        raise ValueError("Image is None!")

    # Convert to HSV space to segmentation
    rust_hsv = cv2.cvtColor(rust, cv2.COLOR_RGB2HSV)

    # Apply a threshold to the green channel to extract the leaves mask
    lower_leaf = np.array([30, 25, 25])
    upper_leaf = np.array([90, 255, 255])

    # Apply a threshold to the red channel to extract the rust pests mask
    lower_pest = np.array([90, 60, 30])
    upper_pest = np.array([130, 255, 255])

    rust_mask = cv2.inRange(rust_hsv, lower_leaf, upper_leaf)
    pest_mask = cv2.inRange(rust_hsv, lower_pest, upper_pest)

    # Create a black background image with the same size as the main image
    background = np.zeros_like(rust, dtype=np.uint8)

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
        os.makedirs(save_dir, exist_ok=True)

        # Get output file name to save
        file_name = img_path.split("/")[-1].split(".")[0]
        output_path = os.path.join(save_dir, file_name + ".png")

        # Save the combined segmented image
        img_to_write = cv2.cvtColor(color_segmented, cv2.COLOR_RGB2BGR)

        cv2.imwrite(output_path, img_to_write)

    return color_segmented


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
