'''
Original Launcher from pimoroni ported and modified for
CircuitPython by BeBoX(c)
email : depanet at gmail.com
twitter : @beboxos
edit from 03.2022
adafruit_epd.epd référence :
fill(color)
fill_rect(x, y, width, height, color)
rect(x, y, width, height, color)
hline(x, y, width, color)
vline(x, y, height, color)
line(x_0, y_0, x_1, y_1, color)
pixel(x, y, color)
rotation
text(string, x, y, color, *, font_name='font5x8.bin', size=1)
colors :
WHITE = 3
BLACK = 0
more : https://docs.circuitpython.org/projects/epd/en/latest/api.html
'''
#HID init
layout = "fr" # fr or us

import time
import usb_hid
from adafruit_hid.keyboard import Keyboard
import adafruit_ducky

keyboard = Keyboard(usb_hid.devices)
if layout=="fr": 
    from adafruit_hid.keyboard_layout_fr import KeyboardLayoutFR
    keyboard_layout = KeyboardLayoutFR(keyboard)  # We're in France :)
else:
    from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
    keyboard_layout = KeyboardLayoutUS(keyboard)  # We're in the US :)
def callduck(filename):
    duck = adafruit_ducky.Ducky(filename, keyboard, keyboard_layout)    
    result = True
    while result is not False:
        result = duck.loop()
    return result


import gc
import os
import math
import microcontroller
import board
import analogio

MAX_BATTERY_VOLTAGE = 4.0
MIN_BATTERY_VOLTAGE = 3.2

ebook=""

page = 0
font_size = 1

inverted = False

ListHIDFiles = os.listdir("/hid/")
hidfiles =[]
count = 0
for n in ListHIDFiles:
    if n[-4:]==".txt":
        if n[0:2]!="._":
            hidfiles.append((n.replace(".txt",""),count))
            count=count+1
hidfiles.append(("EXIT",count))
print(hidfiles)
files = os.listdir("/badges/")
bfiles = []
count = 0
for n in files:
    if n[-4:]==".txt":
        if n[0:2]!="._":
            bfiles.append((n.replace(".txt",""),count))
            count=count+1        
bfiles.append(("EXIT",count))
print(bfiles)
#picfiles
files = os.listdir("/images/")
picfiles = []
count = 0
for n in files:
    if n[-4:]==".bmp":
        if n[0:2]!="._":
            picfiles.append((n.replace(".bmp",""),count))
            count=count+1        
picfiles.append(("EXIT",count))
print(picfiles)
files = os.listdir("/ebook/")
ebfiles = []
count = 0
for n in files:
    if n[-4:]==".txt":
        if n[0:2]!="._":
            ebfiles.append((n.replace(".txt",""),count))
            count=count+1        
ebfiles.append(("EXIT",count))
print(ebfiles)
#fixed functions
examples = [
    ("keyb", 0),
    ("badge", 1),
    ("image", 2),
    ("ebook", 3),
    ("info", 4),
    ("prefs", 5)
]
count = 6
ListFiles = os.listdir("/apps/")
for n in ListFiles:
    if n[-3:]==".py":
        #need to impove, file to not show in menu
        #exlude secrets.py and of course code.py
        if n!="secrets.py" and n!="code.py" and n!="launcher.py" and n[0:2]!="._":
            examples.append((n.replace(".py",""),count))
            count=count+1

print(examples)
font_sizes = (0.5, 0.7, 0.9)

# Approximate center lines for buttons A, B and C
centers = (41, 147, 253)

#MAX_PAGE = math.ceil(len(examples) / 3)
from digitalio import DigitalInOut, Direction, Pull

button_a = DigitalInOut(board.SW_A)
button_a.direction = Direction.INPUT
button_a.pull = Pull.DOWN
button_b = DigitalInOut(board.SW_B)
button_b.direction = Direction.INPUT
button_b.pull = Pull.DOWN
button_c = DigitalInOut(board.SW_C)
button_c.direction = Direction.INPUT
button_c.pull = Pull.DOWN
button_up = DigitalInOut(board.SW_UP)
button_up.direction = Direction.INPUT
button_up.pull = Pull.DOWN
button_down = DigitalInOut(board.SW_DOWN)
button_down.direction = Direction.INPUT
button_down.pull = Pull.DOWN
# False = up , True = pressed

