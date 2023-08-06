#!/usr/bin/python
#

from datetime import datetime

import pkg_resources
import requests
from tornado import web, ioloop, httpserver

from .sql import SQLX
from ..configuration import PlotmanConfig, get_dash_v1, get_dash_v1_static

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


def start_master_api_node(cfg: PlotmanConfig):
    try:
        version = pkg_resources.get_distribution('plotmanx').version
        print(f"Now plotman API - v{version}")
        print(f"API running port {cfg.apis.port} is now listening.. ")

        settings = dict(
            debug=True,
            gzip=True,
            template_path=get_dash_v1(),
            static_path=get_dash_v1_static(),
        )

        appcli = web.Application([
            (r"/report", NodeHandle),
            (r"/nodes", DashSimpleListNodes),
            (r"/api/v1", ApiV1Review),
            (r"/monitor/(.*)", web.StaticFileHandler, dict(path=get_dash_v1(), default_filename="index.html"))
        ], **settings)

        print(f"Serve nuxt path {get_dash_v1()} and set default entry point as index.html")

        http_server = httpserver.HTTPServer(appcli)
        http_server.listen(cfg.apis.port)
        ioloop.IOLoop.current().start()

    except:
        print("Port is in use. Please close the daemon app and start again. ")
