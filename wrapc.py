#!/usr/bin/env python3
import configparser
import os
import sys
import itertools
import argparse
import subprocess
import argcomplete
import functools
import shlex

def completercommand(command, prefix, parsed_args, **kwargs):
    env = os.environ.copy()
    del env["_ARGCOMPLETE"]
    outputs = subprocess.check_output(command.format(**vars(parsed_args)), shell=True, env=env)
    outputs = outputs.decode('utf8')
    outputs = outputs.split('\n')[:-1]
    return (output for output in outputs if output.startswith(prefix))

def main():
    wrapcrc = configparser.ConfigParser()
    wrapcrc.read(os.path.expanduser('~/.wrapcrc'))
    config = wrapcrc[os.path.basename(sys.argv[0])]

    parser = argparse.ArgumentParser()
    for i in itertools.count(start=0, step=1):
        complete = 'complete{}'.format(i)
        if complete in config:
            command = config[complete + "_command"]
            completer = functools.partial(completercommand, command)
            parser.add_argument(config[complete], help=config[complete]).completer = completer
        else:
            break

    argcomplete.autocomplete(parser)
    args, unknownargs = parser.parse_known_args()

    argsdict = vars(args)
    command = shlex.split(config["command"].format(**argsdict))

    os.system(config["pre_hook"].format(**argsdict))

    os.execvp(command[0], command + unknownargs)
