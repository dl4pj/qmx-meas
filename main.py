import matplotlib.pyplot as plt
import rig
import measconfig
import tsutils
import shutil
import os

from tsapython import tinySA
from my_types import PD, Mode

#QMX+
vfo =[1.850e6, 3.550e6, 5.3540e6, 7.050e6, 10.12e6, 14.05e6, 18.090e6, 21.0e6, 24.95e6, 27.0e6, 28.0e6, 50.09e6]
#QMX80
#vfo =[3.550e6, 5.3540e6, 7.050e6, 10.12e6, 14.05e6]
#QMX20extended
#vfo = [14.05e6, 18.090e6, 21.0e6, 24.95e6, 27.0e6, 28.0e6, 50.09e6]

def meas(fvfo, mode):
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

    tsa.repeat(4)
    data_bytes = tsa.scan(mc.fstart, mc.fstop, pts=450, outmask=2)
    m=[0]*4
    for i in range(4):
        m[i] = tsutils.get_marker_value(tsa, i+1)
    tsa.resume()
    tsa.disconnect()

    freq_arr, data_arr = tsutils.convert_data_to_arrays(mc.fstart, mc.fstop, 450, data_bytes)
    return freq_arr, data_arr, m

if __name__ == "__main__":

    if os.path.exists("out"):
        shutil.rmtree("out")
    os.mkdir("out")
    for fvfo in vfo:
        rig.set_rig_freq(fvfo)
        for mode in [Mode.USB, Mode.LSB]:
            plt.clf()
            rig.set_rig_mode(mode)
            for pd in [PD.OFF, PD.ON]:
            #if True:
                rig.set_rig_pd(pd)
                pd = rig.get_rig_pd()
                rig.set_rig_TX()
                description="{}_{}-{}.png".format(int(fvfo/1e3), mode.name, pd.name)
                freq_arr, data_arr, m = meas(fvfo, mode)
                rig.set_rig_RX()
                plt.plot(freq_arr, data_arr)

                m1d = m[2] - m[0]
                m2d = m[3] - m[1]
                print(f"{fvfo}, {mode.name}, {pd.name}, {m1d:.2f}, {m2d:.2f}")
                with open("out/measurements.txt", "a") as f:
                    f.write(f"{fvfo}, {mode.name}, {pd.name}, {m1d:.2f}, {m2d:.2f}\n")

            plt.xlabel("Frequency (Hz)")
            plt.ylabel("Power (dBm)")
            plt.title(f"{fvfo/1e6} MHz {mode.name}")
            plt.legend(["PD OFF", "PD ON"])
            plt.grid()
            plt.savefig(f"out/meas_{fvfo/1e6}_{mode.name}.png")
            plt.close()
