```markdown
# Image Mosaic Builder

Image Mosaic Builder is a Python script that constructs an image mosaic by rebuilding a given main image using a dataset of smaller images.

## Prerequisites

- Python 3.x
- Required Python libraries: `numpy`, `PIL`, `scipy`

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/JavadMokhtari/DigitalImageProcessing.git
   ```
change directory to `ImageMosaics` folder:

   ```bash
   cd ./ImageMosaics
   ```
2. Install the required Python libraries:

   ```bash
   pip install numpy Pillow scipy argparse
   ```

## Usage

1. Place your main image file in a suitable format (e.g., JPEG, PNG) in the specified directory.

2. Prepare a dataset folder containing a collection of images. Each image in the dataset will be used as a tile in the mosaic.

3. Run the script with the following command:

   ```bash
   python main.py /PATH/TO/main_image.jpg /PATH/TO/dataset_folder --crop_size 15 --save_res False
   ```

   Replace `/PATH/TO/main_image.jpg` with the path to your main image file, and `/PATH/TO/dataset_folder` with the path to your dataset folder. The `--crop_size` option specifies the desired size of the cropped tiles (default: 20), and the `--save_res` option indicates whether to save the resulting image.

4. The script will generate the image mosaic using the provided main image and dataset. If the `--save_res` option is specified, the resulting image will be saved as `mosaic.jpg` in the current directory. Otherwise, the resulting image will be displayed.

## Example

Here's an example of how to create an image mosaic using the provided main image and dataset:

```bash
python main.py fruit_background.jpg ../fruits --crop_size 20 --save_res True
```

## License

This project is licensed under the [MIT License](LICENSE).

## Acknowledgements

This project is inspired by the concept of image mosaics and makes use of various Python libraries.

## References

- [PIL (Python Imaging Library) Documentation](https://pillow.readthedocs.io/)
- [NumPy Documentation](https://numpy.org/doc/)
- [SciPy Documentation](https://docs.scipy.org/doc/)

```