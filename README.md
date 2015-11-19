# ppc_rebase

## 0x01背景介绍

对于Binary-blob firmware，需要知道其加载基址才能进行正确的反汇编。传统的确定加载基址的方式是通过手工分析指令，然而这种方法耗时且不准确。本代码给出了一种自动化的PowerPC大端模式固件加载基址识别方案。


## 0x02实现原理
![image](http://7xo3a4.com1.z0.glb.clouddn.com/000.jpg)


## 0x03使用举例
![image](http://7xo3a4.com1.z0.glb.clouddn.com/111.jpg)
![image](http://7xo3a4.com1.z0.glb.clouddn.com/222.jpg)
![image](http://7xo3a4.com1.z0.glb.clouddn.com/333.jpg)

## 0x03总结
虽然本代码只支持分析PowerPC大端模式固件的加载基址，但该方法具有较强的通用性，可以通过重构get_arrow_addr_list和get_target_addr_list扩展到其他平台上。
