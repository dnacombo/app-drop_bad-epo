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

# read config['events'] only if events is a key in config
if 'events' not in config:
	todrop1 = []
else:
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
epochs.save(os.path.join('out_dir','meg-epo.fif'), overwrite=True)

# create string with rejected epochs
info = 'Dropped epochs: ' + str(todrop)
#Save the info into a info.txt file
with open(os.path.join('out_dir','info.txt'), 'w') as f:
    print(info, file=f)

# create a product.json file to show the output
dict_json_product = {'brainlife': []}

info = str(info)
dict_json_product['brainlife'].append({'type': 'info', 'msg': info})

with open('product.json', 'w') as outfile:
    json.dump(dict_json_product, outfile)