led = DigitalInOut(board.USER_LED)
led.direction = Direction.OUTPUT
#led.value = 1 for led on
#led.value = 0 for led off

# Inverted. For reasons.
button_user = board.USER_SW

# Battery measurement
'''
vbat_adc = machine.ADC(badger2040.PIN_BATTERY)
vref_adc = machine.ADC(badger2040.PIN_1V2_REF)
vref_en = machine.Pin(badger2040.PIN_VREF_POWER)
vref_en.init(machine.Pin.OUT)
vref_en.value(0)


display = badger2040.Badger2040()

'''
vbat_adc = analogio.AnalogIn(board.VBAT_SENSE)
#vref_adc = analogio.AnalogIn(board.1V2_REF)
vref_en = analogio.AnalogIn(board.VREF_POWER)
# ********************************* DISPLAY ******************************
try:
    import displayio                  # release displayio for epd driver use
    displayio.release_displays()      # thanks to Chris Parrot
except:
    print("No displayio , ok then it's alpha release")
import digitalio
import busio
from adafruit_epd.epd import Adafruit_EPD
from adafruit_epd.il0373 import Adafruit_IL0373
# create the spi device and pins we will need
try:
    spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
    # board.SCLK renamed to board.SCK
except:
    spi = busio.SPI(board.SCLK, MOSI=board.MOSI, MISO=board.MISO)
    print("alpha release declare spi different")
ecs = digitalio.DigitalInOut(board.INKY_CS)
dc = digitalio.DigitalInOut(board.INKY_DC)
srcs = None #digitalio.DigitalInOut(board.D10)    # can be None to use internal memory
rst = digitalio.DigitalInOut(board.INKY_RST)    # can be None to not use this pin
busy = digitalio.DigitalInOut(board.INKY_BUSY)   # can be None to not use this pin

# give them all to our driver
print("Creating display")
display = Adafruit_IL0373(128, 296, spi,          # 2,9" badger 296x128 display
                          cs_pin=ecs, dc_pin=dc, sramcs_pin=srcs,
                          rst_pin=rst, busy_pin=busy)

display.rotation = 3
WHITE = 3
BLACK = 0
WIDTH = 296
HEIGHT = 128
# ************************************************** diplay init end
def read_le(s):
    # as of this writting, int.from_bytes does not have LE support, DIY!
    result = 0
    shift = 0
    for byte in bytearray(s):
        result += byte << shift
        shift += 8
    return result


class BMPError(Exception):
    pass


def display_bitmap(epd, filename, x,y, deficon="file"):  # pylint: disable=too-many-locals, too-many-branches
    try:
        f = open(filename, "rb")  # pylint: disable=consider-using-with
    except OSError:
        print("Couldn't open file " + filename + " load default icon /assets/"+deficon+".bmp")
        f = open("/assets/"+deficon+".bmp", "rb")
        #return

    #print("File opened")
    try:
        if f.read(2) != b"BM":  # check signature
            raise BMPError("Not BitMap file")

        bmpFileSize = read_le(f.read(4))
        f.read(4)  # Read & ignore creator bytes

        bmpImageoffset = read_le(f.read(4))  # Start of image data
        headerSize = read_le(f.read(4))
        bmpWidth = read_le(f.read(4))
        bmpHeight = read_le(f.read(4))
        flip = True
        '''
        print(
            "Size: %d\nImage offset: %d\nHeader size: %d"
            % (bmpFileSize, bmpImageoffset, headerSize)
        )
        print("Width: %d\nHeight: %d" % (bmpWidth, bmpHeight))
        '''
        if read_le(f.read(2)) != 1:
            raise BMPError("Not singleplane")
        bmpDepth = read_le(f.read(2))  # bits per pixel
        #print("Bit depth: %d" % (bmpDepth))
        if bmpDepth != 24:
            raise BMPError("Not 24-bit")
            pass
        if read_le(f.read(2)) != 0:
            raise BMPError("Compressed file")

        #print("Image OK! Drawing...")

        rowSize = (bmpWidth * 3 + 3) & ~3  # 32-bit line boundary

        for row in range(bmpHeight):  # For each scanline...
            if flip:  # Bitmap is stored bottom-to-top order (normal BMP)
                pos = bmpImageoffset + (bmpHeight - 1 - row) * rowSize
            else:  # Bitmap is stored top-to-bottom
                pos = bmpImageoffset + row * rowSize

            # print ("seek to %d" % pos)
            f.seek(pos)
            rowdata = f.read(3 * bmpWidth)
            for col in range(bmpWidth):
                b, g, r = rowdata[3 * col : 3 * col + 3]  # BMP files store RGB in BGR
                if r < 0x80 and g < 0x80 and b < 0x80:
                    epd.pixel(col + x , row + y, BLACK)
                elif r >= 0x80 and g >= 0x80 and b >= 0x80:
                    pass  # epd.pixel(row, col, Adafruit_EPD.WHITE)
                elif r >= 0x80:
                    epd.pixel(col + x , row + y, BLACK)
    except OSError:
        print("Couldn't read file")
    except BMPError as e:
        print("Failed to parse BMP: " + e.args[0])
    finally:
        f.close()
    #print("Finished drawing")
