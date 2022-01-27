import pickle
import os.path
from pathlib import Path

data_file = Path('data/data.pkl')


def ready_data_setup():
    if os.path.exists(data_file) is False:
        open(data_file, 'wb+')
        s_data = {}
        save_dict(s_data)


def save_dict(c_dict):
    with open(data_file, 'wb') as f:
        pickle.dump(c_dict, f, pickle.HIGHEST_PROTOCOL)


def load_dict():
    with open(data_file, 'rb') as f:
        return pickle.load(f)
