import usb_hid
import time
import board
import adafruit_touchscreen
from adafruit_pyportal import PyPortal

from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode

from adafruit_hid.consumer_control import ConsumerControl
from adafruit_hid.consumer_control_code import ConsumerControlCode
 
keyboard_active = False

#Initiallize the Keyboard
try:
  kbd = Keyboard(usb_hid.devices)
  keyboard_active = True
except OSError:
  keyboard_active = False

cc = ConsumerControl(usb_hid.devices)  


# the current working directory (where this file is)
cwd = ("/"+__file__).rsplit('/', 1)[0]

#Initialize the Pyportal with the default_bg set to the BMP file with all your icons.
pyportal = PyPortal(url='',
                    json_path='',
                    status_neopixel=board.NEOPIXEL,
                    default_bg=cwd+"/buttons.BMP",
                    text_font=cwd+"/fonts/Arial-ItalicMT-17.bdf",
                    text_position=((100, 129), (155, 180)),
                    text_color=(0x000000, 0x000000),
                    caption_text='',
                    caption_font=cwd+"/fonts/Arial-ItalicMT-17.bdf",
                    caption_position=(40, 220),
                    caption_color=0x000000)

# These pins are used as both analog and digital! XL, XR and YU must be analog
# and digital capable. YD just need to be digital
ts = adafruit_touchscreen.Touchscreen(board.TOUCH_XL, board.TOUCH_XR,
                                      board.TOUCH_YD, board.TOUCH_YU,
                                      calibration=((5200, 59000), (5800, 57000)),
                                      size=(320, 240))
p_list = []
while True :

  # If the keyboard is active then we can use the PyPortal like a keyboard (USB HID)
  if keyboard_active:
    p = ts.touch_point
    if p:

      # append each touch connection to a list
      # I had an issue with the first touch detected not being accurate
      p_list.append(p)

      #affter three trouch detections have occured. 
      if len(p_list) == 3:


        #discard the first touch detection and average the other two get the x,y of the touch
        x = (p_list[1][0]+p_list[2][0])/2
        y = (p_list[1][1]+p_list[2][1])/2
        print(x,y)



        # I will refer the the icon/button matrix using the following grid.
        # A1 is the icon/button in the top left corner looking at the PyPortal
        # D3 is the icon/button in the bottom right corner
        # +---+----+----+----+----+
        # |   | A  | B  | C  | D  |
        # +---+----+----+----+----+
        # | 1 | A1 | B1 | C1 | D1 |
        # | 2 | A2 | B2 | C2 | D2 |
        # | 3 | A3 | B3 | C3 | D3 |
        # +---+----+----+----+----+


        # For each button/icon pressed we send a keyboard command using kbd.send
        # this can send multiple key presses as if you were pressing them all at the same time
        # I use a mac and have configured each one of my shortcuts to open an application 
        # using ALT+Control+Shift+Command+[some letter] 
        # These shortcuts trigger an application to launch that was configured using Automator 

        # Column A
        if x > 22.5 and x < 72.5:
          # Icon/Button A1
          if y > 25 and y < 75:
            kbd.send(Keycode.CONTROL, Keycode.SHIFT, Keycode.F1)
            time.sleep(.2)
          # Icon/Button A2
          elif y > 100 and y < 150:
            kbd.send(Keycode.CONTROL, Keycode.SHIFT, Keycode.F2)
            time.sleep(.2)
          # Icon/Button A3  
          elif y > 175 and y < 225:
            kbd.send(Keycode.CONTROL, Keycode.SHIFT, Keycode.F3)
            time.sleep(.2)
  

        # Column B
        elif x > 97.5 and x < 147.5:
          # Icon/Button B1 
          if y > 25 and y < 75:
            kbd.send(Keycode.CONTROL, Keycode.SHIFT, Keycode.F6)
            time.sleep(.2)
          # Icon/Button B2
          elif y > 100 and y < 150:
            kbd.send(Keycode.CONTROL, Keycode.SHIFT, Keycode.F7)
            time.sleep(.2)
          # Icon/Button B3 
          elif y > 175 and y < 225:
            kbd.send(Keycode.CONTROL, Keycode.SHIFT, Keycode.F8)
            time.sleep(.2)
  

        # Column C
        elif x > 172.5 and x < 222.5:
          # Icon/Button C1 
          if y > 25 and y < 75:
            kbd.send(Keycode.CONTROL, Keycode.SHIFT, Keycode.F9)
            time.sleep(.2)

          # Icon/Button C2
          elif y > 100 and y < 150:
            kbd.send(Keycode.CONTROL, Keycode.SHIFT, Keycode.F10)
            time.sleep(.2)
          # Icon/Button C3
          elif y > 175 and y < 225:
            cc.send(ConsumerControlCode.VOLUME_DECREMENT)
            time.sleep(.2)
            #kbd.send(Keycode.CONTROL, Keycode.COMMAND,Keycode.SHIFT,Keycode.T & .2 sec sleep for each button, for preformance)

        # Column D 
        elif x > 247.5 and x < 297.5:
          # Icon/Button D1
          if y > 25 and y < 75:
            kbd.send(Keycode.CONTROL, Keycode.SHIFT, Keycode.F11)
            time.sleep(.2)  
          # Icon/Button D2
          elif y > 100 and y < 150:
            kbd.send(Keycode.CONTROL, Keycode.SHIFT, Keycode.F12)
            time.sleep(.2)
          # Icon/Button D3
          elif y > 175 and y < 225:
            cc.send(ConsumerControlCode.VOLUME_INCREMENT)
            time.sleep(.2)
            #kbd.send(Keycode.ALT,Keycode.CONTROL, Keycode.COMMAND ,Keycode.SHIFT,Keycode.S) 

        # clear list for next detection
        p_list = []

        # sleap to avoid pressing two buttons on accident
        time.sleep(.5)