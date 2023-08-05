from pyfirmata import Board, util, boards
import time
import asyncio
# from inspect import signature
import signal
import sys

def signal_handler(sig, frame):
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)

CMD_LCD_DATA = 3
CMD_LCD_PRINT = 0
CMD_LCD_PUSH = 1
CMD_LCD_CLEAR = 2

CMD_MOTOR_DATA = 2
CMD_MOTOR_ON = 1
CMD_MOTOR_OFF = 2
CMD_MOTOR_INVERSE = 4
CMD_MOTOR_DIR = 5
CMD_MOTOR_SPEED = 6

SAMPLING_INTERVAL = 0x7A  # set the poll rate of the main loop
I2C_REQUEST = 0x76          # send an I2C read/write request
I2C_REPLY = 0x77            # a reply to an I2C read request
I2C_CONFIG = 0x78           # config I2C settings such as delay times and power pins
SET_DIGITAL_PIN = 0xF5         # set a pin value

HIGH = 0x01
LOW = 0x00


class __pyInterfaz(Board):

    def __init__(self, com_port, baudrate=57600, layout=None):
        super().__init__(com_port,  baudrate=baudrate, layout=layout)
        print("Interfaz conectada a "+com_port)
        # Necesitamos escribir directo sobre el puerto e indicamos conexión
        if self.led_builtin:
            self.sp.write([SET_DIGITAL_PIN,self.led_builtin,HIGH]);
            time.sleep(0.1)
            self.sp.write([SET_DIGITAL_PIN,self.led_builtin,LOW]);
        # Iniciamos loop para recibir datos
        it = util.Iterator(self)
        it.start()
        self.add_cmd_handler(I2C_REPLY, self._handle_i2c_message)
        self.send_sysex(I2C_CONFIG, []);  # I2C_CONFIG

    def _handle_i2c_message(self, *args, **kwargs):
        address = util.from_two_bytes([args[0], args[1]])
        if address in self._i2c:
            x = self._i2c[address]
            if x.callBack is not None:
                values = []
                for i in range(2, len(args)-1, 2):
                    values.append(util.from_two_bytes([args[i], args[i+1]]))
                x.callBack(values)
                x.values[values[0]] = values[1:]


    def _handle_analog_message(self, pin_nr, lsb, msb):
        value = ((msb << 7) + lsb)
        # Only set the value if we are actually reporting
        try:
            if self.analog[pin_nr].reporting:
                ## CALL CALLBACK
                for a in self._analogs:
                    if a.index == pin_nr:
                        a._changecb(value)
                self.analog[pin_nr].value = value
        except IndexError:
            raise ValueError

    def output(self, index):
        if index < 1: index = 1
        return self._outputs[index - 1]

    def input(self, index):
        if index < 1: index = 1
        return self._analogs[index - 1]

    def servo(self, index):
        if index < 1: index = 1
        return self._servos[index - 1]

    def i2c(self, address):
        if not address in self._i2c: self._i2c[address] = self._I2C(self, address);
        return self._i2c[address]

    def joystick(self):
        return self._joystick;

    def lcd(self):
        return self._lcd

    def print(self, str1, str2):
        if not self._lcd is None:
            if not self.lcd()._silenciado:
                time.sleep(0.01)
                self.lcd().clear()
                self.lcd().print(0, str1)
                self.lcd().print(1, str2)
                time.sleep(0.01)
        print(' '.join([str1, str2]))

    def loop(self):
        self.loop = asyncio.get_event_loop()
        self.loop.run_forever()

    class _LCD:

        def __init__(self, interfaz):
            self._interfaz = interfaz
            self._silenciado = False

        def _strtosysex(self, str):
            buf = []
            for char in str:
                buf.append(ord(char) & 0x7F)
                buf.append(ord(char) >> 7 & 0x7F)
            return buf

        def push(self, str):
            data = [CMD_LCD_PUSH]
            data += self._strtosysex(str)
            self._interfaz.send_sysex(CMD_LCD_DATA, data)
            return self

        def print(self, row, str):
            data = [CMD_LCD_PRINT, row]
            data += self._strtosysex(str)
            self._interfaz.send_sysex(CMD_LCD_DATA, data)
            return self

        def clear(self):
            self._interfaz.send_sysex(CMD_LCD_DATA, [CMD_LCD_CLEAR])
            return self

        def silence(self):
            self._silenciado = True

        def on(self):
            self._silenciado = False
            return self

    class _Servo:
        def __init__(self, interfaz, index):
            self._interfaz = interfaz
            self.index = index
            self.pin = index - 1 + 9
            self._interfaz.servo_config(self.pin, angle=90)

        def position(self, pos):
            if pos < 0: pos = 0
            if pos > 180: pos = 180
            self._interfaz.digital[self.pin].write(pos)
            self._interfaz.print("servo " + str(self.index + 1), " posicion " + str(pos))

    class _Output:
        def __init__(self, interfaz, index):
            self._interfaz = interfaz
            self.index = index

        def on(self):
            self._interfaz.send_sysex(CMD_MOTOR_DATA, [CMD_MOTOR_ON, self.index])
            self._interfaz.print("salida " + str(self.index + 1), "encendido")
            return self

        def off(self):
            self._interfaz.send_sysex(CMD_MOTOR_DATA, [CMD_MOTOR_OFF, self.index])
            self._interfaz.print("salida " + str(self.index + 1), "apagado")
            return self

        def inverse(self):
            self._interfaz.send_sysex(CMD_MOTOR_DATA, [CMD_MOTOR_INVERSE, self.index])
            self._interfaz.print("salida " + str(self.index + 1), "invertido")
            return self

        def direction(self, d):
            if d > 0:
                d = 1
            else:
                d = 0
            self._interfaz.send_sysex(CMD_MOTOR_DATA, [CMD_MOTOR_DIR, self.index, d])
            self._interfaz.print("salida " + str(self.index + 1), "direccion " + str(d))
            return self

        def speed(self, speed):
            if speed > 100: speed = 100
            if speed < 0: speed = 0
            self._interfaz.send_sysex(CMD_MOTOR_DATA, [CMD_MOTOR_SPEED, self.index, speed & 0x7F, speed >> 7 & 0x7F])
            self._interfaz.print("salida " + str(self.index + 1), "potencia " + str(speed))
            return self

    class _Joystick:
        def __init__(self, interfaz):
            self._interfaz = interfaz
            self.callBack = None
            self.address = 0x48
            self.i2c = self._interfaz.i2c(self.address)
            self.i2c.data(self.__callback)

        def __callback(self, values):
            self.x = 1 if values[2] > 240 else -1 if values[2] < 50 else 0
            self.y = -1 if values[3] > 240 else 1 if values[3] < 50 else 0
            self.button = 1 if values[4] < 10 else 0
            if self.callBack is not None:
                self.callBack({"x": self.x, "y": self.y, "button": self.button})

        def on(self):
            operation = 4 | 0 | 0B01000000;
            self.i2c.write(operation).read_continuous(4)

        def data(self, callback):
            self.callBack = callback
            return self

    class _I2C:
        def __init__(self, interfaz, address):
            self._interfaz = interfaz
            self.address = address & 0x7F
            self.callBack = None
            self.values = dict()

        def write(self, data):
            buf = [self.address, 0, data & 0x7F, data >> 7 & 0x7F]
            self._interfaz.send_sysex(I2C_REQUEST, buf)
            return self

        def __doRead(self, buf, bytes, reg=None):
            if reg is not None:
                buf.append(reg & 0x7F)
                buf.append(reg >> 7 & 0x7F)
            buf.append(bytes & 0x7F)
            buf.append(bytes >> 7 & 0x7F)
            self._interfaz.send_sysex(I2C_REQUEST, buf)

        def read(self, bytes, reg=None):
            buf = [self.address, 8]
            self.__doRead(buf, bytes, reg)

        def read_continuous(self, bytes, reg=None):
            buf = [self.address, 16]
            self.__doRead(buf, bytes, reg)

        def data(self, callback):
            self.callBack = callback
            return self

    class __Sensor:
        def __init__(self):
            self.changeCallback = None
            pass

        def processCallback(self, callback):
            self.changeCallback = callback

        def _changecb(self, data):
            if not (self.changeCallback is None):
                self.changeCallback(data)
                """ 
                sig = signature(self.changeCallback)
                params = len(sig.parameters)
                if params == 1:
                    pass
                elif params == 2:
                    self.changeCallback(data, data)
                """

        def data(self, callback):
            self.processCallback(callback)
            return self

    class _Analog(__Sensor):
        def __init__(self, interfaz, index):
            self._interfaz = interfaz
            self.index = index
            super().__init__()

        def on(self, callback=None):
            self.processCallback(callback)
            self._interfaz.analog[self.index].enable_reporting()
            self._interfaz.print("sensor " + str(self.index + 1), "reportando")

        def off(self):
            self._interfaz.analog[self.index].disable_reporting()
            self._interfaz.print("sensor " + str(self.index + 1), "apagado")

        def read(self):
            return self._interfaz.analog[self.index].read()

        def set_sampling_interval(self, interval):
            self._interfaz.send_sysex(SAMPLING_INTERVAL, util.to_two_bytes(interval))
