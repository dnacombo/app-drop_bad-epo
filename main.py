# Copyright (c) 2020 brainlife.io
#
# This app drops bad epochs by index in a MNE/epochs file.

# set up environment
import os
import json
import numpy as np
import mne
import helper
import re


# load inputs from config.json
with open('config.json') as config_json:
	config =  helper.convert_parameters_to_None(json.load(config_json))

data_file = config['mne']

epochs = mne.read_epochs(data_file,verbose=False)

epochs.drop(config['drop'])

epochs.save(os.path.join('out_dir','meg.fif'))
