import mne 
import pandas as pd 
import wfdb

import argparse
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument("file_path", type=Path)
p = parser.parse_args()


file = str(p.file_path)

subs = file.split('/')
file_name = subs[len(subs)-1]
file_name= file_name.replace(".edf", "")

data = mne.io.read_raw_edf(file)
raw_data = data.get_data()

info = data.info
channels = data.ch_names

edf_dataframe = pd.DataFrame(raw_data)

edf_data = edf_dataframe.T

fmtx=[]
adc_gainx=[]
baselinex=[]
unitsx=[]

for i in range(len(channels)):
  fmtx.append('16')
  adc_gainx.append(0)
  baselinex.append(0)
  unitsx.append('mV')

numArr = edf_data.to_numpy()
wfdb.wrsamp(file_name, fs=250, units=unitsx, sig_name=channels, p_signal=numArr, fmt=fmtx)
