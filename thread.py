from threading import Thread
import time

class Monitor(Thread):
    def __init__(self, name):
        Thread.__init__(self)
        self.name = name

    def run(self):
        print self.getName(), '\n'

if __name__ == '__main__':
    try:
        t = Monitor('123')
        while True:
            t.setDaemon(True)
            t.start()
            time.sleep(1)
            if t.isAlive():break
            else:t = Monitor('123')

    except (KeyboardInterrupt):
        pass
    except Exception, e:
        print e
