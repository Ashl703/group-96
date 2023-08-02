import secrets
from hashlib import sha256
from gmssl import sm3, func
A = 0
B = 7
P = 115792089237316195423570985008687907853269984665640564039457584007908834671663
N = 115792089237316195423570985008687907852837564279074904382605163141518161494337
G_X = 55066263022277343669578718895168534326250603453777594175500187360389116729240
G_Y = 32670510020758816978083085130507043184471273380659243275938904335757337482424
G = (G_X, G_Y)

#扩展欧几里得算法
def extended_euclidean_(a, b):
    if a == b:
        return (a, 1, 0)
    else:
        i = 0
        a_array = [a]
        b_array = [b]
        q_array = []
        r_array = []

        r0 = False

        while not (r0):
            q_array.append(b_array[i]//a_array[i])
            r_array.append(b_array[i]%a_array[i])
            b_array.append(a_array[i])
            a_array.append(r_array[i])
            i += 1
            if r_array[i-1] == 0:
                r0 = True
        i -= 1
        gcd = a_array[i]
        x_array = [1]
        y_array = [0]

        i -= 1
        total = i

        while i >= 0:
            y_array.append(x_array[total-i])
            x_array.append(y_array[total-i] - q_array[i]*x_array[total-i])
            i -= 1

        return (gcd, x_array[-1], y_array[-1])
#求模逆
def mod_inverse(j, n):
    (gcd, x, y) = extended_euclidean(j, n)

    if gcd == 1:
        return x%n
    else:
        return -1
#定义椭圆曲线上加法
def elliptic_add(p, q):
    if p == 0 and q == 0: return 0
    elif p == 0: return q
    elif q == 0: return p
    else:
        # Swap p and q if px > qx.
        if p[0] > q[0]:
            temp = p
            p = q
            q = temp
        r = []
        slope = (q[1] - p[1])*mod_inverse(q[0] - p[0], P) % P
        r.append((slope**2 - p[0] - q[0]) % P)
        r.append((slope*(p[0] - r[0]) - p[1]) % P)

        return (r[0], r[1])


def elliptic_double(p):
    r = []

    slope = (3*p[0]**2 + A)*mod_inverse(2*p[1], P) % P

    r.append((slope**2 - 2*p[0])%P)
    r.append((slope*(p[0] - r[0]) - p[1])%P)

    return (r[0], r[1])
#椭圆曲线上的乘法
def elliptic_multiply(s, p):
    n = p
    r = 0 # 无穷远点

    s_binary = bin(s)[2:] # 二进制转换
    s_length = len(s_binary)

    for i in reversed(range(s_length)):
        if s_binary[i] == '1':
            r = elliptic_add(r, n)
        n = elliptic_double(n)

    return r

def get_bit_num(x):
    if isinstance(x, int):
        num = 0
        tmp = x >> 64
        while tmp:
            num += 64
            tmp >>= 64
        tmp = x >> num >> 8
        while tmp:
            num += 8
            tmp >>= 8
        x >>= num
        while x:
            num += 1
            x >>= 1
        return num
    elif isinstance(x, str):
        return len(x.encode()) << 3
    elif isinstance(x, bytes):
        return len(x) << 3
    return 0
#预计算
def precompute(ID, a, b, G_X, G_Y, x_A, y_A):
    a = str(a)
    b = str(b)
    G_X = str(G_X)
    G_Y = str(G_Y)
    x_A = str(x_A)
    y_A = str(y_A)
    ENTL = str(get_bit_num(ID))

    joint = ENTL + ID + a + b + G_X + G_Y + x_A + y_A
    joint_b = bytes(joint, encoding='utf-8')
    digest = sm3.sm3_hash(func.bytes_to_list(joint_b))
    return int(digest, 16)

#密钥生成
def generate_key():
    private_key = int(secrets.token_hex(32), 16)
    public_key = elliptic_multiply(private_key, G)
    return private_key, public_key

#签名
def sign(private_key, message, Z_A):
    _M = Z_A + message
    _M_b = bytes(_M, encoding='utf-8')
    e = sm3.sm3_hash(func.bytes_to_list(_M_b))  # str
    e = int(e, 16)

    k = secrets.randbelow(P)
    random_point = elliptic_multiply(k, G)

    r = (e + random_point[0]) % N
    s = (mod_inverse(1 + private_key, N) * (k - r * private_key)) % N
    return (r, s)

#验证
def verify(public_key, ID, message, signature):
    r = signature[0]
    s = signature[1]

    Z = precompute(ID, A, B, G_X, G_Y, public_key[0], public_key[1])

    _M = str(Z) + message
    _M_b = bytes(_M, encoding='utf-8')
    e = sm3.sm3_hash(func.bytes_to_list(_M_b))  # str
    e = int(e, 16)
    t = (r + s) % N

    point = elliptic_multiply(s, G)
    point1 = elliptic_multiply(t, public_key)
    point = elliptic_add(point, point1)

    x1 = point[0]
    x2 = point[1]
    R = (e + x1) % N

    return R == r

if __name__ == '__main__':
    prikey, pubkey = generate_key()
    print('pk：', pubkey)
    message = input("message = ")
    ID = input("ID = ")
    Z_A = precompute(ID, A, B, G_X, G_Y, pubkey[0], pubkey[1])
    signature = sign(prikey, message, str(Z_A))
    print("sign: ", signature)
    if verify(pubkey, ID, message, signature) == 1:
        print('验证通过')
