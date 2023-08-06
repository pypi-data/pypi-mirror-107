#!/usr/bin/python
#

from datetime import datetime
from os.path import isfile, join

import pkg_resources
import requests
from tornado import web, ioloop, httpserver
from tornado.template import Loader

from .sql import SQLX
from ..configuration import PlotmanConfig, get_dash_v1

__author__ = 'lousvicton'

try:
    import simplejson as json
except ImportError:
    import json


def PostDat(dp: dict, cfg: PlotmanConfig):
    # sending post request and saving response as response object
    payload = json.dumps(dp)
    requests.post(url=f'http://{cfg.apis.target}:{cfg.apis.port}/report', data=payload)


class ApiBase(web.RequestHandler):
    SUPPORTED_METHODS = ["GET"]

    def initialize(self, *args, **kwargs):
        self.version_plotman = pkg_resources.get_distribution('plotmanx').version
        self.remote_ip = self.request.headers.get('X-Forwarded-For', self.request.headers.get('X-Real-Ip', self.request.remote_ip))
        self.using_ssl = (self.request.headers.get('X-Scheme', 'http') == 'https')

    def set_default_headers(self):
        """Set the default response header to be JSON."""
        self.set_header("Content-Type", 'application/json; charset="utf-8"')

    def send_response(self, data, status=200):
        """Construct and send a JSON response with appropriate status code."""
        self.set_status(status)
        t = int(datetime.now().timestamp())
        response = {'result': 1, 'data': data, 'ts': t, 'ver': self.version_plotman}
        self.write(json.dumps(response))


"""

from prometheus_client.core import GaugeMetricFamily

class PlotmanCollector:
    def collect(self):
        cfg = configuration.get_validated_configs()
        jobs = Job.genTasks(cfg.directories.log)
        count = len(sorted(jobs, key=job.Job.get_time_wall))
        yield GaugeMetricFamily("plotman_jobs_count", "Number of plotting jobs running", value=count)

if __name__ == "__main__":
    start_http_server(8001)
    REGISTRY.register(PlotmanCollector())
    while True:
        time.sleep(1)
"""


class NodeHandle(web.RequestHandler):
    def initialize(self, *args, **kwargs):
        self.remote_ip = self.request.headers.get('X-Forwarded-For', self.request.headers.get('X-Real-Ip', self.request.remote_ip))
        self.using_ssl = (self.request.headers.get('X-Scheme', 'http') == 'https')

    def post(self):
        self.set_header("Content-Type", "text/plain")
        req_body = self.request.body
        sq = SQLX()
        sq.schema_plan()

        jpayload = dict()

        try:
            jpayload = json.loads(req_body)
        except:
            print("error from decoding json file.")
            return

        try:
            ip_remo = jpayload['identity']
        except:
            ip_remo = self.request.headers.get("X-Real-IP") or \
                      self.request.headers.get("X-Forwarded-For") or \
                      self.request.remote_ip

        tstime = datetime.now().strftime('%m-%d %H:%M:%S')

        if req_body is not None:
            sq.datainput(jpayload, ip_remo, tstime)

        sq.end()

        print("Report data ------")
        print(f"remote ip: {ip_remo} and ver. {jpayload['version']}")


class DashSimpleListNodes(ApiBase):

    def get(self):
        sq = SQLX()
        res = sq.getNodes()
        sq.end()
        # key = self.get_argument('key', None)
        self.send_response(res)


class ApiV1Review(ApiBase):

    def get(self):
        """List of routes for this API."""
        routes = {
            'info': 'GET /api/v1',
            'register': 'POST /api/v1/accounts',
            'single profile detail': 'GET /api/v1/accounts/<username>',
            'edit profile': 'PUT /api/v1/accounts/<username>',
            'delete profile': 'DELETE /api/v1/accounts/<username>',
            'login': 'POST /api/v1/accounts/login',
            'logout': 'GET /api/v1/accounts/logout',
            "user's tasks": 'GET /api/v1/accounts/<username>/tasks',
            "create task": 'POST /api/v1/accounts/<username>/tasks',
            "task detail": 'GET /api/v1/accounts/<username>/tasks/<id>',
            "task update": 'PUT /api/v1/accounts/<username>/tasks/<id>',
            "delete task": 'DELETE /api/v1/accounts/<username>/tasks/<id>'
        }
        self.write(json.dumps(routes))


"""class FrontEndLoad(web.RequestHandler):
    def initialize(self, *args, **kwargs):
        self.ver = pkg_resources.get_distribution('plotmanx').version
        self.remote_ip = self.request.headers.get('X-Forwarded-For', self.request.headers.get('X-Real-Ip', self.request.remote_ip))
        self.using_ssl = (self.request.headers.get('X-Scheme', 'http') == 'https')

    def get(self):
        # self.set_header("Content-Type", "text/plain")
        self.render("index.html", messages=None, version=self.ver)

"""


