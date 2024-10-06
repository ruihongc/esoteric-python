import dist.pyesoteric as pe
import dist.pyesotericesoteric as pee
import os

while (path := input("IN: ")):
    with open(path, "r", encoding="latin-1") as f:
        filename = os.path.splitext(os.path.basename(path))[0]
        folder = os.path.join(os.path.dirname(path), filename)
        if not os.path.exists(folder):
            os.makefolders(folder)

        code = f.read()
        with open(os.path.join(folder, filename+"esoteric.py"), "w") as o:
            encoded1 = pe.encode(code)
            assert (len(set(code)) <= 9) or (code == pe.decode(encoded1))
            o.write(encoded1)

        with open(os.path.join(folder, filename+"esoteric2.py"), "w") as o:
            encoded2 = pee.encode(code)
            assert (len(set(code)) <= 9) or (code == pee.decode(encoded2))
            o.write(encoded2)

        assert encoded1 == encoded2
        print("OUT: "+folder)