# ******************************* END BMP iamge display functions
def map_value(input, in_min, in_max, out_min, out_max):
    return (((input - in_min) * (out_max - out_min)) / (in_max - in_min)) + out_min


def get_battery_level():
    # Enable the onboard voltage reference
    #vref_en.value

    # Calculate the logic supply voltage, as will be lower that the usual 3.3V when running off low batteries
    #vdd = 1.24 * (65535 / vref_adc.read_u16())
    #vbat = (vbat_adc.read_u16() / 65535) * 3 * vdd  # 3 in this is a gain, not rounding of 3.3V

    # Disable the onboard voltage reference
    #vref_en.value

    # Convert the voltage to a level to display onscreen
    #return int(map_value(vbat, MIN_BATTERY_VOLTAGE, MAX_BATTERY_VOLTAGE, 0, 4))
    '''
    need to be coded to read battery level in circuitpython , later , for now return fake value
    '''
    return 3


def draw_battery(level, x, y):
    display.rect(x, y, 19, 10, WHITE)
    display.rect(x + 19, y + 3, 2, 4, WHITE)
    display.rect(x + 1, y + 1, 17, 8, BLACK)
    if level < 1:
        display.line(x + 3, y, x + 3 + 10, y + 10, BLACK)
        display.line(x + 3 + 1, y, x + 3 + 11, y + 10, BLACK)
        display.line(x + 2 + 2, y - 1, x + 4 + 12, y + 11, WHITE)
        display.line(x + 2 + 3, y - 1, x + 4 + 13, y + 11, WHITE)
        return
    # Battery Bars
    for i in range(4):
        if level / 4 > (1.0 * i) / 4:
            display.fill_rect(i * 4 + x + 2, y + 2, 3, 6, WHITE)


def draw_disk_usage(x):
    # f_bfree and f_bavail should be the same?
    # f_files, f_ffree, f_favail and f_flag are unsupported.
    f_bsize, f_frsize, f_blocks, f_bfree, _, _, _, _, _, f_namemax = os.statvfs("/")
    f_total_size = f_frsize * f_blocks
    f_total_free = f_bsize * f_bfree
    f_total_used = f_total_size - f_total_free
    f_used = 100 / f_total_size * f_total_used
    # f_free = 100 / f_total_size * f_total_free
    display.rect(x + 10, 3, 80, 10, WHITE)
    display.fill_rect(x + 11, 4, 78, 8, BLACK)
    display.fill_rect(x + 12, 5, int(76 / 100.0 * f_used), 6, WHITE)
    display.text("{:.2f}%".format(f_used), x + 91, 4, WHITE)


