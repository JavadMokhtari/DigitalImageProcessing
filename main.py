from ColorImageSegmentation import segment_rust, accuracy
import os
import cv2


def main():
    # Define path to images and labels
    imgs_path = os.path.normpath("../dataset/images/")
    labels_path = os.path.normpath("../dataset/labels/")

    # Get the absolute path of the current module
    current_dir = os.path.abspath(os.path.dirname(__file__))

    # Change the current directory to the path of the current module
    os.chdir(current_dir)

    # Save all names of images in list
    rust_imgs = os.listdir(imgs_path)

    acc_list = list()

    # Segmentation images and calculate accuracy
    for image in rust_imgs:
        img_path = os.path.join(imgs_path, image)
        seg_img = segment_rust(img_path, save_output=True)

        # Load and Read Ground Truth image
        label_path = os.path.join(labels_path, image.split(".")[0] + ".png")
        gt_img_bgr = cv2.imread(label_path)
        # gt_img = cv2.cvtColor(gt_img_bgr, cv2.COLOR_BGR2RGB)

        # Calculate accuracy and store it
        acc = accuracy(seg_img, gt_img_bgr)
        acc_list.append(acc)

    # Calcualte average of accuracies as total accuracy
    total_accuracy = sum(acc_list) / len(acc_list)
    print(f"{len(acc_list)} images segmented!")
    print(f"The mean accuracy: {total_accuracy*100:.3f} %")


if __name__ == "__main__":
    main()
