import random
import time
iv = 0x7380166f4914b2b9172442d7da8a0600a96f30bc163138aae38dee4db0fb0e4e
MAX = 2 ** 32

def StoB(msg):
    #字符串转比特串
    l=len(msg)
    s_dec=0
    for m in msg:
        s_dec=s_dec<<8
        s_dec+=ord(m)

    msg_bin=bin(s_dec)[2:].zfill(l*8)
    return msg_bin

def ItoB(a,k):
    #整数转比特串
    return bin(a)[2:].zfill(k)

def ItoH(a,k):
    #整数转16进制字符串
    return hex(a)[2:].zfill(k)

def BtoH(a,k):
    #比特串转16进制字符串
    return hex(int(a,2))[2:].zfill(k)

def fill(msg_bin):
    #消息填充
    l=len(msg_bin)
    k=448-(l+1)%512 #满足l+k+1=448mod512
    if k<0:
        k+=512
    l_bin=ItoB(l,64)
    msg_filled=msg_bin+'1'+'0'*k+l_bin
    return msg_filled

def Iteration_func(msg):
    #迭代函数
    #将填充后的消息每512比特分组
    n=len(msg)//512
    b=[]
    for i in range(n):
        b.append(msg[512*i:512*(i+1)])

    #迭代压缩
    v=[ItoB(iv,256)]
    for i in range(n):
        v.append(cf(v[i],b[i]))

    return BtoH(v[n],64)

def msg_extension(bi):
    #消息扩展
    w=[]
    for j in range(16):
        w.append(int(bi[j*32:(j+1)*32],2))

    for j in range(16,68):
        w_j=p1(w[j-16]^w[j-9]^move_left(w[j-3],15))^move_left(w[j-13],7)^w[j-6]
        w.append(w_j)

    w1=[]
    for j in range(64):
        w1.append(w[j]^w[j+4])

    return w,w1

def cf(vi,bi):
    #压缩函数

    w,w1=msg_extension(bi)

    t=[]
    for i in range(8):
        t.append(int(vi[i*32:(i+1)*32],2))
    a,b,c,d,e,f,g,h=t

    for j in range(64):
        ss1=move_left((move_left(a,12)+e+move_left(t_j(j),j))%MAX,7)
        ss2=ss1^move_left(a,12)
        tt1=(ff(a,b,c,j)+d+ss2+w1[j])%MAX
        tt2=(gg(e,f,g,j)+h+ss1+w[j])%MAX
        d=c
        c=move_left(b,9)
        b=a
        a=tt1
        h=g
        g=move_left(f,19)
        f=e
        e=p0(tt2)
    vi_1=ItoB(a,32)+ItoB(b,32)+ItoB(c,32)+ItoB(d,32)+ItoB(e,32)+ItoB(f,32)+ItoB(g,32)+ItoB(h,32)
    vi_1=int(vi_1,2)^int(vi,2)
    
    return ItoB(vi_1,256)

def move_left(a,k):
    #循环左移K比特

    k=k%32
    return((a<<k)&0xFFFFFFFF)|((a&0xFFFFFFFF)>>(32-k))

def p0(x):
    #置换函数p0

    return x^move_left(x,9)^move_left(x,17)

def p1(x):
    return x^move_left(x,15)^move_left(x,23)

def t_j(j):
    #常量
    if j<=15:
        return 0x79cc4519
    else:
        return 0x7a879d8a

def ff(x,y,z,j):
    #布尔函数
    if j<=15:
        return x^y^z
    else:
        return (x&y)|(x&z)|(y&z)

def gg(x,y,z,j):
    #布尔函数
    if j<=15:
        return x^y^z
    else:
        return (x&y)|((x^0xFFFFFFFF)&z)

def SM3(msg):

    s_bin=StoB(msg)
    s_fill=fill(s_bin)
    s_sm3=Iteration_func(s_fill)
    return s_sm3.upper().replace("L","")



def BirthdayAttack(n):
    while 1:
        x=random.random()
        y=random.random()
        h1=SM3(str(x))
        h2=SM3(str(y))
        if h1[:n]==h2[:n]:
            break
    return (h1[:n],h2[:n])


#s1="Ashley"
#s1_sm3=SM3(s1)
#print(s1_sm3)
while 1 :
    n=int(input("碰撞长度(字节)："))
    start=time.time()
    BirthdayAttack(n)
    end=time.time()
    runtime =end-start
    print("用时：",runtime,"s")
    if n==0:
        break
