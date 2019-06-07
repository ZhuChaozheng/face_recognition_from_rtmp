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
