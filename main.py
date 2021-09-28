import re
import interface


def write_config(name, token):
    name = 'TOKEN_' + name
    with open('config.py', 'a') as f:
        print("{} = '{}'".format(name, token), file=f)


def read_config():
    with open('config.py', 'r') as f:
        tokens = f.readlines()
    communities = {}
    for token in tokens:
        token_name, token_value = token.split(' = ')
        token_name = re.sub('TOKEN_', '', token_name)
        token_value = re.sub("[\n\']", '', token_value)
        communities[token_name] = token_value
    return communities


if __name__ == '__main__':
    interface.main_window()