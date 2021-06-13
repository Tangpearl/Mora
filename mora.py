'''
Mora dse
a greedy and singel model version
'''

import copy
import os
import sys
import argparse
from typing import Container
import numpy as np
import pandas as pd
import subprocess as SP
import multiprocessing as MP
import torch
import MNSIM
import mora

mora_layer_type_dicts = {0: "Linear", 1: "CONV", 2: "DWCONV", 3: "Residual", 4: "TRCONV", 5: "NGCONV"}  # DWCONV Residual is DSCONV on maestro
mora_layer_param_dicts = {
    'O': 'output_channel',
    'I': 'input_channel',
    'F': 'feature_size',
    'K': 'kernel_size',
    'S': 'stride',
    'T': 'layer_type',
    'R': 'relu_or_relu&pooling',
    'A': 'appending index'
}  # RP = 0:no relu, 1:relu, 2~:relu and pooling (kernel size), A = conv input index


def set_path():
    global home_path, rram_config_path, maestro_run_path, hw_config_path, model_path
    home_path = os.path.dirname(__file__)
    rram_config_path = os.path.abspath(os.path.join(home_path, "rram_config.ini"))
    maestro_run_path = os.path.abspath(os.path.join(home_path, "maestro_run.sh"))
    hw_config_path = os.path.abspath(os.path.join(home_path, "hw_config.m"))
    model_path = os.path.abspath(os.path.join(home_path, "model"))
    MNSIM_path = os.path.abspath(os.path.join(home_path, "MNSIM"))
    maestro_path = os.path.abspath(os.path.join(home_path, "maestro"))
    sys.path.append(home_path)
    sys.path.append(MNSIM_path)
    sys.path.append(maestro_path)


def set_parser():
    parser = argparse.ArgumentParser(description='mora dse parser')
    parser.add_argument('--dataflow', type=str, default='kcp')
    parser.add_argument('--model', type=str, default='vgg16')
    return parser


def hw_init(hw_config_path):
    hw_dicts = {}
    with open(hw_config_path, 'r') as fs:
        for lines in fs:
            try:
                params, values = lines.split(':')
                hw_dicts[params.strip()] = int(values.strip())
            except ValueError:
                print("check your config file.")
    return hw_dicts


if __name__ == "__main__":
    set_path()
    args = set_parser().parse_args()
    hw_param_dicts = hw_init(hw_config_path)
    model_csv_path = os.path.join(model_path, args.model + '.csv')
    model = pd.read_csv(model_csv_path).to_numpy()
    model_layer_num = model.shape[0]

    dla = mora.HW.DLA(hw_param_dicts, args.dataflow, maestro_run_path)
    rram = mora.HW.RRAM(hw_param_dicts, rram_config_path)
    edp_cons = mora.api.EDP(dla, rram, model, maestro_run_path)
    area_cons = mora.api.area(dla, rram, model, maestro_run_path)

    mora.schedule.greedy_schedule(DLA=dla, RRAM=rram, model=model, EDP_cons=edp_cons, area_cons=area_cons)
    # TODO:  mora.schedule.mora_schedule(DLA=dla, RRAM=rram, model=model, EDP_cons=edp_cons, area_cons=area_cons)
