#!/usr/bin/python

### import guacamole libraries
import avango
import avango.daemon
import os


## Initializes AR Track on LCD wall.
def init_lcd_wall_tracking():

  # create instance of DTrack
  _dtrack = avango.daemon.DTrack()
  _dtrack.port = "5000" # ART port at LCD wall
  
  _dtrack.stations[2] = avango.daemon.Station('tracking-lcd-glasses-athena') # athena tracking glasses
  _dtrack.stations[5] = avango.daemon.Station('tracking-lcd-glasses-1') # LCD wall glasses
  _dtrack.stations[8] = avango.daemon.Station('tracking-lcd-glasses-2') # SAMSUNG 3D-TV glasses
  _dtrack.stations[10] = avango.daemon.Station('tracking-lcd-glasses-3') # MITSUBISHI 3D-TV glasses

  _dtrack.stations[4] = avango.daemon.Station('tracking-lcd-prop-1') # LHT1
  _dtrack.stations[14] = avango.daemon.Station('tracking-lcd-prop-2') # LHT2

  _dtrack.stations[16] = avango.daemon.Station('tracking-black-block') # black block

  _dtrack.stations[20] = avango.daemon.Station('canon-pointer')
  _dtrack.stations[27] = avango.daemon.Station('blue-pointer')

  device_list.append(_dtrack)
  print("ART Tracking started at LCD WALL")


## Initializes AR Track on DLP wall.
def init_dlp_wall_tracking():

  # create instance of DTrack
  _dtrack = avango.daemon.DTrack()
  _dtrack.port = "5002" # ART port at LED wall
  
  # glasses
  _dtrack.stations[1] = avango.daemon.Station('tracking-dlp-glasses-3')
  _dtrack.stations[2] = avango.daemon.Station('tracking-dlp-glasses-4')
  _dtrack.stations[5] = avango.daemon.Station('tracking-dlp-glasses-6')
  _dtrack.stations[31] = avango.daemon.Station('tracking-dlp-glasses-n_1')
  _dtrack.stations[32] = avango.daemon.Station('tracking-dlp-glasses-2_1')
  _dtrack.stations[33] = avango.daemon.Station('tracking-dlp-glasses-3_1')

  _dtrack.stations[27] = avango.daemon.Station('scooter_pointer')
  #_dtrack.stations[23] = avango.daemon.Station('scooter_leg_pointer')
  _dtrack.stations[14] = avango.daemon.Station('scooter_leg_pointer')


  device_list.append(_dtrack)
  print("ART Tracking started at DLP WALL")


## Initializes a spacemouse for navigation.
def init_spacemouse():

  _string = os.popen("python find_device.py 1 3Dconnexion SpaceNavigator").read()

  if len(_string) == 0:
    _string = os.popen("python find_device.py 1 3Dconnexion SpaceTraveler USB").read()

  _string = _string.split()
  if len(_string) > 0:  

    _string = _string[0]
  
    # create a station to propagate the input events
    _spacemouse = avango.daemon.HIDInput()
    _spacemouse.station = avango.daemon.Station('device-spacemouse')
    _spacemouse.device = _string

    # map incoming spacemouse events to station values
    _spacemouse.values[0] = "EV_ABS::ABS_X"   # trans X
    _spacemouse.values[1] = "EV_ABS::ABS_Z"   # trans Y
    _spacemouse.values[2] = "EV_ABS::ABS_Y"   # trans Z
    _spacemouse.values[3] = "EV_ABS::ABS_RX"  # rotate X
    _spacemouse.values[4] = "EV_ABS::ABS_RZ"  # rotate Y
    _spacemouse.values[5] = "EV_ABS::ABS_RY"  # rotate Z

    # buttons
    _spacemouse.buttons[0] = "EV_KEY::BTN_0"  # left button
    _spacemouse.buttons[1] = "EV_KEY::BTN_1"  # right button

    device_list.append(_spacemouse)
    print("SpaceMouse started at:", _string)

  else:
    print("SpaceMouse NOT found !")


def init_new_spacemouse():

  _string = os.popen("python find_device.py 1 3Dconnexion SpaceNavigator for Notebooks").read()

  _string = _string.split()
  if len(_string) > 0:  
    _string = _string[0]
  
    # create a station to propagate the input events
    _spacemouse = avango.daemon.HIDInput()
    _spacemouse.station = avango.daemon.Station('device-spacemouse')
    _spacemouse.device = _string
    _spacemouse.timeout = '10'

    # map incoming spacemouse events to station values
    _spacemouse.values[0] = "EV_REL::REL_X"   # trans X
    _spacemouse.values[1] = "EV_REL::REL_Z"   # trans Y
    _spacemouse.values[2] = "EV_REL::REL_Y"   # trans Z
    _spacemouse.values[3] = "EV_REL::REL_RX"  # rotate X
    _spacemouse.values[4] = "EV_REL::REL_RZ"  # rotate Y
    _spacemouse.values[5] = "EV_REL::REL_RY"  # rotate Z

    # buttons
    _spacemouse.buttons[0] = "EV_KEY::BTN_0"  # left button
    _spacemouse.buttons[1] = "EV_KEY::BTN_1"  # right button

    device_list.append(_spacemouse)
    print("NewSpaceMouse started at:", _string)

  else:
    print("NewSpaceMouse NOT found !")


