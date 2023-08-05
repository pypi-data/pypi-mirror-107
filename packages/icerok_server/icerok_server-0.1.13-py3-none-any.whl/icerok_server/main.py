"""Main program"""

import time
import sys
from pathlib import Path
from serial import Serial
from serial.serialutil import SerialException
import serial.tools.list_ports
from .version import VERSION

BYTES = 8
FILENAME = "data.raw"


def receive_data(ser):
    """Receive the data from the FPGA"""

    print("\nWaiting for the Data from the FPGA...")
    count = 0
    while True:
        try:
            data = ser.read(BYTES)
        except KeyboardInterrupt:
            print("\nABORT...\n")
            ser.close()
            sys.exit()

        data_hex = [hex(d) for d in data]
        print(f"Data received ({len(data_hex)} bytes): ")
        print(f"{data_hex}")

        # Write the data to the file
        p = Path('.')
        f_data = p / FILENAME;
        f_data.write_bytes(data)

        print(f"FILE: {f_data.name}\n")



def _main():
    """Main function: entry point"""
    print("\nRUNNING...")
    print(f"VERSION: {VERSION}")

    # -- Read the device from the arguments
    if len(sys.argv) >= 2:
        devname = sys.argv[1]
    else:
        # -- No device given

        # -- Get all the serial devices
        ports = serial.tools.list_ports.comports(include_links=False)
        if len(ports) == 0:
            print("\nNo serial devices found\n")
            sys.exit(1)
        else:
            print("\nSerial devices found: ")
        for port in ports:
            print(f"* {port}")

        # -- If there are two devices, the second one is opened
        try:
            devname = ports[0].device
        except IndexError:
            print("\nNo serial device selected\n")
            sys.exit(1)

    # -- There is a device
    print(f"\nSerial device: {devname}")
    print("BAUDS: 12000000")

    # -- Open the serial port
    try:
        serial_p = Serial(devname, 12000000)
        time.sleep(0.2)
    except SerialException as exc:
        print("Error al abrir puerto serie ")
        msg = exc.args[1]
        print(msg)
        sys.exit()

    # -- Start the application
    receive_data(serial_p)


# -----------------------
# --    M A I N
# -----------------------
if __name__ == "__main__":
    _main()