"""
    class _Digital(__Sensor):
        def __init__(self, interfaz, index):
            self._interfaz = interfaz
            self.index = index
            super().__init__()

        def on(self, callback=None):
            self.processCallback(callback)
            self._interfaz.digital[self.index].enable_reporting()
            self._interfaz.print("sensor dig. " + str(self.index + 1), "reportando")

        def off(self):
            self._interfaz.disable_digital_reporting(self.index)
            self._interfaz.print("sensor dig. " + str(self.index + 1), "apagado")

        def read(self):
            return self._interfaz.digital_read(self.index)[0]
"""

class i32(__pyInterfaz):
    def __init__(self, com_port, baudrate=115200):
        self.boardlayout = {
            'digital' : tuple(x for x in range(40)),
            'analog' : tuple(x for x in range(20)),
            'pwm' : tuple(x for x in range(40)),
            'use_ports' : True,
            'disabled' : (0, 1) # Rx, Tx
        }    
        self.led_builtin = 2;
        super().__init__(com_port, baudrate=baudrate, layout=self.boardlayout)
        self._lcd = self._LCD(self)
        self._outputs = [self._Output(self, 0), self._Output(self, 1), self._Output(self, 2), self._Output(self, 3)]
        self._servos = [self._Servo(self, 1), self._Servo(self, 2)]
        self._analogs = [self._Analog(self, 0), self._Analog(self, 3), self._Analog(self, 6), self._Analog(self,7)]
        self._i2c = dict()
        self._joystick = self._Joystick(self)


class interfaz(__pyInterfaz):
    def __init__(self, com_port):
        self.led_builtin = 13;
        super().__init__(com_port)
        self._lcd = self._LCD(self)
        self._outputs = [self._Output(self, 0), self._Output(self, 1), self._Output(self, 2), self._Output(self, 3)]
        self._servos = [self._Servo(self, 1), self._Servo(self, 2)]
        self._analogs = [self._Analog(self, 0), self._Analog(self, 1), self._Analog(self, 2), self._Analog(self, 3)]
        self._i2c = dict()
        self._joystick = self._Joystick(self)

class rasti(__pyInterfaz):
    def __init__(self, com_port):
        self.led_builtin = 13;
        super().__init__(com_port)
        self._lcd = None
        self._outputs = [self._Output(self, 0), self._Output(self, 1)]
        self._servos = [self._Servo(self, 1), self._Servo(self, 2)]
        self._analogs = [self._Analog(self, 0), self._Analog(self, 1), self._Analog(self, 2), self._Analog(self, 3)]
        self._i2c = dict()
        self._joystick = self._Joystick(self)