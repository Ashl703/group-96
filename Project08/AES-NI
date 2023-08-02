#include <arm_acle.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>

#define AES_BLOCK_SIZE 16

// AES key expansion
void aes_key_expansion(const uint8_t* input_key, uint8_t* expanded_key) {
    // Copy input key to expanded key
    memcpy(expanded_key, input_key, AES_BLOCK_SIZE);

    // Generate remaining round keys
    for (int i = 1; i < 11; ++i) {
        const uint8_t temp[4] = { expanded_key[(i - 1) * 4 + 12],
                                 expanded_key[(i - 1) * 4 + 13],
                                 expanded_key[(i - 1) * 4 + 14],
                                 expanded_key[(i - 1) * 4 + 15] };

        // Rotate word
        uint32_t temp_word;
        memcpy(&temp_word, temp, sizeof(temp_word));
        temp_word = __builtin_bswap32(temp_word);
        temp_word = (temp_word >> 8) | (temp_word << 24);
        temp_word = __builtin_bswap32(temp_word);
        memcpy(expanded_key + i * 16, &temp_word, sizeof(temp_word));

        // SubBytes and XOR with round constant
        for (int j = 0; j < 4; ++j) {
            expanded_key[i * 16 + j] = __builtin_crypto_aesebsimc(expanded_key[i * 16 + j]);
        }

        expanded_key[i * 16 + 0] ^= expanded_key[(i - 1) * 16 + 0] ^ 0x1B;
        expanded_key[i * 16 + 1] ^= expanded_key[(i - 1) * 16 + 1];
        expanded_key[i * 16 + 2] ^= expanded_key[(i - 1) * 16 + 2];
        expanded_key[i * 16 + 3] ^= expanded_key[(i - 1) * 16 + 3];
    }
}

// AES block encryption
void aes_encrypt_block(const uint8_t* input_block, const uint8_t* expanded_key, uint8_t* output_block) {
    __builtin_crypto_aesmc();
    __builtin_crypto_aesd(aes_block, expanded_key);
}

// AES block decryption
void aes_decrypt_block(const uint8_t* input_block, const uint8_t* expanded_key, uint8_t* output_block) {
    __builtin_crypto_aesimc();
    __builtin_crypto_aesd(aes_block, expanded_key);
}

int main() {
    // Input key, plaintext, and ciphertext examples
    const uint8_t input_key[AES_BLOCK_SIZE] = { 0x2b, 0x7e, 0x15, 0x16, 0x28, 0xae, 0xd2, 0xa6,
                                               0xab, 0xf7, 0x15, 0x88, 0x09, 0xcf, 0x4f, 0x3c };

    const uint8_t plaintext_block[AES_BLOCK_SIZE] = { 0x32, 0x43, 0xf6, 0xa8, 0x88, 0x5a, 0x30, 0x8d,
                                                     0x31, 0x31, 0x98, 0xa2, 0xe0, 0x37, 0x07, 0x34 };

    uint8_t ciphertext_block[AES_BLOCK_SIZE];
    uint8_t decrypted_block[AES_BLOCK_SIZE];

    // Perform AES encryption
    uint8_t expanded_key[176];
    aes_key_expansion(input_key, expanded_key);
    aes_encrypt_block(plaintext_block, expanded_key, ciphertext_block);

    printf("Ciphertext: ");
    for (int i = 0; i < AES_BLOCK_SIZE; ++i) {
        printf("%02x ", ciphertext_block[i]);
    }
    printf("\n");

    // Perform AES decryption
    aes_decrypt_block(ciphertext_block, expanded_key, decrypted_block);

    printf("Decrypted Block: ");
    for (int i = 0; i < AES_BLOCK_SIZE; ++i) {
        printf("%02x ", decrypted_block[i]);
    }
    printf("\n");

    return 0;
}
