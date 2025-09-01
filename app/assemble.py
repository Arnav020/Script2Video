# app assemble.py
import os
import glob
import ffmpeg

def assemble_video(
        clips_folder="outputs/clips/lipsync/",
        output_file="outputs/final_stub.mp4"
):
    """
    Stub: Concatenate all lipsync clips into one final video.
    No audio added yet.
    """

    os.makedirs(os.path.dirname(output_file),exist_ok=True)

    # Get all mp4 clips sorted
    clips = sorted(glob.glob(os.path.join(clips_folder,"*.mp4")))
    if not clips:
        print("No clips found in lipsync folder!")
        return
    
    # Write temporary file list for ffmpeg
    list_file = "temp_clips.txt"
    with open(list_file, "w") as f:
        for clip in clips:
            f.write(f"file '{clip}'\n")

    # Run ffmpeg concat
    ffmpeg.input(list_file,format="concat",safe=0).output(
        output_file, c="copy"
    ).run(overwrite_output=True)

    # Clean up
    os.remove(list_file)
    print(f"Final stub video saved to {output_file}")


if __name__=="__main__":
    assemble_video()