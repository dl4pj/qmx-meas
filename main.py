import matplotlib.pyplot as plt
import rig
import measconfig
import tsutils
import shutil
import os

from tsapython import tinySA
from my_types import PD, Mode

vfo=[0]*11
vfo[0]= 1.850e6
vfo[1]= 3.550e6
vfo[2]= 5.3540e6
vfo[3]= 7.050e6
vfo[4]= 10.12e6
vfo[5]= 14.05e6
vfo[6]= 18.90e6
vfo[7]= 21.0e6
vfo[8]= 24.0e6
vfo[9]= 28.0e6
vfo[10]= 50.0e6

def meas(fvfo, mode, description):

    mc = measconfig.MeasConfig(fvfo, mode)

    tsa = tinySA()
    tsa.set_verbose(True)
    tsa.set_error_byte_return(True)
    connected = tsa.connect("/dev/serial/by-id/usb-tinysa.org_tinySA4_400-if00")

    if connected == False:
        print("ERROR: could not connect to port")
        quit()

    tsa.set_sweep_start(mc.fstart)
    tsa.set_sweep_stop(mc.fstop)

    tsa.marker_freq(1, mc.fl) 
    tsa.marker_freq(2, mc.fr) 
    tsa.marker_freq(3, mc.fipl)
    tsa.marker_freq(4, mc.fipr)

    tsa.repeat(1)
    data_bytes = tsa.scan(mc.fstart, mc.fstop, pts=450, outmask=2)
    m1 = tsutils.get_marker_value(tsa, 1)
    m2 = tsutils.get_marker_value(tsa, 2)
    m3 = tsutils.get_marker_value(tsa, 3)
    m4 = tsutils.get_marker_value(tsa, 4)

    tsa.resume() #resume so screen isn't still frozen
    tsa.disconnect()

    m1d = m3 - m1
    m2d = m4 - m2

    print(f"{fvfo}, {mode.name}, {pd.name}, {m1d:.2f}, {m2d:.2f}")
    with open("out/measurements.txt", "a") as f:
        f.write(f"{fvfo}, {mode.name}, {pd.name}, {m1d:.2f}, {m2d:.2f}\n")

    freq_arr, data_arr = tsutils.convert_data_to_arrays(mc.fstart, mc.fstop, 450, data_bytes)
    plt.clf()
    plt.plot(freq_arr, data_arr)
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Power (dBm)")
    plt.title("VFO: {} MHz".format(fvfo/1e3))
    #plt.text(4000,-125, "ip_links: {m2d} dBm\nip_rechts:{m1d} dBm")
    plt.savefig("out/meas_{}.png".format(description))
    plt.close

if __name__ == "__main__":

    shutil.rmtree("out")
    os.mkdir("out")
    for fvfo in vfo[3:5]:
        rig.set_rig_freq(fvfo)
        for mode in [Mode.USB, Mode.LSB]:
            rig.set_rig_mode(mode)
            for pd in [PD.ON, PD.OFF]:
                rig.set_rig_pd(pd)
                rig.set_rig_TX()
                description="{}_{}-{}.png".format(int(fvfo/1e3), mode.name, pd.name)
                meas(fvfo, mode, description)
                rig.set_rig_RX()
