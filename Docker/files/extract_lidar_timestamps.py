import rclpy
from rclpy.node import Node
from rosbag2_py import SequentialReader, StorageOptions, ConverterOptions, StorageFilter
import argparse

def extract_lidar_timestamps(bag_file, topic_name, output_file):
    # Initialize ROS2 context
    rclpy.init()
    node = Node('extract_lidar_timestamps')

    # Set up the bag reader
    reader = SequentialReader()
    storage_options = StorageOptions(uri=bag_file, storage_id='sqlite3')
    converter_options = ConverterOptions(input_serialization_format='cdr', output_serialization_format='cdr')
    reader.open(storage_options, converter_options)

    # Set the topic filter using StorageFilter
    storage_filter = StorageFilter(topics=[topic_name])
    reader.set_filter(storage_filter)
    
    # Open the output file
    with open(output_file, 'w') as f:
        # Iterate through the bag and extract timestamps
        while reader.has_next():
            (topic, data, t) = reader.read_next()
            # Convert the timestamp (int in nanoseconds) to seconds
            timestamp = t * 1e-9
            f.write(f"{timestamp:.9e}\n")

    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Extract LiDAR timestamps from a ROS2 bag and save to a times.txt file.")
    
    parser.add_argument('bag_file', type=str, help="Path to the ROS2 bag file.")
    parser.add_argument('--topic_name', type=str, default='/velodyne_points', help="LiDAR topic name (default: /velodyne_points).")
    parser.add_argument('--output_file', type=str, default='times.txt', help="Output file name (default: times.txt).")
    
    args = parser.parse_args()
    
    # Extract timestamps using provided arguments
    extract_lidar_timestamps(args.bag_file, args.topic_name, args.output_file)
