# implement the naïve birthday attack of reduced SM3
## 主要函数
* StoB(msg):字符串转比特串
* ItoB(a,k):整数转比特串
* ItoH(a,k):整数转16进制字符串
* BtoH(a,k):比特串转16进制字符串
* fill(msg_bin):消息填充
* Iteration_func(msg):迭代函数，实现将消息每512比特分组、迭代压缩功能
* msg_extension(bi):消息扩展
* cf(vi,bi):压缩函数
* move_left(a,k):循环左移k比特
* p0(x):置换函数p0
* SM3(msg):实现sm3算法
* BirthdayAttack(n):生日攻击
## 运行结果
![image](https://github.com/Ashl703/group-xx/assets/138503504/4a7bc0b4-e936-46a0-bbaa-739c69da3829)
