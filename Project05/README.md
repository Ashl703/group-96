# Impl Merkle Tree following RFC6962
## 实现思路
用列表存储10w个data block的哈希值，然后构建merkle tree；具体来说，根据data blocks的奇偶来找到合并对象，最终生成根节点。<br>
存在性证明的思路类似，生成最终的哈希值然后与根节点进行比较，达成目的。选用data block 12345进行存在性证明，data block 999999进行不存在证明。<br>
## 运行结果
![image](https://github.com/Ashl703/group-xx/assets/138503504/15a7940e-1d81-4d1a-b65b-884d48a90e88)
