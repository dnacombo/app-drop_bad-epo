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

# read config['events']
with open(config['events']) as f:
	todrop1 = f.read()
# turn todrop1 into a list of strings and remove leading and trailing whitespace or commas
todrop1 = todrop1.split(',')
# turn it to integers
# remove leading and trailing whitespace or commas in the list
todrop1 = [re.sub(r'^\s*|\s*$', '', x) for x in todrop1]
# remove empty strings
todrop1 = list(filter(None, todrop1))
todrop1 = [int(x) for x in todrop1]

# if config['drop'] is not None, read it and add to todrop
if config['drop'] is not None:
	todrop2 = config['drop'].split(',')
	todrop2 = [int(x) for x in todrop2]
else:
    todrop2 = []

# create union of todrop1 and todrop2
todrop = list(set(todrop1) | set(todrop2))

epochs.drop(todrop)
epochs.save(os.path.join('out_dir','meg.fif'), overwrite=True)
