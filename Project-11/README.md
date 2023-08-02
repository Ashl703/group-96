# impl-sm2-with-RFC6979
## RFC6979
RFC 6979是一项定义了确定性签名算法（Deterministic Signature Algorithm，DSA）的标准。RFC 6979提出了一种基于哈希函数（如SHA-256）和伪随机函数的方法来生成确定性随机数。此处RFC6979用来以一种“确定性”方式产生k值，k=SHA256(sk+SM3(M)),其中sk为私钥，M为消息。
## sm2
sm2是一种椭圆曲线公钥密码算法。
首先定义了椭圆曲线的参数<br>
定义的函数：<br>
* extended_euclidean()扩展欧几里得算法
* mod_inverse()模逆运算
* elliptic_add()椭圆曲线加
* elliptic_double()椭圆曲线自加
* elliptic_multiply()椭圆曲线乘运算
* generate_key()生成公私钥对
* sign()签名
* verify()验证
k由RFC6979生成
## 结果
![image](https://github.com/Ashl703/group-xx/assets/138503504/4fd0276a-4de5-4da5-83e8-82ab73656a40)

