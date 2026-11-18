import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")
DST_DIR = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")

os.makedirs(DST_DIR, exist_ok=True)
if not os.path.isfile(SRC):
    raise SystemExit("entry.png missing next to main.py")
DST = os.path.join(DST_DIR, "entry.png")
shutil.copyfile(SRC, DST)
print("wrote", DST, os.path.getsize(DST), "bytes")