class WebpHandler(web.StaticFileHandler):
    def write_error(self, status_code, **kwargs):

        if status_code in (404, 500):
            error_page = '{}.html'.format(status_code)
            if isfile(join(get_dash_v1(), error_page)):
                self.write(Loader(get_dash_v1()).load(error_page).generate())
            else:
                super().write_error(status_code, **kwargs)


# Reset
Color_Off = '\033[0m'  # Text Reset

# Regular Colors
Black = '\033[0;30m'  # Black
Red = '\033[0;31m'  # Red
Green = '\033[0;32m'  # Green
Yellow = '\033[0;33m'  # Yellow
Blue = '\033[0;34m'  # Blue
Purple = '\033[0;35m'  # Purple
Cyan = '\033[0;36m'  # Cyan
White = '\033[0;37m'  # White

# Bold
BBlack = '\033[1;30m'  # Black
BRed = '\033[1;31m'  # Red
BGreen = '\033[1;32m'  # Green
BYellow = '\033[1;33m'  # Yellow
BBlue = '\033[1;34m'  # Blue
BPurple = '\033[1;35m'  # Purple
BCyan = '\033[1;36m'  # Cyan
BWhite = '\033[1;37m'  # White

# Underline
UBlack = '\033[4;30m'  # Black
URed = '\033[4;31m'  # Red
UGreen = '\033[4;32m'  # Green
UYellow = '\033[4;33m'  # Yellow
UBlue = '\033[4;34m'  # Blue
UPurple = '\033[4;35m'  # Purple
UCyan = '\033[4;36m'  # Cyan
UWhite = '\033[4;37m'  # White

# Background
On_Black = '\033[40m'  # Black
On_Red = '\033[41m'  # Red
On_Green = '\033[42m'  # Green
On_Yellow = '\033[43m'  # Yellow
On_Blue = '\033[44m'  # Blue
On_Purple = '\033[45m'  # Purple
On_Cyan = '\033[46m'  # Cyan
On_White = '\033[47m'  # White

# High Intensity
IBlack = '\033[0;90m'  # Black
IRed = '\033[0;91m'  # Red
IGreen = '\033[0;92m'  # Green
IYellow = '\033[0;93m'  # Yellow
IBlue = '\033[0;94m'  # Blue
IPurple = '\033[0;95m'  # Purple
ICyan = '\033[0;96m'  # Cyan
IWhite = '\033[0;97m'  # White

# Bold High Intensity
BIBlack = '\033[1;90m'  # Black
BIRed = '\033[1;91m'  # Red
BIGreen = '\033[1;92m'  # Green
BIYellow = '\033[1;93m'  # Yellow
BIBlue = '\033[1;94m'  # Blue
BIPurple = '\033[1;95m'  # Purple
BICyan = '\033[1;96m'  # Cyan
BIWhite = '\033[1;97m'  # White

# High Intensity backgrounds
On_IBlack = '\033[0;100m'  # Black
On_IRed = '\033[0;101m'  # Red
On_IGreen = '\033[0;102m'  # Green
On_IYellow = '\033[0;103m'  # Yellow
On_IBlue = '\033[0;104m'  # Blue
On_IPurple = '\033[0;105m'  # Purple
On_ICyan = '\033[0;106m'  # Cyan
On_IWhite = '\033[0;107m'  # White


def start_master_api_node(cfg: PlotmanConfig):
    try:
        version = pkg_resources.get_distribution('plotmanx').version
        print(f"Now plotman API - v{version}")
        print(f"API running port {cfg.apis.port} is now listening.. ")

        settings = dict(
            debug=True,
            gzip=True
        )

        """
      template_path=get_dash_v1(),
            static_path=get_dash_v1_static(),
            """
        static_handler_args = dict(
            path=get_dash_v1(),
            default_filename="index.html"
        )

        appcli = web.Application([
            (r"/report", NodeHandle),
            (r"/api/v1/nodes", DashSimpleListNodes),
            (r"/api/v1", ApiV1Review),
            (r"/monitors/(.*)", WebpHandler, static_handler_args)
        ], **settings)

        print(f"Serve nuxt path {get_dash_v1()} and set default entry point as index.html")
        print(f"Running at:{BCyan} http://{'127.0.0.1'}:{cfg.apis.port}/ {Color_Off}")
        http_server = httpserver.HTTPServer(appcli)
        http_server.listen(cfg.apis.port)
        ioloop.IOLoop.current().start()

    except OSError:
        print(f"{BRed}Port is in use.{Color_Off} Please close the daemon app and start again. ")
    except KeyboardInterrupt:
        print('Stopping server...')
