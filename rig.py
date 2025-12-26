from subprocess import call
from my_types import Mode

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