def render(tablist, defaulticon="file"):
    # clear display
    print(defaulticon)
    print(tablist)
    MAX_PAGE = math.ceil(len(tablist) / 3)
    led.value = 1
    display.fill(WHITE)
    max_icons = min(3, len(tablist[(page * 3):]))
    for i in range(max_icons):
        x = centers[i]
        label, icon = tablist[i + (page * 3)]
        file = label
        display_bitmap(display, "/assets/"+file+".bmp", x-32 , 24, defaulticon)
        w = 50 # 30 seem correct for default font 5x8
        display.text(label[:5], x - int(w / 2), 16 + 80, BLACK, font_name='font5x8.bin', size=2)

    for i in range(MAX_PAGE):
        x = 286
        y = int((128 / 2) - (MAX_PAGE * 10 / 2) + (i * 10))
        display.fill_rect(x, y, 8, 8, BLACK)
        if page != i:
            display.fill_rect(x + 1, y + 1, 6, 6, WHITE)

    display.fill_rect(0, 0, WIDTH, 16, BLACK)
    draw_disk_usage(90)
    draw_battery(get_battery_level(), WIDTH - 22 - 3, 3)
    display.text("BadgerOS CPython", 3, 4,  WHITE)
    
    display.display()
    led.value = 0


def launch(file):
    fichier = "/apps/"+file+".py"
    print("file :" +  file + " --> " + fichier)
    
    for k in locals().keys():
        if k not in ("gc", "file", "machine"):
            del locals()[k]
    gc.collect()
    try:
        __import__(fichier)  # Try to import _[file] (drop underscore prefix)
    except ImportError:
        pass
        #__import__(file)      # Failover to importing [_file]
    #machine.reset()           # Exit back to launcher
    import microcontroller
    microcontroller.reset()

# important root routine ------------------------------------------------------------
def launch_example(index):
    global page, font_size, inverted
    print("index : "+str(index))
    print(examples[(page * 3) + index][0])
    if (page * 3) + index == 0:
        hidexit=False
        #special action rubber ducky
        while button_a.value==True:
            time.sleep(0.01)
        # keyb
        print("Keyboard emul zone")
        render(hidfiles,"text")
        while hidexit==False:
            if button_a.value==True:
                while button_a.value==True:
                    time.sleep(0.01)
                if hidbutton(1)==False:
                    hidexit=True
            if button_b.value==True:
                while button_b.value==True:
                    time.sleep(0.01)                
                if hidbutton(2)==False:
                    hidexit=True
            if button_c.value==True:
                while button_c.value==True:
                    time.sleep(0.01)                
                if hidbutton(3)==False:
                    hidexit=True
            if button_up.value==True:
                hidbutton(4)
            if button_down.value==True:
                hidbutton(5)            
            time.sleep(0.01)
        page=0
        render(examples,"file")
        return
    if (page * 3) + index == 1:
        #badge section
        badgeexit=False
        while button_b.value==True:
            time.sleep(0.01)
        print("badge zone")
        
        render(bfiles,"userid")
        while badgeexit==False:
            if button_a.value==True:
                while button_a.value==True:
                    time.sleep(0.01)
                if badgebutton(1)==False:
                    badgeexit=True
            if button_b.value==True:
                while button_b.value==True:
                    time.sleep(0.01)                
                if badgebutton(2)==False:
                    badgeexit=True
            if button_c.value==True:
                while button_c.value==True:
                    time.sleep(0.01)                
                if badgebutton(3)==False:
                    badgeexit=True
            if button_up.value==True:
                badgebutton(4)
            if button_down.value==True:
                badgebutton(5)            
            time.sleep(0.01)
        page=0
        render(examples,"file")
        return            
    if (page * 3) + index == 2:
        # show image routine
        imgexit=False
        while button_b.value==True:
            time.sleep(0.01)
        print("image zone")
        
        render(picfiles,"bmp")
        while imgexit==False:
            if button_a.value==True:
                while button_a.value==True:
                    time.sleep(0.01)
                if imgbutton(1)==False:
                    imgexit=True
            if button_b.value==True:
                while button_b.value==True:
                    time.sleep(0.01)                
                if imgbutton(2)==False:
                    imgexit=True
            if button_c.value==True:
                while button_c.value==True:
                    time.sleep(0.01)                
                if imgbutton(3)==False:
                    imgexit=True
            if button_up.value==True:
                imgbutton(4)
            if button_down.value==True:
                imgbutton(5)            
            time.sleep(0.01)
        page=0
        render(examples,"file")
        return         
    if (page * 3) + index == 3:
        # ebook Reader function
        ebexit=False
        oldpage = 1
        page = 0
        while button_a.value==True:
            time.sleep(0.01)
        print("ebook zone")
        print(ebfiles)
        render(ebfiles,"text")
        print("rendered")
        while ebexit==False:
            if button_a.value==True:
                while button_a.value==True:
                    time.sleep(0.01)
                if ebookbutton(1)==False:
                    ebexit=True
            if button_b.value==True:
                while button_b.value==True:
                    time.sleep(0.01)                
                if ebookbutton(2)==False:
                    ebexit=True
            if button_c.value==True:
                while button_c.value==True:
                    time.sleep(0.01)                
                if ebookbutton(3)==False:
                    ebexit=True
            if button_up.value==True:
                ebookbutton(4)
            if button_down.value==True:
                ebookbutton(5)            
            time.sleep(0.01)        
        # back to main
        print('exit ebook')
        try:
            ebook.close()
        except:
            print("ebook allready closed")
        page=1
        render(examples,"file")
        return          
    if (page * 3) + index == 4:
        # info
        print("infos ...")
        return
    if (page * 3) + index == 5:
        # prefs
        print("prefs ...")
        return
    else:    
        try:
            print(examples[(page * 3) + index][0])
            launch(examples[(page * 3) + index][0])
            return True
        except IndexError:
            return False

