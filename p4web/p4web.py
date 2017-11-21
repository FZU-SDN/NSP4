# -- coding: utf-8 --
import os
import commands
import re
from webob.static import DirectoryApp

from ryu.app.wsgi import ControllerBase, WSGIApplication, route
from ryu.base import app_manager
import json



PATH = os.path.dirname(__file__)


# Serving static files
class GUIServerApp(app_manager.RyuApp):
    _CONTEXTS = {
        'wsgi': WSGIApplication,
    }

    def __init__(self, *args, **kwargs):
        super(GUIServerApp, self).__init__(*args, **kwargs)

        wsgi = kwargs['wsgi']
        wsgi.register(GUI_P4_ServerController)

class GUI_P4_ServerController(ControllerBase):
    def __init__(self, req, link, data, **config):
        super(GUI_P4_ServerController, self).__init__(req, link, data, **config)
        path = "%s/P4_tools" % PATH
        self.static_app = DirectoryApp(path)

    @route('topology', '/{filename:.*}', methods=['GET'])
    def static_handler(self, req, **kwargs):
        if kwargs['filename']:
            print kwargs['filename']
            if kwargs['filename'] == "ok":

                # 用于创建拓扑文件
                switches = req.GET['switches']
                hosts = req.GET['hosts']

                switches = req.GET['switches']
                switches = switches.encode('utf-8')
                switches = int(switches)

                hosts = req.GET['hosts']
                hosts = hosts.encode('utf-8')
                hosts = int(hosts)

                linksnum = req.GET['linksnum']
                linksnum = linksnum.encode('utf-8')
                linksnum = int(linksnum)

                link_information = req.GET['link_information']
                link_information = link_information.encode('utf-8')

                #正则匹配得到对应的链路信息，从而写到topo.txt中去
                match_links = re.findall(r'(.*?),', link_information, re.M | re.I)
                links = match_links


                topo_file = open('topo.txt', 'w')
                topo_file.write('switches ' + str(switches) + '\n')
                topo_file.write('hosts ' + str(hosts) + '\n')
                for i in range(linksnum):
                    topo_file.write(links[i] + '\n')
                topo_file.close()

                print 'switches=%d' % switches
                print "hosts=%d" % hosts
                status, output = commands.getstatusoutput('cp -f topo.txt /home/wpq/NSP4/init')

            elif kwargs['filename'] == "table":
                #显示流表专用
                switch_no = req.GET['switch_no']
                switch_no = switch_no.encode('utf-8')

                #--------得到交换机内所有的【表名】（以------为该部分功能的结尾）

                cmd_str = 'python /home/wpq/NSP4/src/show_sw_tables.py --swname s' + switch_no
                status, output = commands.getstatusoutput(cmd_str)
                #正则匹配得到交换机内所有的【表名】
                matchObj = re.findall('(\S+)(?=[\s]*\[i.*\])', output, re.M | re.I)

                table_number = len(matchObj)
                # -----------得到交换机内所有的【表名】----------------#
                data_json = {}

                # print matchObj
                data_json['table-number'] = table_number
                table = []
                for i in range(table_number):
                    table_infor = {}
                    table_name = matchObj[i]
                    table_infor['table-name'] = table_name

                    #查询对应表的匹配项以及动作
                    cmd_str = 'python /home/wpq/NSP4/src/show_table_info.py --swname s' + switch_no + ' --table-name ' + table_name
                    status, output = commands.getstatusoutput(cmd_str)

                    #得到该表对应的匹配项
                    match_table_key = re.findall('[=\t](\S*)(?=\(.*\,.*\))', output, re.M | re.I)
                    #得到该表对应的动作
                    match_action_key = re.findall('[\n](\S+)(?=[\s]*\[(.*)\])', output, re.M | re.I)


                    match_key_num = len(match_table_key)
                    key = []
                    for j in range(match_key_num):
                        key.append(match_table_key[j])

                    table_infor['key-number'] = match_key_num
                    table_infor['key'] = key

                    match_action_num = len(match_action_key)
                    action = []
                    for j in range(match_action_num):
                        action.append(match_action_key[j][0])

                    table_infor['action-number'] = match_action_num
                    table_infor['action'] = action

                    #查询对应表，所对应的表项
                    cmd_str = 'python /home/wpq/NSP4/src/show_table_entry.py --swname s' + switch_no + ' --table-name ' + table_name
                    status, output = commands.getstatusoutput(cmd_str)

                    print output

                    #matchObj0 对应 表项 的 handle（唯一值)
                    matchObj0 = re.findall('(0x[\S]+)', output, re.M | re.I)

                    matchObj1 = re.findall('\*\s(\S+)(?=\s*:\s)', output, re.M | re.I)
                    matchObj2 = re.findall('[\s] (\S+)(?=\n)', output, re.M | re.I)
                    #matchObj3 对应的动作，以及动作参数
                    matchObj3 = re.findall('(\S+)\s- ?([\S ]*)', output, re.M | re.I)

                    table_entry = [
                    ]


                    for j in range(len(matchObj0)):
                        entry = {}
                        entry['handle'] = int(matchObj0[j], 16)
                        entry[matchObj1[j]] = matchObj2[j]
                        entry["action"] = matchObj3[j][0]
                        entry["action-parameter"] = matchObj3[j][1]
                        table_entry.append(entry)

                    table_infor['table-entry'] = table_entry
                    table_infor['table-entry-number'] = len(table_entry)
                    table.append(table_infor)

                data_json['table'] = table
                return json.dumps(data_json)

            elif kwargs['filename'] == 'add_entry':
                #添加表项

                switch_no = req.GET['switch-name']
                table_name = req.GET['table-name']
                action = req.GET['action']
                action_parameter = req.GET['action_parameter']

                switch_no = switch_no.encode('utf-8')
                switch_no = re.findall('([0-9]+)', switch_no, re.M | re.I)
                switch_no = switch_no[0]

                table_name = table_name.encode('utf-8')
                action = action.encode('utf-8')
                action_parameter = action_parameter.encode('utf-8')

                action_sum = action + ' ' + action_parameter

                cmd_str = 'python /home/wpq/NSP4/src/show_table_info.py --swname s' + switch_no + ' --table-name ' + table_name
                status, output = commands.getstatusoutput(cmd_str)

                match_table_key = re.findall('[=\t](\S*)(?=\(.*\,.*\))', output, re.M | re.I)

                match_key_num = len(match_table_key)

                key = []
                match_key_value = ''
                for j in range(match_key_num):
                    match_key_value += req.GET[match_table_key[j]].encode('utf-8') + ' '
                    key.append(match_table_key[j])

                print "match_key_value"
                print match_key_value
                cmd_str = 'python /home/wpq/NSP4/src/table_add_entry.py --swname s' + switch_no + ' --table-name ' + table_name + ' --key ' + match_key_value + '--action ' + action_sum
                status, output = commands.getstatusoutput(cmd_str)

                print cmd_str
                
                output = re.findall('(Error|Invalid)', output, re.M | re.I)

                if len(output) < 1:
                    return "add_entry success!"
                elif output[0] == 'Error':
                    return "input Error!"
                elif output[0] == 'Invalid':
                    return "input Invalid!"
                return json.dumps(output)

            elif kwargs['filename'] == 'del_entry':
                #删除表项
                handle = req.GET['handle'].encode('utf-8')
                table_name = req.GET['table-name'].encode('utf-8')
                switch_no = req.GET['switch-name'].encode('utf-8')

                switch_no = re.findall('([0-9]+)', switch_no, re.M | re.I)
                switch_no = switch_no[0]

                cmd_str = 'python /home/wpq/NSP4/src/table_delete_entry.py --swname s' + switch_no + ' --table-name ' + table_name + ' --handle ' + handle

                print cmd_str
                status, output = commands.getstatusoutput(cmd_str)

                return "delete success"

            req.path_info = kwargs['filename']
        return self.static_app(req)



