FROM osrf/ros:humble-desktop-full

# Avoid keyboard interaction
ENV DEBIAN_FRONTEND=noninteractive

# Install dependencies
RUN apt update && apt install -y \
    git \
    nano \
    python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*
RUN pip install tqdm opencv-python

# Create a workspace for rosbag2_to_pcd
RUN git clone https://github.com/AIT-Assistive-Autonomous-Systems/ros2bag_tools.git /root/ros2bag_tools_ws/src/ros2bag_tools
WORKDIR /root/ros2bag_tools_ws

# Install dependencies
RUN /bin/bash -c "source /opt/ros/humble/setup.bash && \
                  apt update && \
                  rosdep install -y --from-paths src --ignore-src --rosdistro $ROS_DISTRO && \
                  rm -rf /var/lib/apt/lists/*"

# Build rosbag2_to_pcd
RUN /bin/bash -c "source /opt/ros/humble/setup.bash && \
                  colcon build --symlink-install --cmake-args -DCMAKE_BUILD_TYPE=RelWithDebInfo -DCMAKE_EXPORT_COMPILE_COMMANDS=1 && \
                  rm -rf /var/lib/apt/lists/*"

# Clone Tools_RosBag2KITTI repository and delete unnecessary files
RUN git clone https://github.com/leofansq/Tools_RosBag2KITTI.git /root/Tools_RosBag2KITTI && \
    mv /root/Tools_RosBag2KITTI/pcd2bin /root/pcd2bin && \
    rm -r /root/Tools_RosBag2KITTI && \
    rm -r /root/pcd2bin/pcd /root/pcd2bin/bin

# Change input pcd folder and the output bin folder path in pcd2bin.cpp
RUN sed -i 's|/home/cecilia/leo_projects/bishe2019/pcd2bin/bin/|/root/pointcloud-files/bin-files/|g' /root/pcd2bin/pcd2bin.cpp && \
    sed -i 's|/home/cecilia/leo_projects/bishe2019/pcd2bin/pcd/|/root/pointcloud-files/pcd-files/|g' /root/pcd2bin/pcd2bin.cpp

# Build pcd2bin
WORKDIR /root/pcd2bin/CMakeFile
RUN cmake .. && make

# Clone Cloud2DImageConverter repository
RUN git clone https://github.com/AIR-UFG/Cloud2DImageConverter.git /root/Cloud2DImageConverter
WORKDIR /root/Cloud2DImageConverter
RUN pip3 install -e '.[dev]'
# Copy the bin_to_png.py script to the container
COPY files/bin_to_png.py /root/Cloud2DImageConverter/bin_to_png.py 

RUN mkdir -p /root/video_generator
COPY files/create_video.py /root/video_generator/create_video.py

# Add ROS to path
RUN echo "source /opt/ros/humble/setup.bash" >> /root/.bashrc && \
    echo "source /root/ros2bag_tools_ws/install/setup.bash" >> /root/.bashrc

# Set working directory
WORKDIR /root