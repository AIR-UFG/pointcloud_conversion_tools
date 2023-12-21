# Pointcloud Conversion Tools

This Docker image provides a set of tools for converting point cloud data between different formats. The tools included in this image facilitate the conversion from ROS bag files to PCD (Point Cloud Data), from PCD to BIN, and from PCD to PNG. The image is built on top of the OSRF ROS Noetic Desktop Full image.

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
docker build -t pointcloud_conversion_tools Docker
```

### Run the Docker Container

To run the Docker container, utilize the provided run script with the following parameters:

```bash
./run.sh pointcloud_conversion_tools [--rm] [--nvidia]
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
    ├── height
    └── reflectance

</pre>

## Pointcloud Conversion

### ROS Bag to PCD

To convert ROS bag files to PCD, we will use the pcl_ros package. 

First, we need to run the ROS master node. This can be done by running the following command:

```bash
roscore
```

Then, open a new terminal and run the following command to enter the Docker container:

```bash
docker exec -it <container-name> bash
```

and run the following command to convert the ROS bag file to PCD:

```bash
rosrun pcl_ros bag_to_pcd <bag-file> /topic_name <output-folder>
```

- `<bag-file>`: The path to the ROS bag file (put it in the `/root/pointcloud-files/bag-files` directory to access it both from within and outside the container).
- `/topic_name`: The name of the topic that contains the point cloud data.
- `<output-folder>`: The path to the output folder (use the `/root/pointcloud-files/pcd-files` directory to access it both from within and outside the container).

### PCD to BIN

We used the code from [Tools_RosBag2KITTI](https://github.com/leofansq/Tools_RosBag2KITTI) by [leofansq](https://github.com/leofansq/).

The PCD to BIN conversion tool is available in the `pcd2bin` directory. Ensure that you have PCD files in the `/root/pointcloud-files/pcd-files/` directory before running the conversion.

```bash
cd /root/tools/pcd2bin/CMakeFile
./pcd2bin
```

The BIN files will be saved in the `/root/pointcloud-files/bin-files/` directory.

### PCD or BIN to PNG

Altoghout we are using our own repository, it was inspired by [lidar_projection](https://github.com/collector-m/lidar_projection) by [collector-m](https://github.com/collector-m).

This Docker image includes tools for convertind PCD or BIN files to PNG images.

The script is in the `pointcloud_to_image` directory. Navigate to it by running the following command:

```bash
cd /root/tools/pointcloud_to_image
```

And run the following command to convert the PCD files to PNG:

```bash
python3 run.py <input-folder> <output-folder> --val <val>
```

Parameters

- `input_folder`: Path to the input folder containing LiDAR files.
    - /root/pointcloud-files/pcd-files or /root/pointcloud-files/bin-files
- `output_folder`: Path to the output folder for saving images.
    - /root/pointcloud-files/png-files/`<val>`
- `--val`: Value to visualize (`depth`, `height`, or `reflectance`).

For more information, visit the [original repository](https://github.com/alunos-pfc/pointcloud_to_image)

### PNG images to MP4 video

The PNG images can be converted to MP4 video using pointcloud_to_image repository.

The script is in the `pointcloud_to_image` directory. Navigate to it by running the following command:

```bash
cd /root/tools/pointcloud_to_image
```

And run the following command to convert the PNG files to MP4:

```bash
python create_video.py /root/pointcloud-files/png-files/reflectance --output_file /root/pointcloud-files/video-files/reflectance.mp4 --fps 24
```

Parameters

- `image_folder`: Path to the folder containing PNG images.
    - /root/pointcloud-files/png-files/`<val>`
- `--output_file` or `-o`: Output file name (default: output.mp4).
    - /root/pointcloud-files/video-files/`<val>`.mp4
- `--fps`: Frames per second (default: 12).

For more information, visit the [original repository](https://github.com/alunos-pfc/pointcloud_to_image)