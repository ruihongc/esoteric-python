def decode(src):
    src = src.split("\n")[60][3:-1]
    c={'(':0,')':1,'=':2,'c':3,'e':4,'x':5,'%':6}
    return ''.join(chr(c[src[i]]+c[src[i+1]]*7+c[src[i+2]]*7*7)for i in range(0,len(src),3))

def encode(source):
    var = {
        43: "e",
        "prog": "xx",
        "template": "xe",
        1: "cc",
        2: "ce",
        4: "cx",
        8: "ec",
        16: "ee",
        32: "ex",
        64: "xc",
        3: "ccc",
        "data": "x",
        "translator": "c"
    }
    used = ["ccc"]
    namespaces = []
    ns_count = 0
    for i in range(3, 6):
        for j in range(3**i):
            var_name = ""
            for _ in range(i):
                var_name += "cex"[j%3]
                j //= 3
            if not var_name in used:
                namespaces.append(var_name)

    if len(set(source)) <= 9:
        return source

    unpacker = '''exec(''.join(chr({0}[{1}[i]]+{0}[{1}[i+1]]*7+{0}[{1}[i+2]]*7*7)for i in range(0,len({1}),3)))'''.format(var["translator"], var["data"])
    charset = sorted(list(set(unpacker+"{}f")))
    codepoints = map(ord, charset)

    output = (
        "{}='%c%%c%%%%c%%%%%%%%c%%%%%%%%%%%%%%%%c%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%c'\n".format(var["template"]) +
        "{0}=()==()\n".format(var[1]) +
        "{}=''==()\n".format(var[4]) +
        (
            "exec('{0}=%x%%x%%%%x%%%%%%%%x%%%%%%%%%%%%%%%%x'%{2}%{1}%{2}%{1}%{2})\n" +
            "exec('{0}%%%%%%%%%%%%%%%%=%x%%x%%%%x%%%%%%%%x'%{2}%{2}%{2}%{2})\n" +
            "exec('{0}%%%%=%x%%x'%{2}%{2})\n"
        ).format(var[3], var[4], var[1]) +
        (
            "exec('{1}=%x%%x'%{0}%{1})\n" +
            "exec('{1}%%%%=%x%%x'%{2}%{0})\n"
        ).format(var[3], var[4], var[1]) +
        "exec('{0}=%x%%x'%{1}%{2})\n".format(var[43], var[4], var[3])
    )

    for x in [2, 4, 8, 16, 32, 64]:
        output += "exec('{0}={1}%c{1}'%{2})\n".format(var[x], var[x/2], var[43])

    for c in codepoints:
        if c in var:
            continue

        var[c] = namespaces[ns_count]
        ns_count += 1

        rem = c
        pows = []
        while rem:
            pows.append(rem&-rem)
            rem -= rem&-rem

        front = "exec('{}={}".format(var[c], var[pows.pop()])
        back = "'"
        if len(pows) >= 5:
            for i, p in enumerate(pows[:3]):
                front += "%"*(2**i) + "c" + var[p]
                back += "%" + var[43]
            output += front + back + ")\n"
            front = "exec('{}%c={}".format(var[c], var[pows.pop()])
            back = "'%{}".format(var[43])
            for i, p in enumerate(pows[3:]):
                front += "%"*(2**(i+1)) + "c" + var[p]
                back += "%" + var[43]
        else:
            for i, p in enumerate(pows):
                front += "%"*(2**i) + "c" + var[p]
                back += "%" + var[43]

        output += front + back + ")\n"

    i = 0
    length = len(unpacker)

    output += "{}='".format(var["prog"])

    while unpacker[i] in "()exc=%":
        output += unpacker[i]
        i += 1
    output += "'\n"

    while (length-i) >= 6:
        u, v, w, x, y, z = [var[ord(unpacker[i+j])] for j in range(6)]
        output += "exec('{}%c={}%%{}%%{}%%{}%%{}%%{}%%{}'%{})\n".format(var["prog"], var["template"], u, v, w, x, y, z, var[43])
        i += 6

    if i < length:
        output += "exec('''{}%c=('".format(var["prog"])
        while i < length:
            output += unpacker[i]
            i += 1
        output += "')'''%{})\n".format(var[43])

    output += var["data"] + "='"

    ct = {0:'(',1:')',2:'=',3:'c',4:'e',5:'x',6:'%'}
    output += "".join(ct[ord(c)%7]+ct[ord(c)//7%7]+ct[ord(c)//49%7] for c in source)
    output += "'\n"
    output += "exec('''{}=%c'(':{}=={},')':{},'=':{},'c':{},'e':{},'x':{}%%c{},'%%%%%%%%%%%%%%%%':{}%%%%c{}%%%%%%%%c'''%{}%{}%{}%{})\n".format(var['translator'], var[43], var["data"], var[1], var[2], var[3], var[4], var[4], var[1], var[4], var[2], var[ord('{')], var[43], var[43], var[ord('}')]);

    output += "exec({})".format(var["prog"])

    return output
