# Pointcloud Conversion Tools

This Docker image provides a set of tools for converting point cloud data between different formats. The tools included in this image facilitate the conversion from ROS bag files to PCD (Point Cloud Data), from PCD to BIN and from BIN to PNG. The image is built on top of the OSRF ROS Humble Desktop Full image.

## Setup

### Cloning the Repository

Clone this repository and navigate to it.

```bash	
git clone https://github.com/alunos-pfc/pointcloud_conversion_tools.git
cd pointcloud_conversion_tools
```

### Build the Docker Image

Build the Docker image using the following command:

```bash
docker build -t pointcloud_conversion_tools_ros2 Docker
```

### Run the Docker Container

To run the Docker container, utilize the provided run script with the following parameters:

```bash
./run.sh pointcloud_conversion_tools_ros2 [--rm] [--nvidia]
```

- `<image-name>`: The name you assigned to the Docker image during the build process.
- `--rm`: Automatically remove the container when it exits.
- `--nvidia`: Run the container with NVIDIA GPU support.

After running the container, a folder structure will be created within the repository directory. This folder structure will be used to store the point cloud data in the different formats. That folder will be linked to the `/root/pointcloud-files` directory within the container.

<pre>
pointcloud-files
├── bag-files
├── bin-files
├── pcd-files
├── video-files
└── png-files
    ├── depth
    └── reflectance
</pre>

## Pointcloud Conversion

### ROS Bag to PCD

To convert ROS bag files to PCD, we will use the rosbag2_to_pcd package.
We used the code from [rosbag2_to_pcd](https://github.com/xmfcx/rosbag2_to_pcd) by [xmfcx](https://github.com/xmfcx/).

Run the following command to convert the ROS bag file to PCD:

```bash
ros2 launch rosbag2_to_pcd rosbag2_to_pcd.launch.xml bag_path:=<bag-path> topic_name:=/topic_name output_folder:=<output-folder>
```

- `<bag-path>`: The path to the ROS2 bag file (put it in the `/root/pointcloud-files/bag-files` directory to access it both from within and outside the container).
- `/topic_name`: The name of the topic that contains the point cloud data. Default: `/velodyne_points`.
- `<output-folder>`: The path to the output folder. Default value: `/root/pointcloud-files/pcd-files/`, directory that can be accessed both from within and outside the container.

For more information, visit the [original repository](https://github.com/xmfcx/rosbag2_to_pcd)

### PCD to BIN

We used the code from [Tools_RosBag2KITTI](https://github.com/leofansq/Tools_RosBag2KITTI) by [leofansq](https://github.com/leofansq/).

The PCD to BIN conversion tool is available in the `pcd2bin` directory. Ensure that you have PCD files in the `/root/pointcloud-files/pcd-files/` directory before running the conversion.

```bash
cd /root/pcd2bin/CMakeFile
./pcd2bin
```

The BIN files will be saved in the `/root/pointcloud-files/bin-files/` directory, which can be accessed both from within and outside the container.

For more information, visit the [original repository](https://github.com/leofansq/Tools_RosBag2KITTI)

### BIN to PNG

This Docker image includes tools for convertind BIN files to PNG images.

The script is in the `Cloud2DImageConverter` directory. Navigate to it by running the following command:

```bash
cd /root/Cloud2DImageConverter
```

And run the following command to convert the PCD files to PNG:

```bash
python3 bin_to_png.py --data-path <input-folder> --results-path <output-folder>
```

Additional Parameters:

- `--batch-size`: Amount of data that will be loaded into memory in each iteration. Default is `500`.
- `--fov-up`: Field of view up parameter for projection. Default is `15.0`.
- `--fov-down`: Field of view down parameter for projection. Default is `-15.0`.
- `--width`: Width parameter for projection. Default is `512`.
- `--height`: Height parameter for projection. Default is `16`.
- `--is-label`: Boolean value indicating whether the data contains the label folder.

For more information, visit the [original repository](https://github.com/alunos-pfc/Cloud2DImageConverter)

### PNG images to MP4 video

The PNG images can be converted to MP4 video using pointcloud_to_image repository.

The script is in the `video_generator` directory. Navigate to it by running the following command:

```bash
cd /root/video_generator
```

And run the following command to convert the PNG files to MP4:

```bash
python3 create_video.py /root/pointcloud-files/png-files/reflectance --output_file /root/pointcloud-files/video-files/reflectance.mp4 --fps 24
```

Parameters

- `image_folder`: Path to the folder containing PNG images.
    - /root/pointcloud-files/png-files/`<val>`
- `--output_file` or `-o`: Output file name (default: output.mp4).
    - /root/pointcloud-files/video-files/`<val>`.mp4
- `--fps`: Frames per second (default: 12).