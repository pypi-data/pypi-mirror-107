from htf_overton_instruments import interface


class OIDevice(interface.OIInterface):
    PROTOCOL_PREFIX = None

    def __init__(self, com_port, name):
        """
        Initializes an OIInterface with the given COM port.

        Args:
            com_port (str)
            name (str): device name used to get device configuration
        """
        super().__init__(com_port, name)

    @property
    def is_device_ready(self):
        """ Sends a CR to check if the device is ready for commands. """
        self.query("")

    @property
    def baudrate(self):
        """ Generalized Baud rate getter """
        self.query(f"{self.PROTOCOL_PREFIX}_BR?")

    @baudrate.setter
    def baudrate(self, baudrate: int):
        """
        Generalized baudrate setter

        Args:
             baudrate (int): Baud rate code to be set to device
        """
        self.query(f"{self.PROTOCOL_PREFIX}_BR{baudrate}")

    @property
    def module_id(self):
        """ Generalized module ID getter """
        self.query(f"{self.PROTOCOL_PREFIX}_ID?")

    @property
    def master_reset(self):
        """ Generalized master reset """
        self.query(f"{self.PROTOCOL_PREFIX}_MR")


class OptoMateIII(OIDevice):
    PROTOCOL_PREFIX = "IO"

    def __init__(self, com_port):
        """
        Initializes an OIInterface object with the given COM port and predetermined device name.

        Args:
            com_port (str)
        """
        super().__init__(com_port, "OPTO-MATE-III")

    @property
    def output_bit(self):
        """
        Queries for all bits on both ports.

        Returns:
            list of lists of int: set bits are represented with ``1`` and cleared bits with ``0``
        """
        self.collect_bits = True
        for port in range(0, 2):
            self.device_port = port
            self.query(f"IO_PN{port}")
            for bit in range(0, 8):
                self.query(f"IO_DO?{bit}")
        self.collect_bits = False
        self.reply = self.all_bits

    @output_bit.setter
    def output_bit(self, bit: int):
        """
        Sends query for the state of ``bit``.

        Args:
            bit (int): which bit to be checked
        """
        self.query(f"IO_DO?{bit}")

    @output_bit.setter
    def set_output_bit(self, data):
        """
        Sends query to set a bit (``data[0]``) to a state (``data[1]``)

        Args:
            data (tuple): contains both bit and state
        """
        self.query(f"IO_DO{data[0]}{data[1]}")

    @property
    def port_format(self):
        """ Queries the format of the currently selected port. """
        self.query("IO_PF?")

    @port_format.setter
    def port_format(self, port):
        """
        Sets current port to ``port``.

        Args:
            port (int): port to be used.
        """
        self.query(f"IO_PF{port}")

    @property
    def port_data(self):
        """ Queries the data of the currently selected port. """
        self.query("IO_PS?")

    @port_data.setter
    def port_data(self, data):
        """
        Writes ``data`` to the currently selected port.

        Args:
            data (8 bits): Big-Endian
        """
        self.query(f"IO_PW{data}")

    @property
    def port_number(self):
        """ Checks which port is currently selected. """
        self.query("IO_PN?")

    @port_number.setter
    def port_number(self, port):
        """
        Selects ``port``

        Args:
            port (int)
        """
        if port not in range(0, 2):
            raise ValueError("Valid ports are 0 and 1!")
        self.query(f"IO_PN{port}")


