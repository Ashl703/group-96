import hashlib
import hmac
import os
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import ec

def hmac_drbg(seed, m):
    v = b'\x01' * m
    k = b'\x00' * m
    k = hmac.new(k, seed + b'\x00' + m, hashlib.sha256).digest()
    v = hmac.new(k, v, hashlib.sha256).digest()
    k = hmac.new(k, seed + b'\x01' + m, hashlib.sha256).digest()
    v = hmac.new(k, v, hashlib.sha256).digest()
    while True:
        t = b''
        while len(t) < m:
            v = hmac.new(k, v, hashlib.sha256).digest()
            t += v
        yield t[:m]
        k = hmac.new(k, v + b'\x00', hashlib.sha256).digest()
        v = hmac.new(k, v, hashlib.sha256).digest()
        k = hmac.new(k, seed + b'\x01' + m, hashlib.sha256).digest()
        v = hmac.new(k, v, hashlib.sha256).digest()


def generate_sm2_key_pair():
    private_key = ec.generate_private_key(ec.SECP256K1())
    public_key = private_key.public_key()
    return private_key, public_key


def sm2_sign(private_key, message):
    z = int.from_bytes(hashlib.sha256(message).digest(), 'big')
    seck = private_key.private_numbers().private_value
    k = hmac_drbg(seck.to_bytes(32, 'big'), z.to_bytes(32, 'big'))
    while True:
        k_temp = next(k)
        if 0 < k_temp < private_key.curve.order:
            break
    p1 = private_key.curve.generator
    m = (z + k_temp) % private_key.curve.order
    s = ((m + seck * k_temp) * pow(1 + private_key.public_numbers().x, -1, private_key.curve.order)) % private_key.curve.order
    return k_temp, s


def sm2_verify(public_key, message, signature):
    curve = ec.SECP256K1()
    r, s = signature
    if not (0 < r < curve.order and 0 < s < curve.order):
        return False
    e = int.from_bytes(hashlib.sha256(message).digest(), 'big')
    t = (r + s) % curve.order
    if t == 0:
        return False
    p1 = public_key.public_numbers().curve.generator
    u1 = (e * pow(t, -1, curve.order)) % curve.order
    u2 = (r * pow(t, -1, curve.order)) % curve.order
    p = public_key.public_numbers().curve
    Q = ec.EllipticCurvePublicKey.from_encoded_point(p, p1.x, p1.y)
    point = u1 * p1 + u2 * Q
    if point.is_at_infinity():
        return False
    v = (point.x + r) % curve.order
    return v == r


private_key, public_key = generate_sm2_key_pair()
message = b"Hello, world!"
signature = sm2_sign(private_key, message)
valid = sm2_verify(public_key)
