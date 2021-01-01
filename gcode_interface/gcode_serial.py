import serial
import threading
from time import sleep
import logging

# lock = threading.Lock()

class Gcode:
    def __init__(self, port="/dev/ttyUSB0", baudrate=115200, logger=None):
        if logger:
            self.logger = logger
        else:
            logging.basicConfig(level=logging.INFO)
            self.logger = logging
        self.running = True
        self._feedrate = 500
        try:
            self.serial = serial.Serial(port, baudrate, timeout=1)
        except:
            self.logger.error("coulnd't open {}".format(port))
            self.running = False
            return
        self.logger.info("Connected port {} at {} bauds".format(port, baudrate))
        while self.serial.inWaiting() > 0:
            _ = self.serial.read()  # vacia buffer
        self.listen_th = threading.Thread(target=self._listen)
        self.listen_th.start()


    def _listen(self):
        sample_rate = 0.1
        while self.running:
            sleep(sample_rate)
            try:
                hay_datos_serie = self.serial.inWaiting()
            except:  # OSError: [Errno 5] Input/output error
                self.logger.error("Serial port disconnected")
                self.running = False
                break
            if hay_datos_serie == 0:
                continue
            response = self.serial.read_until()  # terminator=LF, size=None Read until a termination sequence is found ('\n' by default), the sizeis exceeded or until timeout occurs.
            response = response.decode(encoding = 'UTF-8',errors = 'ignore')
            self.logger.debug(response.strip())

    def move(self, x, y, z):
        # G1 X7 Y18 F500
        msg = "G1 X{:.3f} Y{:.3f} z{:.3f} F{}\n".format(float(x), float(y), float(z), self._feedrate)
        self.logger.info(msg.strip())
        self.serial.write(msg.encode(encoding='UTF-8'))

    def stop(self):
        self.running = False
        self.logger.info("stopping...")
        if self.listen_th.is_alive():
            self.listen_th.join()
        self.serial.close()
        self.logger.info("stopped")
    
    @property
    def feedrate(self):
        return self._feedrate 

    @feedrate.setter
    def feedrate(self, value):
        self._feedrate = int(value)
        

if __name__ == '__main__':
    try:
        gcode = Gcode()
        for i in range(10):
            print(i)
            sleep(1)
            if i == 3:
                gcode.feedrate = 750
            elif i == 4:
                gcode.move(4,5,6)
    except Exception as e:
        print(e)
    finally:
        gcode.stop()
