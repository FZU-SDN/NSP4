#!/usr/bin/env python

import re
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
parser.add_argument('--handle', help='Handle',
                    type=str, action="store", required=True)
#parser.add_argument('--ops-num', help='Operation Number',
#                    type=int, action="store", required=True)
args = parser.parse_args()

def main():
    # Get Thrift Port
    sw_name = args.swname
    index = int(sw_name[1:])-1
    thrift_port = _THRIFT_BASE_PORT+index

    # Get Table Name
    table_name = args.table_name

    # Get Handle
    table_handle = args.handle
    
    runtime_cmd = "table_delete %s %s" % (table_name, table_handle)
    os.system('echo %s > ./cmd/table_delete.txt' % runtime_cmd)
    os.system("python ./simple_switch_CLI --thrift-port %d < ./cmd/table_delete.txt" % thrift_port)
    os.system('rm -rf ./cmd/table_delete.txt')

    """
    # Get Operation Number
    number = args.ops_num

    handle_file = 'handle/%s_%s.txt' % (sw_name, table_name)
    # remove the entry
    i, text = 1, open(handle_file, "r")
    for line in text.readlines():
        if i != number :
            i = i+1
        else :
            table_handle = int(line)
            os.system("echo 'table_delete %s %s' > cmd/table_delete.txt" % (table_name, table_handle))
            os.system("./simple_switch_CLI --thrift-port %d < cmd/table_delete.txt" % (thrift_port))
            #os.system("rm -rf cmd/table_delete.txt")
            break
    """

if __name__ == '__main__':
    main()