def ebookbutton(pin):
    global page, font_size, inverted
    #if button_user.value():  # User button is NOT held down
    print("ebook bouton : "+str(pin))
    if pin == 1:
        if ebselect(0)==False:
            return False
    if pin == 2:
        if ebselect(1)==False:
            return False
    if pin == 3:
        if ebselect(2)==False:
            return False
    if pin == 4:
        MAX_PAGE = math.ceil(len(bfiles) / 3)
        if page > 0:
            page -= 1
            render(ebfiles,"text")
    if pin == 5:
        MAX_PAGE = math.ceil(len(bfiles) / 3)
        if page < MAX_PAGE - 1:
            page += 1
            render(ebfiles,"text")

def ebselect(index):
    global page, font_size, inverted
    name = ebfiles[(page * 3) + index][0]
    print("/ebook/"+name+".txt")
    if name == "EXIT":
        #hidexit=True
        return False
    else:
        #wait release
        while button_a.value==True or button_b.value==True or button_c.value==True:
            time.sleep(0.01) 
        # ici
        ebookfile= "/ebook/"+name+".txt"
        readebook(ebookfile)                      
        render(ebfiles,"text")
        return True   

def readebook(efile):
    global next_page, prev_page,last_offset,current_page, ebook
    print("go to read" + efile + " ebook")
    ebook = open(efile, "r")
    while True:
        # Was the next page button pressed?
        if next_page:
            current_page += 1

            # Is the next page one we've not displayed before?
            if current_page > len(offsets):
                offsets.append(ebook.tell())  # Add its start position to the offsets list
            led.value=1
            draw_frame()
            render_page()
            led.value=0
            next_page = False  # Clear the next page button flag

        # Was the previous page button pressed?
        if prev_page:
            if current_page > 1:
                current_page -= 1
                ebook.seek(offsets[current_page - 1])  # Retrieve the start position of the last page
                led.value=1
                draw_frame()
                render_page()
                led.value=0
            prev_page = False  # Clear the prev page button flag


        if button_a.value==True:
            return True
        if button_b.value==True:
            return True
        if button_c.value==True:
            return True
        if button_up.value==True:
            while button_up.value==True:
                time.sleep(0.01)
            ebbutton(4)
        if button_down.value==True:
            while button_down.value==True:
                time.sleep(0.01)        
            ebbutton(5)
        time.sleep(0.1)    

def imgbutton(pin):
    global page, font_size, inverted

    #if button_user.value():  # User button is NOT held down
    if pin == 1:
        if img(0)==False:
            return False
    if pin == 2:
        if img(1)==False:
            return False
    if pin == 3:
        if img(2)==False:
            return False
    if pin == 4:
        MAX_PAGE = math.ceil(len(bfiles) / 3)
        if page > 0:
            page -= 1
            render(picfiles,"bmp")
    if pin == 5:
        MAX_PAGE = math.ceil(len(bfiles) / 3)
        if page < MAX_PAGE - 1:
            page += 1
            render(picfiles,"bmp")

