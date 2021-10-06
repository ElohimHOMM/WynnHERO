import pickle
import os.path
from pathlib import Path

data_file = Path('data/data.pkl')

def readyDataSetup():
    if os.path.exists(data_file) == False:
        open(data_file, 'wb+')
        sdata = {}
        save_dict(sdata)

def save_dict(dict):
    with open(data_file, 'wb') as f:
        pickle.dump(dict, f, pickle.HIGHEST_PROTOCOL) 

def load_dict():
    with open(data_file, 'rb') as f:
        return pickle.load(f)
