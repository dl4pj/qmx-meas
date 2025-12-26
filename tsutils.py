import numpy as np

def get_marker_value(tsa, marker_num):
    cmd = f"marker {marker_num}"
    marker_bytes = tsa.command(cmd).decode('ascii')
    markers = [float(x) for x in marker_bytes.split()]
    return markers[3]  # return the dBm value

def convert_data_to_arrays(start, stop, pts, data):
    freq_arr = np.linspace(start, stop, pts)

    data1 =bytearray(data.replace(b"-:.0", b"-10.0"))
    data_arr = [float(line.split()[0]) for line in data1.decode('utf-8').split('\n') if line.strip()]
    return freq_arr, data_arr