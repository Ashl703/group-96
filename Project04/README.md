# do your best to optimize SM3 implementation (software)
## 主要函数
* ROTATE_LEFT：循环左移
* FF1、GG1：实现逻辑运算
* P0、P1：实现置换运算
* sm3_compress：压缩函数
## 使用OpenMP中的多线程技术（parallel）
在计算核心部分的循环周围添加#pragma omp parallel for指令，通过多线程并行执行循环。这将使每个线程处理不同的迭代，从而加速计算过程。
## 运行时间对比
将算法运行1000次，得到测试时间取平均，可以看到运行时间由0.001s降低至0.000002s。
![image](https://github.com/Ashl703/group-96/assets/138503504/acbfc8da-92ec-4c34-9adc-7971c05fb31c)
![image](https://github.com/Ashl703/group-96/assets/138503504/a5c652cc-2d8f-4adc-bc6d-752a87937f9b)
