# AES software implementation
主要利用numpy库实现AES加密矩阵
## 加密算法主要函数
* SubBytes(state)：实现S盒的字节替换作用
* ShiftRows(state)：实现行移位
* MixColumns(state)：实现列混淆
## 密钥扩展主要函数
* SubWord(byte):字节替换
* ExpandKey(key):密钥扩展<br>
## 运行结果
加密矩阵[[0x81,0x76,0x53,0x64],[0x00,0x00,0x00,0x00],[0x00,0x00,0x00,0x00],[0x00,0x00,0x00,0x00]]<br>
![image](https://github.com/Ashl703/group-xx/assets/138503504/8da774cf-0a0e-4cf2-91b7-c34a6257d02f)
