# AES impl with ARM instruction
AES-NI(AES New Instructions)是ARM指令中用于实现AES加解密的指令。<br>
* aes_key_expansion:用于生成AES扩展密钥，并将输入密钥复制到扩展密钥中。然后通过循环生成剩余的轮密钥。在每一轮中，该函数使用内联汇编函数__builtin_crypto_aesebsimc执行SubBytes操作，并使用当前轮密钥与前一轮密钥异或。生成的扩展密钥存储在expanded_key数组中。
* aes_encrypt_block:使用内联汇编函数__builtin_crypto_aesmc和__builtin_crypto_aesd执行AES块加密操作。块加密过程包括MixColumns、SubBytes和轮密钥的异或操作。
* aes_decrypt_block:使用内联汇编函数__builtin_crypto_aesimc和__builtin_crypto_aesd执行AES块解密操作。块解密过程与块加密过程类似，只是在解密时需要执行逆操作。

在main函数中，首先定义了输入密钥和明文块的示例。然后，通过调用aes_key_expansion函数生成扩展密钥。接下来，调用aes_encrypt_block函数对明文块进行加密，并将结果存储在ciphertext_block数组中。最后，调用aes_decrypt_block函数对密文块进行解密，并将结果存储在decrypted_block数组中。
代码输出加密后的密文和解密后的明文。<br>
* 密钥：{ 0x2b, 0x7e, 0x15, 0x16, 0x28, 0xae, 0xd2, 0xa6,0xab, 0xf7, 0x15, 0x88, 0x09, 0xcf, 0x4f, 0x3c };
* 明文：{ 0x32, 0x43, 0xf6, 0xa8, 0x88, 0x5a, 0x30, 0x8d,0x31, 0x31, 0x98, 0xa2, 0xe0, 0x37, 0x07, 0x34 };
运行结果<br>
![image](https://github.com/Ashl703/group-xx/assets/138503504/b9067eb4-d89b-41ee-9866-71f2c23c94ab)