class SwitchMateV1(OIDevice):
    PROTOCOL_PREFIX = "SM"

    def __init__(self, com_port):
        """
        Initializes an OIInterface with the given COM port and predetermined device name.

        Args:
            com_port (str)
        """
        super().__init__(com_port, "SWITCH-MATE(v1)")

    @property
    def relay(self):
        """ Gets the state of the currently selected relay. """
        self.query("SM_RS?")

    @relay.setter
    def relay(self, data):
        """
        Selects a relay and sets it to a given state.

        Args:
            data (tuple): First element is which relay is to be set, second element is the state
        """
        self.query(f"SM_SR0{data[0]}{data[1]}")

    @property
    def clear_relays(self):
        """ Clears all relays """
        self.query("SM_MC")

    @property
    def close_relays(self):
        """ Sets all relays """
        self.query("SM_MS")

    @relay.setter
    def set_relays(self, byte):
        """
        Sets relays to ``byte``.

        Args:
            byte (hex): The hexadecimal number which the relays are to be set to.
        Raises:
            ValueError: if the ``byte`` is not between 0 and 16.
        """
        if byte < 0 or byte > 15:
            raise ValueError("Choose a value between 0x0 and 0xF")
        self.query(f"SM_SM0{byte:1X}")

    @property
    def settling_time(self):
        """ Gets the settling time of the currently selected relay. """
        self.query("SM_ST?")

    @settling_time.setter
    def settling_time(self, time):
        """
        Sets the settling time of the currently selected relay to ``time``.

        Args:
            time (int): Integer between 0 and 255.
        Raises:
            ValueError: if the ``time`` is not between 0 and 255.
        """
        if time < 1 or time > 255:
            raise ValueError("Choose a value between 1 and 255")
        self.query(f"SM_ST{time:03}")

    @property
    def relay_config(self):
        """ Clears all pre-set relay configurations. """
        self.query("SM_CC")

    @relay_config.setter
    def select_relay_config(self, memory_location):
        """
        Selects a pre-set relay configuration.

        Args:
            memory_location (int)

        Raises:
            ValueError: if ``memory_location`` is not between 1 and 16.
        """
        if memory_location < 0 or memory_location > 15:
            raise ValueError("Choose a value between 0 and 15")
        self.query(f"SM_SC{memory_location:02}")

    @relay_config.setter
    def read_relay_config(self, memory_location):
        """
        Reads the relay configuration at ``memory_location``.

        Args:
            memory_location (int)

        Raises:
            ValueError: if ``memory_location`` is not between 1 and 16.
        """
        if memory_location < 0 or memory_location > 15:
            raise ValueError("Choose a value between 0 and 15")
        self.query(f"SM_RC?{memory_location:02}")

    @relay_config.setter
    def save_relay_config(self, memory_location):
        """
        Saves the current relay configuration at ``memory_location``.

        Args:
            memory_location (int)

        Raises:
            ValueError: if ``memory_location`` is not between 1 and 16.
        """
        if memory_location < 0 or memory_location > 15:
            raise ValueError("Choose a value between 0 and 15")
        self.query(f"SM_WC{memory_location:02}")


class GSMMate(OIDevice):
    PROTOCOL_PREFIX = "GS"

    def __init__(self, com_port):
        """
        Initializes an OIInterface with the given COM port and predetermined device name.

        Args:
            com_port (str)
        """
        super().__init__(com_port, "GSM-MATE")



    @property
    def relay(self):
        """ Gets the state of the currently selected relay. """
        self.query("GS_RS?")

    @relay.setter
    def relay(self, data):
        """
        Selects a relay and sets it to a given state.

        Args:
            data (tuple): First element is which relay is to be set, second element is the state
        """
        self.query(f"GS_SR0{data[0]}{data[1]}")

    @property
    def settling_time(self):
        """ Gets the settling time of the currently selected relay. """
        self.query("GS_ST?")

    @settling_time.setter
    def settling_time(self, time):
        """
        Sets the settling time of the currently selected relay to ``time``.

        Args:
            time (int): Integer between 0 and 255.
        Raises:
            ValueError: if the ``time`` is not between 0 and 255.
        """
        if time < 1 or time > 255:
            raise ValueError("Choose a value between 1 and 255")
        self.query(f"GS_ST{time:03}")


