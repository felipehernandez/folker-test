import sys


def is_debug():
    return 'debug' in sys.argv


def is_trace():
    return 'trace' in sys.argv


def capture_parameters_context():
    return {pair[0]: pair[1] for pair in [value[2:].split('=') for value in sys.argv if value.startswith('-c')]}
