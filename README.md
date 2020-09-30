# face_recognition_from_rtmp

This project is hosted by Hohai University Robotics motion and vision Lab by National Defense Student. As its name meaning, we release a stable solution on face_recognition through RTMP. Before starting this project, we accumulate abundant practical experience on real-time video transmission system based on RTMP, which has been applied in [dog_project](https://github.com/ZhuChaozheng/dog_project). As we all known, RTMP is the best method for live video, since it has minimum delay time than other solutions (e.g. RTSP). Also, to obtain better result in face recognition, we call many functions on [Johe](https://github.com/ageitgey/face_recognition)'s C++ library. As you can see, it will draw a rectangle to contain someone face and name him below this rectangle.


## Get Started
```
pip3 install cycler==0.10.0 kiwisolver==1.0.1 matplotlib==2.2.2 numpy==1.14.2 opencv-python==3.4.0.12 pyparsing==2.2.0 python-dateutil==2.7.2 pytz==2018.4 six==1.11.0

pip3 install dlib

pip3 install face_recognition

git clone https://github.com/ZhuChaozheng/face_recognition_from_rtmp

python3 face_recognition_from_rtmp.py --cpus 4
```

## Parrallel Compute
you can also set the argument to equal with your cpu cores. *``e.g. --cpus 40``*

## Multi-Video-Input
we can easy to realize multi video sources input by using command line, set the argument --rtmp. *``e.g. --rtmp 192.168.1.117/2710/live``*

## How to push your own video
### server
the most easiest way is to use [srs](https://github.com/ossrs/srs/wiki/v1_CN_SampleRTMP)
```
git clone https://github.com/ossrs/srs

cd srs/trunk

git pull

./configure && make
```
modify the *conf* file
```
# conf/rtmp.conf
listen              1935;
max_connections     1000;
vhost __defaultVhost__ {
}
```
start you srs server
```
./objs/srs -c conf/rtmp.conf
```
### client

for pi use default camera(not USB camera)
```
gst-launch-1.0 -v v4l2src ! 'video/x-raw, width=640, height=480, framerate=30/1' ! queue ! videoconvert ! omxh264enc !  h264parse ! flvmux ! rtmpsink location='rtmp://{your server IP}/rtmp/live live=1'
```
for Ubuntu PC
```
sudo apt-get install libav-tools
avconv -f video4linux2 -r 24 -i /dev/video0 -f flv rtmp://{your server IP}:1935/rtmp/live
```

Then your RTMP stream is ``rtmp://{your server IP}/live/livestream``


# 一.环境搭建

## 1.1ubuntu 16.04

```plain
pip3 install cycler==0.10.0 kiwisolver==1.0.1 matplotlib==2.2.2 numpy==1.14.2 opencv-python==3.4.0.12 pyparsing==2.2.0 python-dateutil==2.7.2 pytz==2018.4 six==1.11.0
pip3 install dlib
pip3 install face_recognition -i https://pypi.tuna.tsinghua.edu.cn/simple/      使用清华源的话，可以顺便也把dlib库安装好，即可以一次性安装好所有依赖，之后就可以直接导入对应的识别包，同时也可以在控制台使用face_recognition命令传入图片信息直接识别 详情见：https://github.com/ageitgey/face_recognition 
pip3 install opencv-python （推荐，用于视频流和图片信息操作）
pip3 install paho-mqtt （可选，只是目前所使用的通信方式）
git clone https://github.com/ZhuChaozheng/face_recognition_from_rtmp（克隆项目）
python3 face_recognition_from_rtmp.py --cpus 4
```
## 1.2 推流服务器搭建

与树莓派进行连接

```plain
ｘｓｈｅｌｌ使用树莓派ｉｐ连接树莓派
树莓派用户名  pi  密码 raspberry
vi /etc/wpa_supplicant/wpa_supplicant.conf 修改wifi
树莓派用户名　ｒｏｏｔ　　　密码　raspberry
自启动推流文件 revideo.sh  在/etc/profile.d 目录下　
手动推流方式，video.sh在Documents目录下
sh video.sh 
自启动推流
将revideo.sh移动到/etc/profile.d，要取消自启动推流的话则将该文件移到别的目录
```
## 1.3搭建nginx+rtmp推流服务

```plain
sudo apt-get update
sudo apt-get -y install nginx
sudo apt-get -y remove nginx
sudo apt-get clean
sudo rm -rf /etc/nginx/*
安装编译用的套件
sudo apt-get install -y curl build-essential libpcre3-dev libpcre++-dev zlib1g-dev libcurl4-openssl-dev libssl-dev
建立系统上放置网页的目录
sudo mkdir -p /var/www
建立编译用的目录
mkdir -p ~/nginx_src
cd ~/nginx_src
用 git 下载 nginx 与 nginx-rtmp-module 的原始码
git clone https://github.com/arut/nginx-rtmp-module.git
git clone https://github.com/nginx/nginx.git
设定编译参数
cd nginx
./configure --prefix=/var/www --sbin-path=/usr/sbin/nginx --conf-path=/etc/nginx/nginx.conf --pid-path=/var/run/nginx.pid --error-log-path=/var/log/nginx/error.log --http-log-path=/var/log/nginx/access.log --with-http_ssl_module --without-http_proxy_module --add-module=/home/pi/nginx_src/nginx-rtmp-module
测试是否安装正常
nginx -v
正常的话，会显示版本
修改 /etc/nginx/nginx.conf，添加推流地址，如图rtmp-live_2710地址，如果要添加推流地址，直接加上 application live_2711之类的即可
详情见  https://blog.gtwang.org/iot/raspberry-pi-nginx-rtmp-server-live-streaming/

```
![图片](https://uploader.shimo.im/f/kLgEtbM7zLLjhZkc.png!thumbnail)

1.4 安装emqx，与锁进行通信

emqx broker  3.2.7以上

看官网下载文档[https://docs.emqx.io/broker/latest/en/getting-started/install.html](https://docs.emqx.io/broker/latest/en/getting-started/install.html)

# 二、使用

## 2.1.存储人脸图片

把相片导入到known_people文件夹中，训练人脸模型，照片名即为识别出的信息，分辨率越高精度越好，训练速度越慢，照片选择单人照，没有比例要求，训练完就可以进行识别了

```plain
python3 training_face_encodings.py path of the photo
```
## 2.2.识别

```plain
python3 ttt.py
```
目前采用的是rtmp流传输视频信息，opencv截取图片进行识别，若是存在被识别出的人脸则会发送到mqtt服务器，同时锁接收到相应的消息然后开锁2秒钟
# 三.测试及其他补充

## 3.1测试识别

测试时可以使用公开的rtmp源地址，不过可能会有些卡，也可以利用“直播神探”应用对某些使用rtmp协议的直播平台截取推流码（后一个方法源比较好，视频流会比较流畅），在ttt.py文件里修改rtmp地址即可

## 3.2测试门锁

测试门锁的推流成不成功，使用vlc软件，填写推流地址，查看是否显示画面


## 3.3其他

rtrt.py只是单纯的rtmp推流，检测视频流延迟的

面对不同分辨率可能需要调整识别代码中的compare参数（tolerance）来确保准确度，越低越严格

location中可以加参数改变识别距离（实际上是对人脸大小的筛选，数值越大越能够定位到更小的脸，默认是1）

准确度用tolerance参数即可，速率上需要跑成并行（控制台命令中已经有了直接利用多核的方式，但是代码本身应用的时候还需要自己去写，作者并没有提供相应代码）或者采用隔帧识别方式，距离上可以修改opencv的缩放程度以及location参数修改，不过延长距离会较大影响到识别速率最好和并行结合起来。

一个锁对应一个话题，服务器向对应话题发送开锁指令，只有订阅该话题的锁能收到指令，其他锁无法接收

启动后至多一分钟自动开始传输视频，若摄像头红灯未亮起则说明失败，检测ｗｉｆｉ网络是否设置正确以及供电口是否正确

倘若发现视频无法播放，有播放器页面但是没有画面，而且红灯亮起，则可能是网络中断，请检查路由器是否正常，待网络正常之后，至多等待几分钟即可恢复推流，若没有恢复就断电重启

# 四、实验室账户密码等信息

计信院服务器ip：10.196.83.16

端口:1883

服务器密码：P@ssw0rd

Teamviewer 账号 1488447980    密码：fc12345

黄倩老师实验室的锁

锁id：client2710

推流地址：rtmp://10.196.83.16/live_2711/hello

文件地址：face_recognition_from_rtmp

人脸图片存储在known_people文件夹

运行 ttt文件

# 五、算力要求

比河海校园网好就行，不知道河海具体带宽多少



