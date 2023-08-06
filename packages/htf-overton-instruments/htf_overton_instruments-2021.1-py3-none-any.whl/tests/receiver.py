import serial


class Receiver:
    """
    Simulates device responses.
    """

    def __init__(self, print_messages: bool):
        """
        Args:
            print_messages (bool): if ``True`` all incoming and outgoing messages are printed to the console.
        """
        self._serial = serial.Serial("COM5")
        self._serial.baudrate = 19200
        self._serial.bytesize = 8
        self._serial.parity = serial.PARITY_NONE
        self._serial.stopbits = serial.STOPBITS_ONE
        self._serial.xonxoff = 0
        self.baudrate_code = "0"
        self.output_bits = [[0, 1, 1, 0, 1, 0, 0, 1], [1, 0, 0, 1, 0, 1, 1, 0]]
        self.settling_time = ""
        self.relays = [0, 0, 0, 0, 0, 0, 0, 0]
        self.presets = [
            [0, 1, 0, 1, 0, 1, 0, 1],
            [1, 0, 1, 0, 1, 0, 1, 0],
            [1, 1, 0, 0, 1, 0, 1, 0]
        ]
        self.mux_mode = "0"
        self.port = 0
        self.print_messages = print_messages

    def send_data(self, data):
        """ Sends an ASCII message containing ``data`` and a CR. """
        data = str(data) + '\r'
        msg = bytes(data.encode('ascii'))
        self._serial.write(msg)
        if self.print_messages:
            print(self._serial.port + " sent " + repr(data))

    def get_message(self):
        """ Waits for an incoming message and sends the appropriate response. """
        self._serial.reset_input_buffer()
        message = ""
        while True:

            byte = self._serial.read()
            byte = byte.decode('ascii')
            message += byte

            if len(byte) == 0:
                break

            if byte == '\n' or byte == '\r':
                if self.print_messages:
                    print(self._serial.port + " received: " + message)
                if message == "\r":
                    self.send_data("->")
                    message = ""
                if "IO_" in message:
                    if "BR" in message:
                        for char in message:
                            if char.isdigit():
                                self.baudrate_code = char
                        self.send_data(f"<{self.baudrate_code}>")
                    elif "DO" in message:
                        if "?" in message:
                            for char in message:
                                if char.isdigit():
                                    self.send_data(f"<{self.output_bits[self.port][int(char)]}>")
                        else:
                            selected = None

                            for char in message:
                                if char.isdigit():
                                    if selected is not None:
                                        self.output_bits[self.port][int(selected)] = int(char)
                                    selected = char
                    elif "ID?" in message:
                        self.send_data("<OPTO-MATEIII(vI)>")
                    elif "PF?" in message:
                        self.send_data("<>")
                    elif "PS?" in message:
                        self.send_data(f"<{self.output_bits[self.port]}>")
                    elif "PN" in message:
                        for char in message:
                            if char.isdigit():
                                self.port = int(char)
                                self.send_data("<>")
                            elif char == "?":
                                self.send_data(f"<{self.port}>")
                    elif len(message) > 1:
                        self.send_data("<>")
                    message = ""
                elif "SM_" in message:
                    if "BR" in message:
                        for char in message:
                            if char.isdigit():
                                self.baudrate_code = char
                        self.send_data(f"<{self.baudrate_code}>")
                    elif "ID?" in message:
                        self.send_data("<SWITCH-MATE(vI)>")
                    elif "RS?" in message:
                        self.send_data(f"<{self.relays}>")
                    elif "ST" in message:
                        if "?" in message:
                            self.send_data(f"<{self.settling_time}>")
                        else:
                            self.settling_time = ""
                            for char in message:
                                if char.isdigit():
                                    self.settling_time += char
                    elif "RC?" in message:
                        return_preset = ""
                        for char in message:
                            if char.isdigit():
                                return_preset += char
                                if len(return_preset) == 2:
                                    self.send_data(f"<{self.presets[int(return_preset)]}>")
                    elif "SR0" in message:
                        for char in message:
                            if char.isdigit():
                                selected_relay = char
                                if selected_relay is not None:
                                    self.relays[int(selected_relay)] = int(char)
                    elif "WC" in message:
                        write_relay = ""
                        for char in message:
                            if char.isdigit():
                                write_relay += char
                                if len(write_relay) == 2:
                                    self.presets[int(write_relay)] = self.relays
                    elif "SC" in message:
                        select_preset = ""
                        for char in message:
                            if char.isdigit():
                                select_preset += char
                                if len(select_preset) == 2:
                                    self.relays = self.presets[int(select_preset)]
                    elif "MC" in message:
                        self.relays = [0, 0, 0, 0, 0, 0, 0, 0]
                    elif "MS" in message:
                        self.relays = [1, 1, 1, 1, 1, 1, 1, 1]
                    elif len(message) > 1:
                        self.send_data("<>")
                    message = ""
                elif "GS_" in message:
                    if "BR" in message:
                        for char in message:
                            if char.isdigit():
                                self.baudrate_code = char
                        self.send_data(f"<{self.baudrate_code}>")
                    elif "ID?" in message:
                        self.send_data("<GSM Mate>")
                    elif "RS?" in message:
                        self.send_data(f"<{self.relays}>")
                    elif "ST" in message:
                        if "?" in message:
                            self.send_data(f"<{self.settling_time}>")
                        else:
                            self.settling_time = ""
                            for char in message:
                                if char.isdigit():
                                    self.settling_time += char
                    elif "SR0" in message:
                        for char in message:
                            if char.isdigit():
                                selected_relay = char
                                if selected_relay is not None:
                                    self.relays[int(selected_relay)] = int(char)
                    elif len(message) > 1:
                        self.send_data("<>")
                    message = ""
                elif "MX_" in message:
                    if "BR" in message:
                        for char in message:
                            if char.isdigit():
                                self.baudrate_code = char
                        self.send_data(f"<{self.baudrate_code}>")
                    elif "ID?" in message:
                        self.send_data("<MUX Mate>")
                    elif "RS?" in message:
                        self.send_data(f"<{self.relays}>")
                    elif "ST" in message:
                        if "?" in message:
                            self.send_data(f"<{self.settling_time}>")
                        else:
                            self.settling_time = ""
                            for char in message:
                                if char.isdigit():
                                    self.settling_time += char
                    elif "RC?" in message:
                        return_preset = ""
                        for char in message:
                            if char.isdigit():
                                return_preset += char
                                if len(return_preset) == 2:
                                    self.send_data(f"<{self.presets[int(return_preset)]}>")
                    elif "SR0" in message:
                        for char in message:
                            if char.isdigit():
                                selected_relay = char
                                if selected_relay is not None:
                                    self.relays[int(selected_relay)] = int(char)
                    elif "MM" in message:
                        if "?" in message:
                            self.send_data(f"<{self.mux_mode}>")
                        else:
                            self.mux_mode = ""
                            for char in message:
                                if char.isdigit():
                                    self.mux_mode += char
                    elif "MC" in message:
                        self.relays = [0, 0, 0, 0, 0, 0, 0, 0]
                    elif "MS" in message:
                        self.relays = [1, 1, 1, 1, 1, 1, 1, 1]
                    elif len(message) > 1:
                        self.send_data("<>")
                    message = ""
                elif "SF_" in message:
                    if "BR" in message:
                        for char in message:
                            if char.isdigit():
                                self.baudrate_code = char
                        self.send_data(f"<{self.baudrate_code}>")
                    elif "ID?" in message:
                        self.send_data("<SFM Mate>")
                    elif "ST" in message:
                        if "?" in message:
                            self.send_data(f"<{self.settling_time}>")
                        else:
                            self.settling_time = ""
                            for char in message:
                                if char.isdigit():
                                    self.settling_time += char
                    elif "AS?" in message:
                        self.send_data("<00000000>")
                    elif len(message) > 1:
                        self.send_data("<>")
                    message = ""
