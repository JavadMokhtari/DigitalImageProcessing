from PIL import Image
import numpy as np
import glob
from scipy import spatial

def load_image(img_path, new_size: tuple[int, int]=None):
    """
    Load an image from the specified file path and resize it if desired.

    Args:
        * img_path (str): The file path of the image.
        * new_size (tuple[int, int], optional): The desired new size of the 
        image. Defaults to None.

    Returns:
        np.ndarray: The image loaded as a NumPy array.
    """

    # Open the image using PIL
    img = Image.open(img_path)
    # Convert the image to RGB mode if needed
    img = img.convert("RGB")
    # Resize the image if a new size is specified 
    if new_size:
        img = img.resize(new_size)
    # Convert the image to a NumPy array and return it
    return np.asarray(img)  



def build_img_mosaics(main_img_path: str, 
                        dataset_path: str, 
                        crop_size: tuple[int, int] = (20, 20),
                        save_res: bool = True):
    """
    Construct an image mosaic using a main image and a dataset of images.

    Args:
        main_img_path (str): The path to the main image.
        dataset_path (str): The path to the dataset folder.
        crop_size (tuple[int, int], optional): The desired crop size.
        save_res (bool, optional): Whether to save the resulting image.

    Returns:
        PIL.Image.Image: The image mosaic as a PIL Image object.
    """

    # Initialize an empty list to store the cropped images
    images = []

    for file in glob.glob(dataset_path + '/*'):
        # Load and resize the image using the specified crop size
        img = load_image(file, new_size=crop_size)
        # Append the resized image to the list of images
        images.append(img)

    # Convert the list of images to a NumPy array and return it
    images_arr = np.array(images)

    # Load main image that high resolution
    main_img = load_image(main_img_path)

    # Select every 10th pixel in both the row and column directions from the 
    # main_img array to create the template_img
    template_img = main_img[::10, ::10]

    image_values = np.apply_over_axes(np.mean, 
                            images_arr, (1,2)).reshape(images_arr.shape[0],3)

    # Create a KDTree from the image values
    tree = spatial.KDTree(image_values)
    # Initialize an array to store the matched indices
    image_idx = np.zeros(template_img.shape[:2], dtype=np.uint32)  

    for i in range(template_img.shape[0]):
        for j in range(template_img.shape[1]):
            # Get the template pixel value
            template = template_img[i, j]

            # Find the 5 closest matches to the template using the KDTree
            match = tree.query(template, k=5)

            # Randomly select one of the 5 matches
            pick = np.random.randint(5)
            
            # Store the selected match index in the corresponding position
            image_idx[i, j] = match[1][pick]

    # Create a new blank image canvas with the size calculated based on the 
    # template image dimensions and the crop size
    canvas = Image.new('RGB', (crop_size[1] * template_img.shape[1],
                            crop_size[0] * template_img.shape[0]))


    # Iterate over the rows and columns of the template image
    for i in range(template_img.shape[0]):
        for j in range(template_img.shape[1]):

            # Get the image array corresponding to the matched index at the 
            # current  position (i, j)
            arr = images_arr[image_idx[i, j]]
            
            # Calculate the coordinates for pasting the current image based on 
            # the current position and the crop size
            x, y = i * crop_size[0], j * crop_size[1]

            # Create a PIL image from the image array
            im = Image.fromarray(arr)

            # Paste the image onto the canvas at the calculated coordinates
            canvas.paste(im, (y, x))

    if save_res:
        # Save rebuilt image
        canvas.save("fruits.jpg")

    return canvas