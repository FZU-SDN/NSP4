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
        table_info_cmd = "echo 'table_add %s %s %s =>%s' > cmd/table_add.txt" % (table_name, action, key, paras)
    else :
        table_info_cmd = "echo 'table_add %s %s %s =>' > cmd/table_add.txt" % (table_name, action, key)

    #print(table_info_cmd)

    os.system(table_info_cmd)
    cmd = "./simple_switch_CLI --thrift-port %d < cmd/table_add.txt" % thrift_port
    os.system("%s > handle_tmp.txt" % cmd)
    os.system("rm -rf cmd/table_add.txt")
    
    # Get Handle
    text = open('handle_tmp.txt', "r")
    for line in text.readlines():
        if line[0] == 'E':
            for i in range(len(line)):
                if line[i].isdigit():
                    break
            handle = line[i:-1]
            os.system("echo '%s' >> handle/%s_%s.txt" % (handle, sw_name, table_name)) 
    os.system("rm -rf handle_tmp.txt")        

if __name__ == '__main__':
    main()
