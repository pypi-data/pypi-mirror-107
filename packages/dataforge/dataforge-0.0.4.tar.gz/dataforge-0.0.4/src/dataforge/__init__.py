import confuse
import os

config = confuse.Configuration('dataforge', __name__)
# Allow config.yaml at project root with highest priority
if os.path.isfile('config.yaml'):
    config.set_file('config.yaml')
