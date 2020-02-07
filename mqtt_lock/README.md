1.本文件夹下是人脸识别系统的硬件实现部分，实现了一个mqtt的执行器功能。
2.文件夹下的sch&pcb文件夹中是硬件电路板的原理图和PCB，AD格式，pdf文件是原理图。
3.项目基于micropython的ESP8266的运行时环境，在下载三个py文件前，应该先使用乐鑫的下载工具下载运行时。运行时下载地址:http://www.micropython.org/download
4.项目的boot.py是项目的主要逻辑，simple.py和robust.py来自于micropython-lib，simple.py提供了基于socket的mqtt底层环境，robust.py则提供了一些关于鲁棒性的功能（注意，我们对这个文件进行了改造，和开源库中的有差异）