def img(index):    
    name = picfiles[(page * 3) + index][0]
    print("/image/"+name+".bmp")
    if name == "EXIT":
        #hidexit=True
        return False
    else:
        #wait release
        while button_a.value==True or button_b.value==True or button_c.value==True:
            time.sleep(0.01) 
        led.value=1
        # ici
        display.fill(WHITE)
        display_bitmap(display, "/images/"+name+".bmp", 0 , 0, "bmp")
        display.display()
        led.value=0
        #wait a a b or c button
        while button_a.value==False and button_b.value==False and button_c.value==False:
            time.sleep(0.01)            
        #wait release
        while button_a.value==True or button_b.value==True or button_c.value==True:
            time.sleep(0.01)                         
        render(picfiles,"bmp")
        return True


def badgebutton(pin):
    global page, font_size, inverted

    #if button_user.value():  # User button is NOT held down
    if pin == 1:
        if badge(0)==False:
            return False
    if pin == 2:
        if badge(1)==False:
            return False
    if pin == 3:
        if badge(2)==False:
            return False
    if pin == 4:
        MAX_PAGE = math.ceil(len(bfiles) / 3)
        if page > 0:
            page -= 1
            render(bfiles,"userid")
    if pin == 5:
        MAX_PAGE = math.ceil(len(bfiles) / 3)
        if page < MAX_PAGE - 1:
            page += 1
            render(bfiles,"userid")

def badge(index):    
    name = bfiles[(page * 3) + index][0]
    print("/badge/"+name+".txt")
    if name == "EXIT":
        #hidexit=True
        return False
    else:
        #wait release
        while button_a.value==True or button_b.value==True or button_c.value==True:
            time.sleep(0.01) 
        led.value=1
        draw_badge(name)
        led.value=0
        #wait a a b or c button
        while button_a.value==False and button_b.value==False and button_c.value==False:
            time.sleep(0.01)            
        #wait release
        while button_a.value==True or button_b.value==True or button_c.value==True:
            time.sleep(0.01)                         
        render(bfiles,"userid")
        return True


def hid(index):    
    name = hidfiles[(page * 3) + index][0]
    print("/hid/"+name+".txt")
    if name == "EXIT":
        hidexit=True
        return False
    else:
        led.value=1
        callduck("/hid/"+name+".txt")
        led.value=0
        return True

def hidbutton(pin):
    global page, font_size, inverted

    #if button_user.value():  # User button is NOT held down
    if pin == 1:
        if hid(0)==False:
            return False
    if pin == 2:
        if hid(1)==False:
            return False
    if pin == 3:
        if hid(2)==False:
            return False
    if pin == 4:
        MAX_PAGE = math.ceil(len(hidfiles) / 3)
        if page > 0:
            page -= 1
            render(hidfiles,"text")
    if pin == 5:
        MAX_PAGE = math.ceil(len(hidfiles) / 3)
        if page < MAX_PAGE - 1:
            page += 1
            render(hidfiles,"text")

def button(pin):
    global page, font_size, inverted
    print( "button pin : "+ str(pin))
    #if button_user.value():  # User button is NOT held down
    if pin == 1:
        launch_example(0)
    if pin == 2:
        launch_example(1)
    if pin == 3:
        launch_example(2)
    if pin == 4:
        MAX_PAGE = math.ceil(len(examples) / 3)
        if page > 0:
            page -= 1
            render(examples)
        else:
            page= MAX_PAGE -1
            render(examples)
    if pin == 5:
        MAX_PAGE = math.ceil(len(examples) / 3)
        if page < MAX_PAGE - 1:
            page += 1
            render(examples)
        else:
            page=0
            render(examples)

