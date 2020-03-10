import getopt
import sys


def _resolve_command_option_key(command: str) -> str:
    return {
        '-d': 'debug', '--debug': 'debug',
        '-t': 'trace', '--trace': 'trace',
        '-l': 'LOG', '--log': 'LOG',
        '-c': 'context', '--context': 'context',
        '-f': 'file', '--file': 'files',
        '-F': 'file_re', '--FILE': 'file_re',
    }[command]


def _merge_parameter(key: str, old_value, new_value: str):
    if key in ['debug', 'trace', 'file', 'log', 'file_re']:
        return new_value
    if key in ['context']:
        merge = old_value if old_value else {}
        pair = new_value.split(':')
        merge[pair[0]] = pair[1]
        return merge


def usage():
    print('-d                         --debug                           debug')
    print('-t                         --trace                           trace')
    print('-lXXX.XX                   --log=XXX.XX                      log to file XXX.XX')
    print('-ckey:value                --context=key:value               add to context key=value')
    print('-ftest_file[,test_file]    --file=test_file[,test_file]      execute all tests whose file name are listed')
    print('-Ftest_file_re             --FILE=test_file_re               execute all tests whose file name match the regular expression')


command_options = {}


def load_command_arguments():
    if len(sys.argv) == 1:
        return
    try:
        opts, args = getopt.getopt(sys.argv[1:],
                                   'dtl:c:f:F:',
                                   ['debug', 'trace', 'log=', 'context=', 'file=', 'FILE='])
        for command_option in opts:
            key = _resolve_command_option_key(command_option[0])
            command_options[key] = _merge_parameter(key, command_options.get(key), command_option[1])
    except getopt.GetoptError as err:
        # print help information and exit:
        print(err)  # will print something like "option -a not recognized"
        usage()
        sys.exit(2)


def is_debug():
    return 'debug' in command_options or is_trace()


def is_trace():
    return 'trace' in command_options


def log_to_file():
    return command_options.get('log', None)


def capture_parameters_context():
    return command_options.get('context', {})


def test_file_regular_expression():
    return '**/{}'.format(command_options.get('file_re', 'folker_test*.yaml'))


def parameterised_test_files():
    files = command_options.get('file', None)
    if files is None:
        return []
    else:
        return files.split(',')
