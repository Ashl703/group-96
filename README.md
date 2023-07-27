# group-xx
## 笔记本配置

## Project1
implement the naïve birthday attack of reduced SM3
实现方式：Python 实现结果：能够实现32bit的生日攻击
![image](https://github.com/Ashl703/group-xx/assets/138503504/4a7bc0b4-e936-46a0-bbaa-739c69da3829)

## Project2
implement the Rho method of reduced SM3
实现方式：Python 实现结果：能够实现32bit的生日攻击
![image](https://github.com/Ashl703/group-xx/assets/138503504/27cbb450-5530-4f1f-8d0c-d4e3d74cd7ba)

## Project3
implement length extension attack for SM3, SHA256, etc.
md5的长度扩展攻击
![image](https://github.com/Ashl703/group-xx/assets/138503504/abd7331a-a584-43b8-8966-7a0fcc79dde1)

## Project4
## Project5
Impl Merkle Tree following RFC6962
实现方式：Python 
### 实现思路
用列表存储10w个data block的哈希值，然后构建merkle tree,具体来说，根据data blocks的奇偶来找到合并对象，最终生成根节点。存在性证明的思路类似，生成最终的哈希值然后与根节点进行比较，达成目的。选用data block 12345进行存在性证明，data block 999999进行不存在证明。
![image](https://github.com/Ashl703/group-xx/assets/138503504/15a7940e-1d81-4d1a-b65b-884d48a90e88)

## Project6
## Project7
## Project8
## Project9
 AES software implementation
![image](https://github.com/Ashl703/group-xx/assets/138503504/7d094472-8bde-4e1a-9d22-89224ed339f4)

## Project10
report on the application of this deduce technique in Ethereum with ECDSA
## Project11
impl sm2 with RFC6979
## Project12
## Project13
## Project14
## Project15
## Project16
## Project17
## Project18
## Project19
## Project20
## Project21
## Project22
research report on MPT
MPT树定义 一种经过改良的、融合了默克尔树和前缀树两种树结构优点的数据结构，以太坊中，MPT是一个非常重要的数据结构，在以太坊中，帐户的交易信息、状态以及相应的状态变更，还有相关的交易信息等都使用MPT来进行管理，其是整个数据存储的重要一环。交易树，收据树，状态树都是采用的MPT结构。

MPT树的作用 1.存储任意长度的key-value键值对数据； 2.提供了一种快速计算所维护数据集哈希标识的机制； 3.提供了快速状态回滚的机制； 4.提供了一种称为默克尔证明的证明方法，进行轻节点的扩展，实现简单支付验证；
![image](https://github.com/Ashl703/group-xx/assets/138503504/b167d5d2-1ee5-4ef4-8b50-4139cb27b522)

