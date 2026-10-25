"""Video encoder args shared by montaje/quemar/unir. Set env QSV=1 to use the Intel Quick Sync hardware encoder (does not work on the i3-3220 of this PC).
Env ENC_PRESET (default veryfast) lets the long intermediate steps use ultrafast (about 2x faster, bigger files)."""
import os


def v(q):
    preset = os.environ.get("ENC_PRESET", "veryfast")
    if os.environ.get("QSV") == "1":
        return ["-c:v", "h264_qsv", "-global_quality", str(q), "-preset", "veryfast", "-pix_fmt", "nv12"]
    return ["-c:v", "libx264", "-preset", preset, "-crf", str(q), "-pix_fmt", "yuv420p"]