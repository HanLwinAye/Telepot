import os

path = '/home/pi/Desktop/Telepot/Telepot/source/yinmayhnin/'
files = []
for r, d, f in os.walk(path):
    for file in f:
        if '.jpg' in file and '2020-05-11' in file:
            files.append(os.path.join(r, file))
            
for f in files:
    print(f)