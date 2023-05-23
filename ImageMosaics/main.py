import argparse
from ImageMosaics import build_img_mosaics


def main(args):
    # Set the arguments
    main_img_path = args.main_img_path
    dataset_path = args.dataset_path
    crop_size = (args.crop_size, args.crop_size)
    save_res = args.save_res

    # Call the build_img_mosaics function with the specified arguments
    result = build_img_mosaics(main_img_path,
                               dataset_path,
                               crop_size=crop_size,
                               save_res=save_res)

    # Print the result or perform further actions
    print(f"New image shape is: {result.shape}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Image Mosaic Builder')

    # Add command-line arguments
    parser.add_argument('main_img_path', type=str,
                        help='Path to the main image')
    parser.add_argument('dataset_path', type=str,
                        help='Path to the dataset folder')
    parser.add_argument('--crop_size', type=int, default=20,
                        help='Crop size [default: (20) 20)]')
    parser.add_argument('--save_res', action='store_true',
                        help='Save the resulting image')

    # Parse the command-line arguments
    args = parser.parse_args()

    # Call the main function with the parsed arguments
    main(args)
