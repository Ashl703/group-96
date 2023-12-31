#include <ctime>
#include <stdint.h>
#include <stdio.h>
#include <omp.h>

#define ROTATE_LEFT(x, n) (((x) << (n)) | ((x) >> (32 - (n))))
#define FF1(x, y, z) ((x) ^ (y) ^ (z))
#define GG1(x, y, z) (((x) & (y)) | ((x) & (z)) | ((y) & (z)))
#define P0(x) ((x) ^ ROTATE_LEFT((x), 9) ^ ROTATE_LEFT((x), 17))
#define P1(x) ((x) ^ ROTATE_LEFT((x), 15) ^ ROTATE_LEFT((x), 23))

#define GG2(x) (((x) & 0xFFFFFFFF) ^ ((x) >> 16))





void sm3_compress(uint32_t state[8], const uint8_t block[64]) {
    uint32_t w[68];
    uint32_t ww[64];
    uint32_t a, b, c, d, e, f, g, h;
    uint32_t ss1, ss2, tt1, tt2;
    int i;

    for (i = 0; i < 16; i++) {
        w[i] = (block[i * 4 + 0] << 24) |
            (block[i * 4 + 1] << 16) |
            (block[i * 4 + 2] << 8) |
            (block[i * 4 + 3]);
    }

    for (i = 16; i < 68; i++) {
        w[i] = P1(w[i - 16] ^ w[i - 9] ^ ROTATE_LEFT(w[i - 3], 15)) ^ ROTATE_LEFT(w[i - 13], 7) ^ w[i - 6];
    }
    for (i = 0; i < 64; i++) {
        ww[i] = w[i] ^ w[i + 4];
    }

    a = state[0];
    b = state[1];
    c = state[2];
    d = state[3];
    e = state[4];
    f = state[5];
    g = state[6];
    h = state[7];

#pragma omp parallel for private(i, ss1, ss2, tt1, tt2) shared(state)
    for (i = 0; i < 64; i++) {
        ss1 = ROTATE_LEFT(ROTATE_LEFT(a, 12) + e + ROTATE_LEFT(0x79CC4519, i), 7);
        ss2 = ss1 ^ ROTATE_LEFT(a, 12);
        tt1 = FF1(a, b, c) + d + ss2 + ww[i];
        tt2 = GG1(e, f, g) + h + ss1 + w[i];
        d = c;
        c = ROTATE_LEFT(b, 9);
        b = a;
        a = tt1;
        h = g;
        g = ROTATE_LEFT(f, 19);
        f = e;
        e = GG2(tt2);
    }

    state[0] ^= a;
    state[1] ^= b;
    state[2] ^= c;
    state[3] ^= d;
    state[4] ^= e;
    state[5] ^= f;
    state[6] ^= g;
    state[7] ^= h;
}

int main() {
    
    uint32_t state[8] = { 0x01234567, 0x89ABCDEF, 0xFEDCBA98, 0x76543210, 0xF0E1D2C3, 0x4B697474, 0x54686174, 0x7320 };
    uint8_t block[64] = { 0x01, 0x23, 0x45, 0x67, 0x89, 0xAB, 0xCD, 0xEF, 0xFE, 0xDC, 0xBA, 0x98, 0x76, 0x54, 0x32, 0x10,
                         0xF0, 0xE1, 0xD2, 0xC3, 0x4B, 0x69, 0x74, 0x74, 0x54, 0x68, 0x61, 0x74, 0x73, 0x20 };
    double start, end, duration;
    start = omp_get_wtime();
#pragma omp parallel for
//为了得到运行时间，循环1000次取平均
    for (int i = 0; i < 1000; i++) {
        sm3_compress(state, block);
    }
    end = omp_get_wtime();;
    duration = end - start;

    // 输出计算后的结果
    for (int i = 0; i < 8; i++) {
        printf("%08x ", state[i]);
    }
    printf("%f", duration / 1000);

    return 0;
}
