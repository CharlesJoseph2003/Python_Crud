import board
import busio
from adafruit_seesaw import seesaw, rotaryio, digitalio, neopixel



class encoders():
    def __init__(self):
        self.i2c = busio.I2C(board.SCL, board.SDA)
        self.addresses = [0x36, 0x37, 0x38, 0x39, 0x3a, 0x3b, 0x3c, 0x3d]
        self.qt_enc = [seesaw.Seesaw(self.i2c, addr=adr) for adr in self.addresses]
        self.button = []
        self.button_held = []
        self.last_position = []
        self.encoder = []
        self.pixel = []

        for addr in range(len(self.addresses)):
            self.qt_enc[addr].pin_mode(24, self.qt_enc[addr].INPUT_PULLUP)
            self.button.append(digitalio.DigitalIO(self.qt_enc[addr], 24))
            self.button_held.append(False)
            self.encoder.append(rotaryio.IncrementalEncoder(self.qt_enc[addr]))
            self.last_position.append(None)
            self.pixel.append(neopixel.NeoPixel(self.qt_enc[addr], 6, 1))
            self.pixel[addr].brightness = 0.2
            self.pixel[addr].fill(0xff0000)

       

encoder.button

i2c = busio.I2C(board.SCL, board.SDA)
addresses = [0x36, 0x37, 0x38, 0x39, 0x3a, 0x3b, 0x3c, 0x3d]


qt_enc = [seesaw.Seesaw(i2c, addr=adr) for adr in addresses]
button = []
button_held = []
last_position = []
encoder = []
pixel = []


for addr in range(len(addresses)):
    qt_enc[addr].pin_mode(24, qt_enc[addr].INPUT_PULLUP)
    button.append(digitalio.DigitalIO(qt_enc[addr], 24))
    button_held.append(False)
    encoder.append(rotaryio.IncrementalEncoder(qt_enc[addr]))
    last_position.append(None)
    pixel.append(neopixel.NeoPixel(qt_enc[addr], 6, 1))
    pixel[addr].brightness = 0.2
    pixel[addr].fill(0xff0000)

while True:
    for addr in range(len(addresses)):
        position = -encoder[addr].position

        if position != last_position[addr]:
            last_position[addr] = position
            # print("Position {}: {}".format(addr, position))

        if not button[addr].value and not button_held[addr]:
            button_held[addr] = True
            pixel[addr].brightness = 0.5
            # print("Button {} pressed".format(addr))

        if button[addr].value and button_held[addr]:
            button_held[addr] = False
            pixel[addr].brightness = 0.2
            # print("Button {} released".format(addr))

        if addr == 0:
            pixel[addr].fill(0xff0000)
        elif addr == 1:
            pixel[addr].fill(0x00ff00)
        elif addr == 2:
            pixel[addr].fill(0x0000ff)
        elif addr == 3:
            pixel[addr].fill(0xffff00)
        elif addr == 4:
            pixel[addr].fill(0xff00ff)
        elif addr == 5:
            pixel[addr].fill(0x00ffff)
        elif addr == 6:
            pixel[addr].fill(0xff0000)
        elif addr == 7:
            pixel[addr].fill(0x00ff00)

    print("Positions: ", [encoder[i].position for i in range(len(addresses))])
    # print("Button states: ", [button[i].value for i in range(len(addresses))])
    # print("Button held states: ", button_held)   
