import importlib
import os

profiles, templates, stage_templates = {}, {}, {}

# load assistants
file_path = os.path.dirname(os.path.realpath(__file__))
for name in os.listdir(file_path + '/module'):
    if os.path.isdir(file_path + '/module/' + name) and '__' not in name:
        importlib.import_module('folker.module.' + name)
