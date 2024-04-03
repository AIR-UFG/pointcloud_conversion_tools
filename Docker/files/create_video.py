import cv2
import os
import argparse

def images_to_video(image_folder, output_file=None, fps=12):
    # Get all PNG files from the specified folder
    images = [img for img in os.listdir(image_folder) if img.endswith(".png")]
    images.sort()

    if not images:
        print("No PNG images found in the specified folder.")
        return

    # Read the first image to get dimensions
    first_image = cv2.imread(os.path.join(image_folder, images[0]))
    height, width, _ = first_image.shape

    # Define the codec and create a VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    output_file = output_file or os.path.join(image_folder, "output.mp4")

    out = cv2.VideoWriter(output_file, fourcc, fps, (width, height))

    # Write each image to the video file
    for image in images:
        img_path = os.path.join(image_folder, image)
        frame = cv2.imread(img_path)
        out.write(frame)

    out.release()
    print(f"Video saved as {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert PNG images to video or GIF.")
    parser.add_argument("image_folder", help="Path to the folder containing PNG images")
    parser.add_argument("-o", "--output_file", help="Output file name (default: first image name)")
    parser.add_argument("--fps", type=int, default=12, help="Frames per second (default: 12)")

    args = parser.parse_args()
    images_to_video(args.image_folder, args.output_file, args.fps)
