def bin2hex(bin):
    if len(bin)%4:bin="".join(('0'*(4-len(bin)%4),bin))
    l=[]
    for i in range(0,len(bin),4):
        x=0
        if bin[i]=='1':x+=8
        if bin[i+1]=='1':x+=4
        if bin[i+2]=='1':x+=2
        if bin[i+3]=='1':x+=1
        if x<10:l.append(chr(x+48))
        else:l.append(chr(x+55))
    return"".join(l)