FROM osrf/ros:noetic-desktop-full

# Avoid keyboard interaction
ENV DEBIAN_FRONTEND=noninteractive

# Install dependencies
RUN apt update && apt install -y \
    git \
    python3-pip \
    libpcl-dev \
    python3-tk \
    python3-pcl \
    pcl-tools \
    && rm -rf /var/lib/apt/lists/*
RUN pip3 install numpy matplotlib tk

# Clone pointcloud_to_image repository
RUN git clone https://github.com/alunos-pfc/pointcloud_to_image.git /root/tools/pointcloud_to_image

# Clone Tools_RosBag2KITTI repository and delete unnecessary files
RUN git clone https://github.com/leofansq/Tools_RosBag2KITTI.git /root/tools/Tools_RosBag2KITTI && \
    mv /root/tools/Tools_RosBag2KITTI/pcd2bin /root/tools && \
    rm -r /root/tools/Tools_RosBag2KITTI && \
    rm -r /root/tools/pcd2bin/pcd /root/tools/pcd2bin/bin

# Change pcd and bin folders path in pcd2bin.cpp
RUN sed -i 's|/home/cecilia/leo_projects/bishe2019/pcd2bin/bin/|/root/pointcloud-files/bin-files/|g' /root/tools/pcd2bin/pcd2bin.cpp && \
    sed -i 's|/home/cecilia/leo_projects/bishe2019/pcd2bin/pcd/|/root/pointcloud-files/pcd-files/|g' /root/tools/pcd2bin/pcd2bin.cpp

# Build pcd2bin
WORKDIR /root/tools/pcd2bin/CMakeFile
RUN cmake .. && make

# Add ROS to path
RUN echo "source /opt/ros/noetic/setup.bash" >> /root/.bashrc

# Set working directory
WORKDIR /root