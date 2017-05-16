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
parser.add_argument('--key', help='Match Key',
                    type=str, action="store", required=True)
parser.add_argument('--action', help='Action',
                    type=str, action="store", required=True)
parser.add_argument('--para-num', help='Number of Para',
                    type=int, action="store", required=False, default=0)
parser.add_argument('para', nargs='*', type=str)
args = parser.parse_args()

def main():
    # Get Thrift Port
    sw_name = args.swname
    index = int(sw_name[1:])-1
    thrift_port = _THRIFT_BASE_PORT+index

    # Get Table Name
    table_name = args.table_name
    
    # Get Match Key
    key = args.key

    # Get Action
    action = args.action

    # Get Number of Paras
    num = args.para_num

    paras = ''
    
    if num != 0 :
        para = args.para
        for i in range(num) :
            paras = paras+' '
            paras = paras+para[i]
        table_info_cmd = "echo 'table_add %s %s %s =>%s' > cmd/table_add.txt" % (table_name, key, action, paras)
    else :
        table_info_cmd = "echo 'table_add %s %s %s =>' > cmd/table_add.txt" % (table_name, key, action)

    #print(table_info_cmd)

    os.system(table_info_cmd)
    cmd = "./simple_switch_CLI --thrift-port %d < cmd/table_add.txt" % thrift_port
    os.system(cmd)
    os.system("rm -rf cmd/table_add.txt")

if __name__ == '__main__':
    main()