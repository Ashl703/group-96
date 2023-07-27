.section .text
.global aes_encrypt

@ 输入参数:
@ r0 = 加密密钥（128位）
@ r1 = 输入数据（128位）
@ 输出结果:
@ r1 = 加密后的数据

aes_encrypt:
    push {r4-r11, lr}   @ 保存寄存器

    vld1.8      d0, [r0]     @ 导入密钥
    vld1.8      d1, [r1]     @ 导入数据

    vdup.32     q12, d0[0]   @ 生成轮密钥0
    vdup.32     q13, d0[1]   @ 生成轮密钥1
    vdup.32     q14, d0[2]   @ 生成轮密钥2
    vdup.32     q15, d0[3]   @ 生成轮密钥3

    @ 初始加/解密轮
    vadd.i32    q1, q1, q12   @ 加/解密数据的第一轮密钥
    vadd.i32    q2, q2, q13   @ 加/解密数据的第二轮密钥
    vadd.i32    q3, q3, q14   @ 加/解密数据的第三轮密钥
    vadd.i32    q4, q4, q15   @ 加/解密数据的第四轮密钥

    @ 轮函数
    mov         r4, #9       @ 进行9轮加/解密
1:
    vaeseq      q5, q1, q0   @ AES加/解密-SubBytes、ShiftRows、MixColumns
    vaesmc      q5, q5       @ AES加/解密-SubBytes、ShiftRows、MixColumns

    vaeseq      q6, q2, q0   @ AES加/解密-SubBytes、ShiftRows、MixColumns
    vaesmc      q6, q6       @ AES加/解密-SubBytes、ShiftRows、MixColumns

    vaeseq      q7, q3, q0   @ AES加/解密-SubBytes、ShiftRows、MixColumns
    vaesmc      q7, q7       @ AES加/解密-SubBytes、ShiftRows、MixColumns

    vaeseq      q8, q4, q0   @ AES加/解密-SubBytes、ShiftRows、MixColumns
    vaesmc      q8, q8       @ AES加/解密-SubBytes、ShiftRows、MixColumns

    vdup.32     q12, d0[4]   @ 生成下一轮密钥
    vdup.32     q13, d0[5]   @ 生成下一轮密钥
    vdup.32     q14, d0[6]   @ 生成下一轮密钥
    vdup.32     q15, d0[7]   @ 生成下一轮密钥

    vadd.i32    q1, q1, q12  @ 加/解密数据的下一轮密钥
    vadd.i32    q2, q2, q13  @ 加/解密数据的下一轮密钥
    vadd.i32    q3, q3, q14  @ 加/解密数据的下一轮密钥
    vadd.i32    q4, q4, q15  @ 加/解密数据的下一轮密钥

    subs        r4, r4, #1   @ 减少轮数计数器
    bne         1b           @ 继续下一轮加/解密

    @ 最后一轮-没有MixColumns
    vaeseq      q5, q1, q0   @ AES加/解密-SubBytes、ShiftRows
    vaesmc      q5, q5       @ AES加/解密-SubBytes、ShiftRows

    vaeseq      q6, q2, q0   @ AES加/解密-SubBytes、ShiftRows
    vaesmc      q6, q6       @ AES加/解密-SubBytes、ShiftRows

    vaeseq      q7, q3, q0   @ AES加/解密-SubBytes、ShiftRows
    vaesmc      q7, q7       @ AES加/解密-SubBytes、ShiftRows

    vaeseq      q8, q4, q0   @ AES加/解密-SubBytes、ShiftRows
    vaesmc      q8, q8       @ AES加/解密-SubBytes、ShiftRows

    vdup.32     q12, d0[10]  @ 最后一轮密钥
    vdup.32     q13, d0[11]  @ 最后一轮密钥
    vdup.32     q14, d0[12]  @ 最后一轮密钥
    vdup.32     q15, d0[13]  @ 最后一轮密钥

    vadd.i32    q1, q1, q12  @ 加/解密数据的最后一轮密钥
    vadd.i32    q2, q2, q13  @ 加/解密数据的最后一轮密钥
    vadd.i32    q3, q3, q14  @ 加/解密数据的最后一轮密钥
    vadd.i32    q4, q4, q15  @ 加/解密数据的最后一轮密钥

    vst1.8      d1, [r1]     @ 导出加密/解密结果

    pop {r4-r11, lr}    @ 恢复寄存器
    bx lr               @ 返回
