import copy
import os
import sys
import numpy as np
import pandas as pd
import subprocess as SP
import multiprocessing as MP
import tensorflow as tf
from importlib import import_module


class DLA(object):
    def __init__(self, hw_param_dicts, dataflow, home_path) -> None:
        super(DLA, self).__init__()
        self.hw_param_dicts = hw_param_dicts
        self.dataflow = dataflow
        self.home_path = home_path
        self.dla_dicts = self.set_dla()

    def set_dla(self):
        dla_dicts = {}
        dla_dicts['pes'] = self.hw_param_dicts['dla_pes']
        dla_dicts['glb_size'] = self.hw_param_dicts['glb_size']
        # dla_dicts['l1_size'] = self.hw_param_dicts['dla_l1_size']
        dla_dicts['noc_bw'] = self.hw_param_dicts['dla_noc_bw']
        # dla_dicts['offchip_bw'] = self.hw_param_dicts['offchip_bw']
        dla_dicts['dataflow'] = self.dataflow
        return dla_dicts

    def invoke_maestro(self, model):
        output_csv_path = os.path.abspath(os.path.join(self.home_path, 'output/' + model + '/' + model + '-dla.csv'))
        mapping_path = os.path.abspath(os.path.join(self.home_path, 'model/' + model + '/' + model + '-dla_' + self.dataflow + '.m'))
        params = [self.dla_dicts['pes'], self.dla_dicts['glb_size'], self.dla_dicts['noc_bw'], mapping_path]
        # command = "./maestro --HW_file='{}' --Mapping_file='{}' --print_res=true --print_res_csv_file=true --print_log_file=false".format()
        command = "../maestro/maestro --num_pes={0[0]} --l2_size_cstr={0[1]} --noc_bw_cstr={0[2]} --Mapping_file='{0[3]}' --print_res=true --print_res_csv_file=true --print_log_file=false".format(
            *params)
        if os.path.exists(output_csv_path):
            print("dla outfile conflict.")
            raise AttributeError
        process = SP.Popen(command, stdout=SP.PIPE, stderr=SP.PIPE)
        stdout, stderr = process.communicate()
        process.wait()
        if os.path.exists(output_csv_path):
            print('maestro invoked', self.rram_dicts)
        else:
            print('maestro invoke fatal.')
            raise AttributeError
        return


class RRAM(object):
    def __init__(self, hw_param_dicts, home_path) -> None:
        super(RRAM, self).__init__()
        self.hw_param_dicts = hw_param_dicts
        self.rram_dicts = self.set_rram()
        self.mem_capacity = self.get_memory_capacity()
        self.home_path = home_path
        self.rram_config_path = os.path.abspath(os.path.join(home_path, "rram_config.ini"))

    def set_rram(self):
        rram_dicts = {}
        rram_dicts['tile_row'] = self.hw_param_dicts['rram_tile_size']
        rram_dicts['tile_col'] = self.hw_param_dicts['rram_tile_size']
        rram_dicts['glb_size'] = self.hw_param_dicts['glb_size']
        rram_dicts['tile_bw'] = self.hw_param_dicts['rram_tile_bw']
        return rram_dicts

    def get_memory_capacity(self):
        return self.rram_dicts['tile_row'] * self.rram_dicts['tile_col'] * 16 * 8 * 2 * 128**2  # bit

    def invoke_MNSIM(self, model):
        output_csv_path = os.path.abspath(os.path.join(self.home_path, 'output/' + model + '/' + model + '-rram.csv'))
        if os.path.exists(output_csv_path):
            print("rram outfile conflict.")
            raise AttributeError
        command = "python ../MNSIM.py -model {v1} -tile_size {v2} -tile_noc_bw {v3}".format(v1=model, v2=[self.rram_dicts['tile_row'], self.rram_dicts['tile_col']], v3=self.rram_dicts['tile_bw'])
        process = SP.Popen(command, stdout=SP.PIPE, stderr=SP.PIPE)
        stdout, stderr = process.communicate()
        process.wait()
        if os.path.exists(output_csv_path):
            print('MNSIM invoked', self.rram_dicts)
        else:
            print('MNSIM invoke fatal.')
            raise AttributeError


# TODO: change output format and location to /output/
