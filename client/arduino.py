import serial
import serial.tools.list_ports


def connect(port):
    """
    Attempts a connection.

    If successful, return the serial connection. Otherwise, throw an error.
    """

    connection = serial.Serial(port, 9600, timeout=3)
    if not connection.is_open:
        raise ConnectionError("ERROR: Could not connect.")

    read = connection.readline().decode()

    if read.startswith("ERROR"):
        raise ConnectionError(read)

    if read.startswith("READY"):
        return connection

    raise TimeoutError("ERROR: Connection timed out. Likely incorrect port selected.")


def get_ports():
    """Return a list of all the ports' paths."""

    return list(port.device for port in serial.tools.list_ports.comports())
