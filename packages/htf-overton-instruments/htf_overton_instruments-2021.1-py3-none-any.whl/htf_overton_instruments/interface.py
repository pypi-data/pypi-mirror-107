import serial
import htf
import time
import os.path


class OIInterface:
    """Overton Instruments Interface class, enables communication with their devices"""

    def __init__(self, com_port, name):
        """
        Args:
            com_port (str): COM port on which device is connected
            name (str): Name of device
        """
        self.comport = com_port
        self.device_port = 0
        self.collect_bits = False
        self.print_messages = True
        self.all_bits = [[], []]
        self.reply = None
        self._serial = serial.Serial(timeout=1)
        self._serial.port = self.comport
        self._serial.baudrate = 19200
        self._serial.bytesize = 8
        self._serial.parity = serial.PARITY_NONE
        self._serial.stopbits = serial.STOPBITS_ONE
        self._serial.xonxoff = 0

    def open_port(self):
        """ Opens serial connection on the connected COM port """
        self._serial.open()

    def close_port(self):
        """ Closes serial connection """
        self._serial.close()

    def query(self, data):
        """
        Sends a request for information contained by ``data``
        and makes the client wait for the response.
        Sleep is required to ensure sequential communication.

        Args:
            data: ASCII command to be sent

        """
        data = str(data) + '\r'
        msg = bytes(data, encoding="ascii")

        # time.sleep(1)
        # self._serial.flushInput()
        self._serial.write(msg)

        if self.print_messages:
            print(f"{self.comport} sent {msg}")

        # self.__serial.reset_output_buffer()
        # time.sleep(3)  # Apparently a delay here produces quasi-regular sample intervals (doesn't work without it)
        # self._serial.flushOutput()
        self.read()

        if self.print_messages and self.reply is not None:
            print(f"Reply: {self.reply}")

    def read(self, timeout=3):
        """
        Checks for replies from the OI device.
        OI device replies are between '<' and '>'
        and a CR ends the message.
        """
        message = ''
        tmax = time.time() + timeout

        # read until '>'
        while byte := self.get_next_byte():
            if time.time() > tmax:
                raise TimeoutError("Timeout has occurred.")
            if byte == '\n':
                if message == '\r':
                    continue
                else:
                    break
            message += byte

        self.process_message(message)

    def get_next_byte(self):
        """
        Reads a byte from the COM port.

        Returns:
            the read byte as a string
        """
        return self._serial.read(1).decode('ascii')

    def process_message(self, message):
        """
        Packages replies neatly to work with htf tests.
        Device replies are stored in instance attribute reply.

        Args:
            message (str):
        """
        self.reply = None

        message = message.strip()
        message = message.replace('\r', '')
        if message == '->':
            self.reply = "Ready."
            return
        message = message.replace('<', '')
        message = message.replace('->', '')
        message = message.replace('>', '')
        message = message.strip()

        if message == '><':
            self.read()

        if message != '':
            if self.collect_bits:
                self.all_bits[self.device_port].append(int(message))
            else:
                if len(message) == 1:
                    self.reply = int(message)
                else:
                    self.reply = message
        else:
            self.reply = True
