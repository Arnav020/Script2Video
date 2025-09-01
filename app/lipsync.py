# app/lipsync.py
import cv2
import os
import numpy as np

def fake_lipsync(
    input_dir="outputs/keyframes",
    audio_file="outputs/audio/dialogue_stub.wav",
    output_dir="outputs/clips/lipsync"    
):
    """
    Fake Lipsync stub:
    Just alternates between original frame and a darkened version to simulate mouth movemnet for each audio beep.
    """

    os.makedirs(output_dir, exist_ok=True)

    files = sorted([f for f in os.listdir(input_dir) if f.endswith(".png")])
    if not files:
        print("No keyframes found to lipsync.")
        return

    for idx,f in enumerate(files):
        frame = cv2.imread(os.path.join(input_dir, f))

        h, w, _=frame.shape
        mouth_area = frame.copy()
        cv2.rectangle(mouth_area, (w//3, 2*h//3),(2*w//3, 5*h//6),(0,0,0),-1)
        blended = cv2.addWeighted(frame,0.7,mouth_area,0.3,0)

        #Alternate frames: closed / open mouth
        frames = [frame, blended, frame, blended]

        out_path=os.path.join(output_dir,f"lipsync_{idx+1}.mp4")
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        out = cv2.VideoWriter(out_path, fourcc, 6,(w,h)) # 6 fps

        for fr in frames:
            out.write(fr)
        out.release()
        print(f"Fake lipsync clip saved to {out_path}")


if __name__=="__main__":
    fake_lipsync()