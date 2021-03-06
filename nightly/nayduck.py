#!/usr/bin/env python

import argparse
import subprocess
import requests

import json

from colorama import Fore


parser = argparse.ArgumentParser(description='Run tests.')
parser.add_argument('--branch', '-b', dest='branch',
                    help='Branch to test. By default gets current one.' )
parser.add_argument('--sha', '-s', dest='sha',
                    help='Sha to test. By default gets current one.')
parser.add_argument('--test_file', '-t', dest='test_file', default='tests_for_nayduck.txt',
                    help='Test file with list of tests. By default nayduck.txt')

args = parser.parse_args()

def get_curent_sha():
    return subprocess.check_output(['git', 'rev-parse', 'HEAD'], universal_newlines=True)

def get_current_branch():
    return subprocess.check_output(['git', 'rev-parse', '--abbrev-ref', 'HEAD'], universal_newlines=True)

if __name__ == "__main__":
    if not args.branch:
        branch = get_current_branch().strip()
    else:
        branch = args.branch
    if not args.sha:
        sha = get_curent_sha().strip()
    else:
        sha = args.sha
    post = {'branch': branch, 'sha': sha, 'test_file': args.test_file}
    print('Sending request ...')
    res = requests.post('http://nayduck.eastus.cloudapp.azure.com:5000/request_a_run', json=post)
    json_res = json.loads(res.text)
    if json_res['code'] == 0:
        print(Fore.GREEN + json_res['response'])
    else:
        print(Fore.RED + json_res['response'])

    
