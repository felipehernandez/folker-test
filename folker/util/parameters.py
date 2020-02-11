import getopt
import sys


def _resolve_command_option_key(command: str) -> str:
    return {
        '-d': 'debug', '--debug': 'debug',
        '-t': 'trace', '--trace': 'trace',
        '-f': 'file', '--file': 'file',
        '-c': 'context', '--context': 'context'
    }[command]


def _merge_parameter(key: str, old_value, new_value: str):
    if key in ['debug', 'trace', 'file']:
        return new_value
    if key in ['context']:
        merge = old_value if old_value else {}
        pair = new_value.split(':')
        merge[pair[0]] = pair[1]
        return merge


def usage():
    print('-d               --debug                 debug')
    print('-t               --trace                 trace')
    print('-fXXX.XX         --file=XXX.XX           log to file XXX.XX')
    print('-ckey:value      --context=key:value     add to context key=value')


command_options = {}


def load_command_arguments():
    try:
        opts, args = getopt.getopt(sys.argv[1:],
                                   'dtf:c:',
                                   ['debug', 'trace', 'file=', 'context='])
        for command_option in opts:
            key = _resolve_command_option_key(command_option[0])
            command_options[key] = _merge_parameter(key, command_options.get(key), command_option[1])
    except getopt.GetoptError as err:
        # print help information and exit:
        print(err)  # will print something like "option -a not recognized"
        usage()
        sys.exit(2)


def is_debug():
    return 'debug' in command_options


def is_trace():
    return 'trace' in command_options


def log_to_file():
    return command_options.get('file', None)


def capture_parameters_context():
    return command_options.get('context', {})
