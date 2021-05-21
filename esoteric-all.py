import dist.pyesoteric as pe
import dist.pyesotericesoteric as pee
import os

def esotericall(root):
    for i in os.listdir(root):
        src = os.path.abspath(os.path.join(root,i))
        if os.path.isfile(src):
            print("IN: "+src)
            with open(src, "r", encoding="utf-8") as f:
                code = f.read()
                dir = src.replace("\\", "/").split("/")
                fname = dir[-1][:-3]
                if len(dir) > 1:
                    dir = "/".join(dir[:-1])+"/"+fname+"/"
                else:
                    dir = fname+"/"
                if not os.path.exists(dir):
                    os.makedirs(dir)
                with open(dir+fname+"esoteric.py", "w") as o:
                    o.write(pe.encode(code))
                with open(dir+fname+"esoteric2.py", "w") as o:
                    o.write(pee.encode(code))
                print("OUT: "+dir)

DIST = "dist"
TEST = "test"
esotericall(DIST)
esotericall(TEST)