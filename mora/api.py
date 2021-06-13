import copy
import os
import sys
import numpy as np
import pandas as pd
import subprocess as SP
import multiprocessing as MP
import torch
import MNSIM


def EDP(DLA, RRAM, model, home_path):
    # return {'dla': DLA.get_edp(model), 'rram': RRAM.get_edp(model)}
    dla_output_csv_path = os.path.abspath(os.path.join(home_path, 'output/' + model + '/' + model + '-dla.csv'))
    rram_output_csv_path = os.path.abspath(os.path.join(home_path, 'output/' + model + '/' + model + '-rram.csv'))
    if os.path.exists(dla_output_csv_path) is not True or os.path.exists(dla_output_csv_path) is not True:
        print("api.read outfile conflict.")
        raise AttributeError
    dla_out = pd.read_csv(dla_output_csv_path)
    rram_out = pd.read_csv(rram_output_csv_path)
    dla_edp = float(dla_out.at[0, 'energy']) * float(dla_out.at[0, 'latency'])
    rram_edp = float(rram_out.at[0, 'energy']) * float(rram_out.at[0, 'latency'])
    return {'dla': dla_edp, 'rram': rram_edp}


def area(DLA, RRAM, model, home_path):
    dla_output_csv_path = os.path.abspath(os.path.join(home_path, 'output/' + model + '/' + model + '-dla.csv'))
    rram_output_csv_path = os.path.abspath(os.path.join(home_path, 'output/' + model + '/' + model + '-rram.csv'))
    if os.path.exists(dla_output_csv_path) is not True or os.path.exists(dla_output_csv_path) is not True:
        print("api.read outfile conflict.")
        raise AttributeError
    dla_out = pd.read_csv(dla_output_csv_path)
    rram_out = pd.read_csv(rram_output_csv_path)
    dla_area = float(dla_out.at[0, 'area'])
    rram_area = float(rram_out.at[0, 'area'])
    return {'dla': dla_area, 'rram': rram_area}
