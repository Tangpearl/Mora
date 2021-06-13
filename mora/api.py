import copy
import os
import sys
import numpy as np
import pandas as pd
import subprocess as SP
import multiprocessing as MP
import torch
import MNSIM


def EDP(DLA, RRAM, model, maestro_run_path):
    return {'dla': invoke_maestro(DLA, model, maestro_run_path).get_edp(), 'rram': invoke_MNSIM(RRAM, model).get_edp()}


def area(DLA, RRAM, model, maestro_run_path):
    return {'dla': invoke_maestro(DLA, model).get_area(), 'rram': invoke_MNSIM(RRAM, model).get_area()}


class invoke_maestro(object):
    def __init__(self, DLA, model, maestro_run_path) -> None:
        super(invoke_maestro, self).__init__()


class invoke_MNSIM(object):
    def __init__(self, DLA, model, maestro_run_path) -> None:
        super(invoke_MNSIM, self).__init__()
