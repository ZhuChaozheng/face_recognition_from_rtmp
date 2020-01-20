import time
import simple
import machine

class MQTTClient(simple.MQTTClient):

    DELAY = 2
    DEBUG = False

    def delay(self, i):
        time.sleep(self.DELAY)

    def log(self, in_reconnect, e):
        if self.DEBUG:
            if in_reconnect:
                print("mqtt reconnect: %r" % e)
            else:
                print("mqtt: %r" % e)

    def reconnect(self):
        i = 0
        reboot_cnt = 0
        while 1:
            try:
                print("reconnect")
                return super().connect(False)
            except OSError as e:
                self.log(True, e)
                i += 1
                reboot_cnt += 1
                print(reboot_cnt)
                if reboot_cnt == 3:
                    machine.reset()

    def publish(self, topic, msg, retain=False, qos=0):
        while 1:
            try:
                return super().publish(topic, msg, retain, qos)
            except OSError as e:
                self.log(False, e)
                machine.reset()
            self.reconnect()

    def wait_msg(self):
        while 1:
            try:
                self.sock.setblocking(False)
                return super().wait_msg()
            except OSError as e:
                self.log(False, e)
            self.reconnect()
            