class LDMMate(OIDevice):
    PROTOCOL_PREFIX = "IO"

    def __init__(self, com_port):
        """
        Initializes an OIInterface with the given COM port and predetermined device name.

        Args:
            com_port (str)
        """
        super().__init__(com_port, "LDM-MATE")

    @property
    def output_bit(self):
        """
        Queries for all bits on both ports.

        Returns:
            list of lists of int: set bits are represented with ``1`` and cleared bits with ``0``
        """
        self.collect_bits = True
        for bit in range(0, 8):
            self.query(f"IO_DO?{bit}")
        self.collect_bits = False
        self.reply = self.all_bits

    @output_bit.setter
    def output_bit(self, bit: int):
        """
        Sends query for the state of ``bit``.

        Args:
            bit (int): which bit to be checked
        """
        self.query(f"IO_DO?{bit}")

    @output_bit.setter
    def set_output_bit(self, data):
        """
        Sends query to set a bit (``data[0]``) to a state (``data[1]``)

        Args:
            data (tuple): contains both bit and state
        """
        self.query(f"IO_DO{data[0]}{data[1]}")

    @property
    def port_format(self):
        """ Queries the format of the currently selected port. """
        self.query("IO_PF?")

    @port_format.setter
    def port_format(self, port):
        """
        Sets current port to ``port``.

        Args:
            port (int): port to be used.
        """
        self.query(f"IO_PF{port}")

    @property
    def port_data(self):
        """ Queries the data of the currently selected port. """
        self.query("IO_PS?")

    @port_data.setter
    def port_data(self, data):
        """
        Writes ``data`` to the currently selected port.

        Args:
            data (8 bits): Big-Endian
        """
        self.query(f"IO_PW{data}")


class MUXMate(OIDevice):
    PROTOCOL_PREFIX = "MX"

    def __init__(self, com_port):
        super().__init__(com_port, "MUX-MATE")

    @property
    def relay(self):
        """ Gets the state of the currently selected relay. """
        self.query("MX_RS?")

    @relay.setter
    def relay(self, data):
        """
        Selects a relay and sets it to a given state.

        Args:
            data (tuple): First element is which relay is to be set, second element is the state
        """
        self.query(f"MX_SR0{data[0]}{data[1]}")

    @property
    def clear_relays(self):
        """ Clears all relays """
        self.query("MX_MC")

    @property
    def close_relays(self):
        """ Sets all relays """
        self.query("MX_MS")

    @property
    def mux_mode(self):
        """ Queries the MUX mode"""
        self.query("MX_MM?")

    @mux_mode.setter
    def mux_mode(self, state):
        """
        Sets the MUX mode

        Args:
            state (int): 0 or 1, check device documentation for mode descriptions.
        """
        if state in (0,1):
            self.query(f"MX_MM{state}")
        else:
            raise ValueError("The state must be 0 or 1")

    @property
    def settling_time(self):
        """ Gets the settling time of the currently selected relay. """
        self.query("MX_ST?")

    @settling_time.setter
    def settling_time(self, time):
        """
        Sets the settling time of the currently selected relay to ``time``.

        Args:
            time (int): Integer between 0 and 255.
        Raises:
            ValueError: if the ``time`` is not between 0 and 255.
        """
        if time < 1 or time > 255:
            raise ValueError("Choose a value between 1 and 255")
        self.query(f"MX_ST{time:03}")


class SFMMate(OIDevice):
    PROTOCOL_PREFIX = "SF"

    def __init__(self, com_port):
        super().__init__(com_port, "SFM-MATE")

    @property
    def short_status(self):
        """ Queries the short status of the device. """
        self.query("SF_AS?")

    @property
    def settling_time(self):
        """ Gets the settling time of the currently selected relay. """
        self.query("SF_ST?")

    @settling_time.setter
    def settling_time(self, time):
        """
        Sets the settling time of the currently selected relay to ``time``.

        Args:
            time (int): Integer between 0 and 255.
        Raises:
            ValueError: if the ``time`` is not between 0 and 255.
        """
        if time < 1 or time > 255:
            raise ValueError("Choose a value between 1 and 255")
        self.query(f"SF_ST{time:03}")
