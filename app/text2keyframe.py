# app/text2keyframe.py
from pathlib import Path
from typing import List, Tuple

def _wrap_text(text: str, max_chars: int = 42) -> List[str]:   #Breaks a long string into multiple lines of text
    words = text.split()
    lines, cur = [], []
    count = 0
    for w in words:
        if count + len(w) + (1 if cur else 0) > max_chars:
            lines.append(" ".join(cur))
            cur, count = [w], len(w)
        else:
            cur.append(w)
            count += len(w) + (1 if cur[:-1] else 0)
    if cur:
        lines.append(" ".join(cur))
    return lines

def generate_keyframes(
    script_path: str = "data/sample_script.txt",
    output_dir: str = "outputs/keyframes",
    size: Tuple[int, int] = (768, 432),
) -> List[str]:
    """
    Very first stub:
    - Reads a plain-text script (one scene per line).
    - Creates a simple placeholder image per scene with the scene text.
    - Saves PNGs to outputs/keyframes and returns their paths.

    Later we'll replace this with SDXL image generation.
    """
    from PIL import Image, ImageDraw, ImageFont

    script_file = Path(script_path)
    assert script_file.exists(), f"Script not found: {script_file}"

    out_dir = Path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    lines = [ln.strip() for ln in script_file.read_text(encoding="utf-8").splitlines() if ln.strip()]
    if not lines:
        raise ValueError("Script file is empty. Add at least one scene line.")

    saved_paths: List[str] = []
    W, H = size

    # Try to load a default font; fall back to PIL's built-in.
    try:
        font = ImageFont.truetype("arial.ttf", 22)
    except Exception:
        font = ImageFont.load_default()

    for idx, scene in enumerate(lines, start=1):
        img = Image.new("RGB", (W, H), color=(245, 245, 245))  # Creates a blank RBG image with light Gray background
        draw = ImageDraw.Draw(img)

        title = f"Scene {idx}"
        body_lines = _wrap_text(scene, max_chars=60)    # Wraps scene text into multiple lines

        # Title
        draw.text((24, 24), title, fill=(20, 20, 20), font=font)

        # Body text
        y = 70
        for bl in body_lines:
            draw.text((24, y), bl, fill=(40, 40, 40), font=font)  # writes wrapped text
            y += 28                                               # with some spacing

        out_path = out_dir / f"scene_{idx:02d}.png"
        img.save(out_path)
        saved_paths.append(str(out_path))

    return saved_paths

if __name__ == "__main__":
    paths = generate_keyframes()
    print("Generated keyframes:")
    for p in paths:
        print(" -", p)
