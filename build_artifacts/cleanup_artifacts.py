import os
import glob
files = glob.glob(fr'{os.getcwd()}\logs\*.log')
for f in files:
    os.remove(f)
files = glob.glob(fr'{os.getcwd()}\screenshots\*.png')
for f in files:
    os.remove(f)
