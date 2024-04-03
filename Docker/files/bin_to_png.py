import argparse
import os
import shutil
from Cloud2DImageConverter import api

def parse_args():
    parser = argparse.ArgumentParser(description="Cloud2DImageConverter")

    parser.add_argument("--data-path", type=str, default="/root/pointcloud-files/bin-files",
                        help="Path containing the velodyne and labels folders")
    parser.add_argument("--results-path", type=str, default="/root/pointcloud-files/png-files",
                        help="Path where the results will be saved")
    parser.add_argument("--batch-size", type=int, default=500,
                        help="Amount of data that will be loaded into memory in each iteration")
    parser.add_argument("--fov-up", type=float, default=15.0,
                        help="Field of view up parameter for projection")
    parser.add_argument("--fov-down", type=float, default=-15.0,
                        help="Field of view down parameter for projection")
    parser.add_argument("--width", type=int, default=512,
                        help="Width parameter for projection")
    parser.add_argument("--height", type=int, default=16,
                        help="Height parameter for projection")
    parser.add_argument("--is-label", action="store_true",
                        help="Boolean value indicating whether the data contains the label folder")

    return parser.parse_args()

def main():
    args = parse_args()

    # Extracting the folder name
    folder_name = os.path.basename(args.data_path)
    
    # Extracting the path to the parent directory
    parent_dir = os.path.dirname(args.data_path)
    
    # Rename the folder containing the .bin files to 'velodyne'
    os.rename(args.data_path, os.path.join(parent_dir, "velodyne"))
    
    try:
        # Call the api.run() function
        api.run(data_path=parent_dir+'/',
                results_path=args.results_path+'/',
                batch_size=args.batch_size,
                fov_up=args.fov_up,
                fov_down=args.fov_down,
                width=args.width,
                height=args.height,
                is_label=args.is_label)
    finally:
        # Rename the 'velodyne' folder back to its original name
        os.rename(os.path.join(parent_dir, "velodyne"), os.path.join(parent_dir, folder_name))

if __name__ == "__main__":
    main()