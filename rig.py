import subprocess
import time
import serial
from subprocess import call
from my_types import Mode, PD


def reset_rig():
    ser = serial.Serial('/dev/serial/by-id/usb-QRP_Labs_QMX_Transceiver-if00')
    try:
        if ser.is_open:
            hex_data = b'\x0A\x1B\x5B\x42\x0A\x0D\x11\x1B\x5B\x41\x0A\x0D' 
            ser.write(hex_data)
            time.sleep(0.1)
    finally:
        ser.close()

def set_rig_freq(freq):
    rig_model = 2057
    cmd = f"rigctl -m {rig_model} -s 9600 -r /dev/serial/by-id/usb-QRP_Labs_QMX_Transceiver-if00 F {freq}"
    call(cmd, shell=True)

def set_rig_TX():
    rig_model = 2057
    cmd = f"rigctl -m {rig_model} -s 9600 -r /dev/serial/by-id/usb-QRP_Labs_QMX_Transceiver-if00 T 1"
    call(cmd, shell=True)

def set_rig_RX():
    rig_model = 2057
    cmd = f"rigctl -m {rig_model} -s 9600 -r /dev/serial/by-id/usb-QRP_Labs_QMX_Transceiver-if00 T 0"
    call(cmd, shell=True)

def set_rig_mode(mode):
    rig_model = 2057
    cmd = f"rigctl -m 2057 -r /dev/serial/by-id/usb-QRP_Labs_QMX_Transceiver-if00 -s 9600 M {mode.name} 3200"
    call(cmd, shell=True)

def set_rig_pd(pd):
    rig_model = 2057
    cmd = f"rigctl -m 2057 -s 9600 -r /dev/serial/by-id/usb-QRP_Labs_QMX_Transceiver-if00 w \"MM3|13|0={pd.name};\""
    call(cmd, shell=True)
    reset_rig()

def get_rig_pd():
    rig_model = 2057
    cmd = f"/usr/bin/rigctl -m 2057 -s 9600 -r /dev/serial/by-id/usb-QRP_Labs_QMX_Transceiver-if00 w \"MM3|13|0;\""
    result = subprocess.run(cmd, stdout=subprocess.PIPE, shell=True)
    output = result.stdout.decode('utf-8').split(';')[0]
    a = PD.ON
    if output == "MMON":
        return PD.ON
    elif output == "MMOFF":
        return PD.OFF
    else:
        raise ValueError("Unknown PD state from rig") 


if __name__ == "__main__":
    set_rig_pd(PD.ON)
    pd = get_rig_pd()
    print(f"PD is {pd.name}")