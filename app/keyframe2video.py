# app/keyframe2video.py
import cv2
import os

def keyframes_to_video(
    input_dir="outputs/keyframes", 
    output_file="outputs/clips/video_stub.mp4", 
    fps=24,              # video framerate
    seconds_per_frame=2  # how long each keyframe lasts
):
    """Stitch keyframe PNGs into a simple video with hold duration."""

    files = sorted([f for f in os.listdir(input_dir) if f.endswith(".png")])
    if not files:
        print("No keyframes found in", input_dir)
        return

    first_frame = cv2.imread(os.path.join(input_dir, files[0]))
    height, width, _ = first_frame.shape

    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    fourcc = cv2.VideoWriter_fourcc(*"mp4v") # video codec
    out = cv2.VideoWriter(output_file, fourcc, fps, (width, height)) # creates an object that writes frames into an .mp4 file.

    frames_per_image = fps * seconds_per_frame

    for f in files:
        frame = cv2.imread(os.path.join(input_dir, f))
        for _ in range(frames_per_image):  # repeat frame to hold it
            out.write(frame)

    out.release()
    print(f" Video saved to {output_file}")


if __name__ == "__main__":
    keyframes_to_video()
