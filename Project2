def Rho(n):
    x=random.random()
    h1=SM3(str(x))
    h2=SM3(str(h1))
    while 1:
        h1=SM3(str(h1))
        h2=SM3(str(SM3(h2)))
        if h1[:n]==h2[:n]:
            break
    return (h1[:n],h2[:n])

while 1:
        n = int(input("碰撞长度(字节)："))
        start = time.time()
        for i in range(15):
            Rho(n)
        end = time.time()
        runtime = (end - start) / 15
        print("用时：", runtime, "s")
        if n == 0:
            break