def init_xbox_controller():

  _string = os.popen("python find_device.py 1 Xbox 360 Wireless Receiver").read()

  _string = _string.split()
  if len(_string) > 0:
    _string = _string[0]
  
    # create a station to propagate the input events
    _xbox = avango.daemon.HIDInput()
    _xbox.station = avango.daemon.Station('device-xbox')
    _xbox.device = _string
    #_xbox.timeout = '10'

    # map incoming spacemouse events to station values
    _xbox.values[0] = "EV_ABS::ABS_X"
    _xbox.values[1] = "EV_ABS::ABS_Y"
    
    _xbox.values[2] = "EV_ABS::ABS_RX"


    device_list.append(_xbox)
    print("Xbox-360 Controller started at:", _string)

  else:
    print("Xbox-360 Controller NOT found !")


def init_keyboard():

  _string = os.popen("ls /dev/input/by-id | grep \"-event-kbd\" | sed -e \'s/\"//g\'  | cut -d\" \" -f4").read()
  
  _string = _string.split()
  
  if len(_string) > 0:
    _string = _string[0]
    
    _keyboard = avango.daemon.HIDInput()
    _keyboard.station = avango.daemon.Station('device-keyboard')
    _keyboard.device = "/dev/input/by-id/" + _string
    
    _keyboard.buttons[0] = "EV_KEY::KEY_KPPLUS"
    _keyboard.buttons[1] = "EV_KEY::KEY_KPMINUS"
    _keyboard.buttons[2] = "EV_KEY::KEY_W"
    _keyboard.buttons[3] = "EV_KEY::KEY_A"
    _keyboard.buttons[4] = "EV_KEY::KEY_S"
    _keyboard.buttons[5] = "EV_KEY::KEY_D"
    _keyboard.buttons[6] = "EV_KEY::KEY_PAGEUP"
    _keyboard.buttons[7] = "EV_KEY::KEY_PAGEDOWN"
    _keyboard.buttons[8] = "EV_KEY::KEY_LEFT"
    _keyboard.buttons[9] = "EV_KEY::KEY_RIGHT"
    _keyboard.buttons[10] = "EV_KEY::KEY_UP"
    _keyboard.buttons[11] = "EV_KEY::KEY_DOWN"
    
    _keyboard.buttons[12] = "EV_KEY::KEY_1"
    _keyboard.buttons[13] = "EV_KEY::KEY_2"
    _keyboard.buttons[14] = "EV_KEY::KEY_3"     
    _keyboard.buttons[15] = "EV_KEY::KEY_4"
    _keyboard.buttons[16] = "EV_KEY::KEY_5"
    _keyboard.buttons[17] = "EV_KEY::KEY_6"
    _keyboard.buttons[18] = "EV_KEY::KEY_SPACE"
    _keyboard.buttons[19] = "EV_KEY::KEY_LEFTCTRL"
    
    device_list.append(_keyboard)
    
    print("Keyboard started at:", _string)
  
  else:
    print("Keyboard NOT found !")
		

def init_mouse():

	_string = os.popen("ls /dev/input/by-id | grep \"-event-mouse\" | sed -e \'s/\"//g\'  | cut -d\" \" -f4").read()

	_string = _string.split()
	if len(_string) > 0:

		_string = _string[0]

		_mouse = avango.daemon.HIDInput()
		_mouse.station = avango.daemon.Station('device-mouse')
		_mouse.device = "/dev/input/by-id/" + _string
		_mouse.timeout = '14' # better !

		_mouse.values[0] = "EV_REL::REL_X"
		_mouse.values[1] = "EV_REL::REL_Y"

		_mouse.buttons[0] = "EV_KEY::BTN_LEFT"
		_mouse.buttons[1] = "EV_KEY::BTN_RIGHT"

		device_list.append(_mouse)
		print("Mouse started at:", _string)

	else:
		print("Mouse NOT found !")


device_list = []

#init_spacemouse()
init_new_spacemouse()
init_xbox_controller()
init_keyboard()
init_mouse()
init_lcd_wall_tracking()
init_dlp_wall_tracking()

avango.daemon.run(device_list)
