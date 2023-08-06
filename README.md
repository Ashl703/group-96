# group-96
* 注：由于一开始不熟悉github的使用方法，导致22个项目没有正确创建文件夹；因此评分老师只需看与下文名称一致的文件夹和此md文件即可，其余文件请忽视，感谢谅解！<br>
* 共完成11个项目：Project01、Project02、Project03、Project04、Project05、Project08、Project09、Project-10、Project-11、Project-17、Project-22。<br>
* 基本情况如下，每个项目的具体情况见相关文件夹的md文件。
## 笔记本配置
* CPU:11th Gen Intel(R) Core(TM) i5-1135G7 @ 2.40GHz
## Project01
implement the naïve birthday attack of reduced SM3<br>
实现方式：Python<br>
实现结果：能够实现32bit的生日攻击<br>
![image](https://github.com/Ashl703/group-xx/assets/138503504/4a7bc0b4-e936-46a0-bbaa-739c69da3829)
## Project02
implement the Rho method of reduced SM3<br>
实现方式：Python <br>
实现结果：能够实现32bit的生日攻击<br>
![image](https://github.com/Ashl703/group-xx/assets/138503504/27cbb450-5530-4f1f-8d0c-d4e3d74cd7ba)
## Project03
implement length extension attack for SM3, SHA256, etc.<br>
实现方式：Python<br>
实现结果:基本能够实现md5的长度扩展攻击<br>
![image](https://github.com/Ashl703/group-xx/assets/138503504/abd7331a-a584-43b8-8966-7a0fcc79dde1)
## Project04
do your best to optimize SM3 implementation (software)<br>
实现方式：C++,使用OpenMP中的多线程技术（parallel）<br>
实现结果：运行时间由0.001s降低至0.000002s<br>
![image](https://github.com/Ashl703/group-96/assets/138503504/acbfc8da-92ec-4c34-9adc-7971c05fb31c)

![image](https://github.com/Ashl703/group-96/assets/138503504/a5c652cc-2d8f-4adc-bc6d-752a87937f9b)
## Project05
Impl Merkle Tree following RFC6962<br>
实现方式：Python 
### 实现思路
用列表存储10w个data block的哈希值，然后构建merkle tree,具体来说，根据data blocks的奇偶来找到合并对象，最终生成根节点。存在性证明的思路类似，生成最终的哈希值然后与根节点进行比较，达成目的。选用data block 12345进行存在性证明，data block 999999进行不存在证明。<br>
实现结果：<br>
![image](https://github.com/Ashl703/group-xx/assets/138503504/15a7940e-1d81-4d1a-b65b-884d48a90e88)
## Project06
未实现
## Project07
未实现
## Project08
AES impl with ARM instruction<br>
实现方式：C++<br>
实现结果：<br>
![image](https://github.com/Ashl703/group-xx/assets/138503504/b9067eb4-d89b-41ee-9866-71f2c23c94ab)
## Project09
AES software implementation<br>
实现方式：Python<br>
实现结果：<br>
![image](https://github.com/Ashl703/group-xx/assets/138503504/7d094472-8bde-4e1a-9d22-89224ed339f4)
## Project-10
report on the application of this deduce technique in Ethereum with ECDSA<br>
report具体从ECDSA(椭圆曲线数字签名算法)概述、ECDSA原理、在以太坊中使用ECDSA从签名中推导出公钥的应用三个方面入手,详见Project-10中的readme.md文件。
## Project-11
impl sm2 with RFC6979<br>
实现方式：Python<br>
实现结果：<br>
![image](https://github.com/Ashl703/group-xx/assets/138503504/4fd0276a-4de5-4da5-83e8-82ab73656a40)
## Project12
未完成
## Project13
未完成
## Project14
未完成
## Project15
未完成
## Project16
未完成
## Project-17
比较Firefox和谷歌的记住密码插件的实现区别<br>
report中具体从存储位置、自动登录、密码同步、密码生成器、自动填充、安全性六个方面比较了二者的区别，详见Project-17中的compare.md文件。
## Project18
未完成
## Project19
未完成
## Project20
未完成
## Project21
未完成
## Project-22
research report on MPT<br>
report中具体从MPT简述、Patricia Tree、Merkle Tree、MPT (in Ethereum)、MPT构造过程、HP编码、MPT基本操作七个方面比较了二者的区别，详见Project-22中的repo on MPT.md文件。<br>
## 分工表
独自完成<br>
group-96<br>
组员一：谢兴婷 学号：202100460165