def draw_badge(file):
    logo = file
    try:
        f = open("/badges/"+file+".bmp","r")
        f.close()
    except:
        logo = "user"
    f = open("/badges/"+file+".txt","r")
    company = f.readline()
    name = f.readline()
    detail1_title = f.readline()
    detail1_text = f.readline()
    detail2_title = f.readline()
    detail2_text = f.readline()
    f.close()    
    #Constants cans be customised
    IMAGE_WIDTH = 104

    COMPANY_HEIGHT = 40
    DETAILS_HEIGHT = 20
    NAME_HEIGHT = HEIGHT - COMPANY_HEIGHT - (DETAILS_HEIGHT * 2) - 2
    TEXT_WIDTH = WIDTH - IMAGE_WIDTH - 1
    LEFT_PADDING = 10
    NAME_PADDING = 20
    DETAIL_SPACING = 20
    OVERLAY_BORDER = 40
    OVERLAY_SPACING = 20
    # clear scren (black)
    display.fill(BLACK)
    # Draw a border around the image
    display.line(WIDTH - IMAGE_WIDTH, 0, WIDTH - 1, 0, WHITE)
    display.line(WIDTH - IMAGE_WIDTH, 0, WIDTH - IMAGE_WIDTH, HEIGHT - 1, WHITE)
    display.line(WIDTH - IMAGE_WIDTH, HEIGHT - 1, WIDTH - 1, HEIGHT - 1, WHITE)
    display.line(WIDTH - 1, 0, WIDTH - 1, HEIGHT - 1, WHITE)
    # Draw the company
    display.text(company, LEFT_PADDING, (COMPANY_HEIGHT // 2) -10,WHITE,font_name='font5x8.bin', size=2 )

    # Draw a white background behind the name
    display.fill_rect(1, COMPANY_HEIGHT + 1, TEXT_WIDTH, NAME_HEIGHT, WHITE)

    # Draw the name, scaling it based on the available width
    fsize = 3
    name_length = len(name)*(fsize*6)
    if name_length >= (TEXT_WIDTH - NAME_PADDING):
        fsize=2
        name_length = len(name)*(fsize*6)
        if name_length >= (TEXT_WIDTH - NAME_PADDING):
            fsize=1
            name_length = len(name)*(fsize*6)            
    display.text(name, (TEXT_WIDTH - name_length) // 2, (NAME_HEIGHT // 2) + COMPANY_HEIGHT - 5, BLACK, font_name='font5x8.bin', size=fsize)

    # Draw a white backgrounds behind the details
    display.fill_rect(1, HEIGHT - DETAILS_HEIGHT * 2, TEXT_WIDTH, DETAILS_HEIGHT - 1, WHITE)
    display.fill_rect(1, HEIGHT - DETAILS_HEIGHT, TEXT_WIDTH, DETAILS_HEIGHT - 1, WHITE)

    # Draw the first detail's title and text
    name_length = len(detail1_title)*5
    display.text(detail1_title, LEFT_PADDING, HEIGHT - ((DETAILS_HEIGHT * 3) // 2) -5, BLACK, font_name='font5x8.bin', size=1)
    display.text(detail1_text,  LEFT_PADDING + name_length + DETAIL_SPACING, HEIGHT - ((DETAILS_HEIGHT * 3) // 2) -5,  BLACK, font_name='font5x8.bin', size=1)

    # Draw the second detail's title and text
    name_length = len(detail2_title)*5
    display.text(detail2_title, LEFT_PADDING, HEIGHT - (DETAILS_HEIGHT // 2) -5, BLACK, font_name='font5x8.bin', size=1)
    display.text(detail2_text, LEFT_PADDING + name_length + DETAIL_SPACING, HEIGHT - (DETAILS_HEIGHT // 2) -5, BLACK, font_name='font5x8.bin', size=1)
    # Draw badge image
    display.fill_rect(WIDTH - IMAGE_WIDTH , 0, WIDTH, HEIGHT, WHITE)
    print(logo)
    display_bitmap(display, "/badges/"+logo+".bmp", WIDTH - IMAGE_WIDTH , 0)
    display.display()

ARROW_THICKNESS = 3
ARROW_WIDTH = 18
ARROW_HEIGHT = 14
ARROW_PADDING = 2
TEXT_PADDING = 4
TEXT_SIZE = 0.5
TEXT_SPACING = int(34 * TEXT_SIZE)
TEXT_WIDTH = WIDTH - TEXT_PADDING - TEXT_PADDING - ARROW_WIDTH

# Draw a upward arrow
def draw_up(x, y, width, height, thickness, padding):
    border = (thickness // 4) + padding
    display.line(x + border, y + height - border,
                 x + (width // 2), y + border, WHITE)
    display.line(x + (width // 2), y + border,
                 x + width - border, y + height - border, WHITE)
# Draw a downward arrow
def draw_down(x, y, width, height, thickness, padding):
    border = (thickness // 2) + padding
    display.line(x + border, y + border,
                 x + (width // 2), y + height - border, WHITE)
    display.line(x + (width // 2), y + height - border,
                 x + width - border, y + border, WHITE)

# Draw the frame of the text reader
def draw_frame():
    display.fill(WHITE)
    display.fill_rect(WIDTH - ARROW_WIDTH, 0, ARROW_WIDTH, HEIGHT, BLACK)
    if current_page > 1:
        draw_up(WIDTH - ARROW_WIDTH, (HEIGHT // 4) - (ARROW_HEIGHT // 2),
                ARROW_WIDTH, ARROW_HEIGHT, ARROW_THICKNESS, ARROW_PADDING)
    draw_down(WIDTH - ARROW_WIDTH, ((HEIGHT * 3) // 4) - (ARROW_HEIGHT // 2),
              ARROW_WIDTH, ARROW_HEIGHT, ARROW_THICKNESS, ARROW_PADDING)

next_page = True
prev_page = False
last_offset = 0
current_page = 0
offsets = []
def ebbutton(pin):
    global next_page, prev_page, change_font_size, change_font
    if pin == 5:
        next_page = True

    if pin == 4:
        prev_page = True
# ------------------------------
#         Render page
# ------------------------------

def render_page():
    global next_page, prev_page, change_font_size, change_font, ebook
    row = 0
    line = ""
    pos = ebook.tell()
    next_pos = pos
    add_newline = False
    #display.font(FONTS[0])
    led.value=1
    while True:
        # Read a full line and split it into words
        words = ebook.readline().split(" ")

        # Take the length of the first word and advance our position
        next_word = words[0]
        if len(words) > 1:
            next_pos += len(next_word) + 1
        else:
            next_pos += len(next_word)  # This is the last word on the line

        # Advance our position further if the word contains special characters
        if '\u201c' in next_word:
            next_word = next_word.replace('\u201c', '\"')
            next_pos += 2
        if '\u201d' in next_word:
            next_word = next_word.replace('\u201d', '\"')
            next_pos += 2
        if '\u2019' in next_word:
            next_word = next_word.replace('\u2019', '\'')
            next_pos += 2

        # Rewind the file back from the line end to the start of the next word
        ebook.seek(next_pos)

        # Strip out any new line characters from the word
        next_word = next_word.strip()

        # If an empty word is encountered assume that means there was a blank line
        if len(next_word) == 0:
            add_newline = True

        # Append the word to the current line and measure its length
        appended_line = line
        if len(line) > 0 and len(next_word) > 0:
            appended_line += " "
        appended_line += next_word
        appended_length = len(appended_line)*6

        # Would this appended line be longer than the text display area, or was a blank line spotted?
        if appended_length >= TEXT_WIDTH or add_newline:

            # Yes, so write out the line prior to the append
            print(line)
            #display.pen(0)
            #display.thickness(FONT_THICKNESSES[0])
            display.text(line, TEXT_PADDING, (row * TEXT_SPACING) + (TEXT_SPACING // 2) + TEXT_PADDING, BLACK)

            # Clear the line and move on to the next row
            line = ""
            row += 1

            # Have we reached the end of the page?
            if (row * TEXT_SPACING) + TEXT_SPACING >= HEIGHT:
                print("+++++")
                display.display()

                # Reset the position to the start of the word that made this line too long
                ebook.seek(pos)
                return
            else:
                # Set the line to the word and advance the current position
                line = next_word
                pos = next_pos

            # A new line was spotted, so advance a row
            if add_newline:
                print("")
                row += 1
                if (row * TEXT_SPACING) + TEXT_SPACING >= HEIGHT:
                    print("+++++")
                    display.display()
                    return
                add_newline = False
        else:
            # The appended line was not too long, so set it as the line and advance the current position
            line = appended_line
            pos = next_pos
    

render(examples, "files")


# Wait for wakeup button to be released
while button_a.value==True or button_b.value==True or button_c.value==True or button_up.value==True or button_down.value==True:
    pass

# main loop root 
while True:
    if button_a.value==True:
        button(1)
    if button_b.value==True:
        button(2)
    if button_c.value==True:
        button(3)
    if button_up.value==True:
        button(4)
    if button_down.value==True:
        button(5)
    time.sleep(0.01)
