import copy
import os
import sys
import numpy as np
import pandas as pd
import subprocess as SP
import multiprocessing as MP
import torch
import MNSIM


class DLA(object):
    def __init__(self, hw_param_dicts, dataflow, maestro_run_path) -> None:
        super(DLA, self).__init__()
        self.hw_param_dicts = hw_param_dicts
        self.dataflow = dataflow
        self.maestro_run_path = maestro_run_path
        self.dla_dicts = self.set_dla()

    def set_dla(self):
        dla_dicts = {}
        dla_dicts['pes'] = self.hw_param_dicts['dla_pes']
        dla_dicts['glb_size'] = self.hw_param_dicts['glb_size']
        dla_dicts['l1_size'] = self.hw_param_dicts['dla_l1_size']
        dla_dicts['noc_bw'] = self.hw_param_dicts['dla_noc_bw']
        dla_dicts['offchip_bw'] = self.hw_param_dicts['offchip_bw']
        dla_dicts['dataflow'] = self.dataflow
        return dla_dicts


class RRAM(object):
    def __init__(self, hw_param_dicts, rram_config_path=os.path.dirname(__file__)) -> None:
        super(RRAM, self).__init__()
        self.hw_param_dicts = hw_param_dicts
        self.rram_config_path = rram_config_path
        self.rram_dicts = self.set_rram()
        self.mem_capacity = self.get_memory_capacity()  # bit

    def set_rram(self):
        rram_dicts = {}
        rram_dicts['tiles'] = self.hw_param_dicts['rram_tiles']
        rram_dicts['glb_size'] = self.hw_param_dicts['glb_size']
        rram_dicts['tile_bw'] = self.hw_param_dicts['rram_tile_bw']
        return rram_dicts

    def get_memory_capacity(self):
        return self.rram_dicts['tiles'] * 16 * 8 * 2 * 128**2
