# arduino-rfid-5409

Replacing the barcode scanner with an RFID scanner.

This is meant to be a supplementary program to [FRC5409/GrizzlyTime](https://github.com/FRC5409/GrizzlyTime). Rather than typing or using a barcode scanner, users can scan an RFID tag/card instead.

## Hardware

- Arduino
- PN532

## Set up

This program assumes you already have GrizzlyTime set up.

### On computer:

Ensure you are in the project root directory.

1. [Install Python 3](https://www.python.org/) (tested on 3.11.4)
2. Install Python dependencies using `pip3 install -r requirements.txt`
3. Run the Python program by invoking it as a module using `python3 -m client`

### On Arduino:

1. Connect the PN532 to the Arduino using I2C (see [tutorial](https://www.wellpcb.com/interfacing-pn532-with-arduino.html))
2. Upload the code in the `arduino` directory (see [PlatformIO documentation](https://docs.platformio.org/en/stable/integration/ide/vscode.html))

## Maintenance

This program uses SQLite as its database. There is no functionality in the GUI to browse/edit the database. It is recommended to use [DB Browser for SQLite](https://sqlitebrowser.org/).
