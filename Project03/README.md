# implement length extension attack for SM3, SHA256, etc.
## 攻击原理
* 计算原消息msg的hash值H
* 在msg+padding之后附加一段消息,用H作为IV计算附加消息之后的hash值,得到消息扩展后的hash_attack
* 得到hash_extend
* 验证hash_attack == hash_extend
## 实现结果：
![image](https://github.com/Ashl703/group-xx/assets/138503504/abd7331a-a584-43b8-8966-7a0fcc79dde1)
