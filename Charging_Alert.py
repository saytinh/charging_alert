import time
import os
import click
import datetime
from pyicloud import PyiCloudService


print("Setup Time Zone")
time.strftime("%X %x %Z")
os.environ["TZ"] = "Asia/Ho_Chi_Minh"


print("Py iCloud Services")
api = PyiCloudService("duongtronghue@gmail.com", "86Vw9BcdT7wiQ5")

if api.requires_2fa:
    print("Two-factor authentication required. Your trusted devices are:")

    devices = api.trusted_devices
    for i, device in enumerate(devices):
        print(
            "  %s: %s"
            % (i, device.get("deviceName", "SMS to %s" % device.get("phoneNumber")))
        )

    device = click.prompt("Which device would you like to use?", default=0)
    device = devices[device]
    if not api.send_verification_code(device):
        print("Failed to send verification code")
        sys.exit(1)

    code = click.prompt("Please enter validation code")
    if not api.validate_verification_code(device, code):
        print("Failed to verify verification code")
        sys.exit(1)


maxBatLevel = 66

def batteryCheck():
    global currentBatLevel
    global lastBatLevel
    x = api.devices[1].status()
    currentBatLevel = round(x['batteryLevel']*100)
    if ((currentBatLevel == maxBatLevel) and (currentBatLevel > lastBatLevel)):
        api.devices[1].play_sound()
    lastBatLevel = currentBatLevel
    print("Current Level: " + str(currentBatLevel))

while(True):
    batteryCheck()
    time.sleep(5)
