import subprocess
import os

# A known working stream (small file)
url = "https://www.w3schools.com/html/mov_bbb.mp4"
cmd = ["mpv", "--no-video", "--ao=null", url]

print(f"Running: {' '.join(cmd)}")
process = subprocess.Popen(cmd, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
stdout, stderr = process.communicate()

print(f"Exit code: {process.returncode}")
print("Stderr output:")
print(stderr.decode())
