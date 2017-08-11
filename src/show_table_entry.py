#!/usr/bin/env python

import argparse
from time import sleep
import os
import subprocess

_THIS_DIR = os.path.dirname(os.path.realpath(__file__))
_THRIFT_BASE_PORT = 22222

parser = argparse.ArgumentParser(description='P4 demo')
parser.add_argument('--swname', help='Switch Name',
                    type=str, action="store", required=True)
parser.add_argument('--table-name', help='Table Name',
                    type=str, action="store", required=True)
args = parser.parse_args()

def main():
    # Get Thrift Port
    sw_name = args.swname
    index = int(sw_name[1:])-1
    thrift_port = _THRIFT_BASE_PORT+index

    # Get Table Name
    table_name = args.table_name
    
    table_info_cmd = "echo 'table_dump %s' > ./cmd/table_dump.txt" % table_name
    os.system(table_info_cmd)
    cmd = "python ./simple_switch_CLI --thrift-port %d < ./cmd/table_dump.txt" % thrift_port
    os.system(cmd)
    os.system("rm -rf cmd/table_info.txt")

if __name__ == '__main__':
    main()
