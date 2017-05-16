import os
import commands
import re
from webob.static import DirectoryApp

from ryu.app.wsgi import ControllerBase, WSGIApplication, route
from ryu.base import app_manager




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
            if kwargs['filename'] == "ok":
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

                print output
                # return output
                # status, output = commands.getstatusoutput('python /home/wpq/NSP4/src/show_sw_tables.py --swname=s1')


                # print output
                # matchObj = re.findall('(\S+)(?=[\s]*\[.*\])', output, re.M | re.I)

                # print matchObj

                # return matchObj[0]
            req.path_info = kwargs['filename']
        return self.static_app(req)



