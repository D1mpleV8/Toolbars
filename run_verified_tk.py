import subprocess
import time
import os

print("Starting clean Xvfb session explicitly at DISPLAY=:99")
xvfb_proc = subprocess.Popen(["Xvfb", ":99", "-screen", "0", "1280x850x24"])
time.sleep(2)

print("Starting customized visual masterpiece with DISPLAY=:99 environment variable")
my_env = os.environ.copy()
my_env["DISPLAY"] = ":99"
py_proc = subprocess.Popen(["python3", "pc_toolbox/main.py"], env=my_env)
time.sleep(6)

print("Taking brand new sleek screenshot of the gorgeous UI")
subprocess.run(["scrot", "pc_toolbox_screenshot.png"], env=my_env)

print("Cleaning up display servers")
py_proc.terminate()
xvfb_proc.terminate()
time.sleep(1)
print("Finished!")
