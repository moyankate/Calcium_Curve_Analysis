import numpy as np
import pandas as pd
from scipy.interpolate import interp1d


def load_traces(data_file, ttl_file=None):
    data = pd.read_csv(data_file)

    if ttl_file:
        ttls = pd.read_csv(ttl_file, header=None, names=["Timestamp", "Value"])


        ttls_rising = ttls[ttls["Value"]==True]
        event_ts = event_ids(ttls_rising["Timestamp"].values)

        for event_name in event_ts:
            event_ts[event_name] = event_ts[event_name] - data["Timestamp"][0]

    data["Timestamp"] = data["Timestamp"] - data["Timestamp"][0]

    traces = deinterleave(data)

    if ttl_file:
        return traces, event_ts
    else:
        return traces


def event_ids(ttl_ts, ttl_window=1.2, ttl_codes={"start":10, "shock":1, "tone":2, "pips":3}):
    event_ts = {}
    for event_name in ttl_codes:
        event_ts[event_name] = []

    for ts in ttl_ts:
        if not np.any((ttl_ts < ts) & (ttl_ts > ts-ttl_window)):
            n_pulses = np.sum((ttl_ts >= ts) & (ttl_ts < ts+ttl_window))
            
            for event_name in ttl_codes:
                if n_pulses == ttl_codes[event_name]:
                    event_ts[event_name].append(ts)
    return event_ts


def scale(trace):
    return (trace - trace.mean())/trace.std()


### wrtn's help

def deinterleave(data):
    traces = {}
    regions = [x for x in data.columns if "Region" in x]
    channels = data["LedState"].unique()
    channels = channels[channels < 5]  # LedState가 5 미만인 경우만 처리
    ts = data["Timestamp"]

    for reg in regions:
        traces["ts"] = ts
        traces[reg] = {}
        data_reg = data[["Timestamp", "LedState", reg]]
        
        for chan in channels:
            data_chan = data_reg[data_reg["LedState"] == chan]
            if len(data_chan) > 1:  # 데이터 포인트가 2개 이상인 경우에만 보간 함수 적용
                f = interp1d(data_chan["Timestamp"], data_chan[reg], fill_value="extrapolate")
                traces[reg]["state" + str(chan)] = f(ts)
            else:
                print(f"Warning: Not enough data points for LedState {chan} in {reg}. Skipping interpolation.")
                traces[reg]["state" + str(chan)] = np.nan  # 데이터가 충분하지 않은 경우 NaN 할당

    return traces


def deinterleave_LA(data):
    traces = {}
    violet = data[data["LedState"]==1]
    green = data[data["LedState"]==2]
    red = data[data["LedState"]==4]

    f = interp1d(violet["Timestamp"], violet["Region0G"], fill_value="extrapolate")
    traces["lar_violet"] = f(data["Timestamp"])
    f = interp1d(green["Timestamp"], green["Region0G"], fill_value="extrapolate")
    traces["lar_green"] = f(data["Timestamp"])
    f = interp1d(red["Timestamp"], red["Region1R"], fill_value="extrapolate")
    traces["lar_red"] = f(data["Timestamp"])
    traces["lar_gcamp"] = (traces["lar_green"] - traces["lar_violet"]) / traces["lar_violet"]
    traces["lar_rgeco"] = (traces["lar_red"] - traces["lar_violet"]) / traces["lar_violet"]

    f = interp1d(violet["Timestamp"], violet["Region2G"], fill_value="extrapolate")
    traces["acc_violet"] = f(data["Timestamp"])
    f = interp1d(green["Timestamp"], green["Region2G"], fill_value="extrapolate")
    traces["acc_green"] = f(data["Timestamp"])
    f = interp1d(red["Timestamp"], red["Region3R"], fill_value="extrapolate")
    traces["acc_red"] = f(data["Timestamp"])
    traces["acc_gcamp"] = (traces["acc_green"] - traces["acc_violet"]) / traces["acc_violet"]
    traces["acc_rgeco"] = (traces["acc_red"] - traces["acc_violet"]) / traces["acc_violet"]

    f = interp1d(violet["Timestamp"], violet["Region4G"], fill_value="extrapolate")
    traces["lal_violet"] = f(data["Timestamp"])
    f = interp1d(green["Timestamp"], green["Region4G"], fill_value="extrapolate")
    traces["lal_green"] = f(data["Timestamp"])
    f = interp1d(red["Timestamp"], red["Region5R"], fill_value="extrapolate")
    traces["lal_red"] = f(data["Timestamp"])
    traces["lal_gcamp"] = (traces["lal_green"] - traces["lal_violet"]) / traces["lal_violet"]
    traces["lal_rgeco"] = (traces["lal_red"] - traces["lal_violet"]) / traces["lal_violet"]
    
    traces["Timestamp"] = data["Timestamp"].copy()
    return traces