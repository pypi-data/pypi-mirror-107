#!/usr/bin/python
#
import json
import os
import sqlite3
from datetime import datetime

import requests
from tornado import web, ioloop, httpserver

from .configuration import PlotmanConfig, get_db_path


def PostDat(dp: dict, cfg: PlotmanConfig):
    # sending post request and saving response as response object
    payload = json.dumps(dp)
    requests.post(url=f'http://{cfg.apis.target}:{cfg.apis.port}/report', data=payload)


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


class MainHandler(web.RequestHandler):
    def prepare(self):
        if self.request.headers.get("Content-Type", "").startswith("application/json"):
            self.json_args = json.loads(self.request.body)
        else:
            self.json_args = None

    def post(self):
        self.set_header("Content-Type", "text/plain")
        req_body = self.json_args

        remote_addr = os.environ.get('REMOTE_ADDR', '-')
        ts = datetime.now().strftime('%m-%d %H:%M:%S')

        con = sqlite3.connect(get_db_path())
        cur = con.cursor()

        cur.execute('''CREATE TABLE IF NOT EXISTS systemchia (
                           tid text PRIMARY KEY,
                           block text NOT NULL,
                           ip text NOT NULL
                   );''')

        # Insert a row of data
        cur.execute(f"INSERT INTO systemchia VALUES ('{ts}','{req_body}','{remote_addr}')")
        con.commit()
        con.close()
        print(req_body)


def apiOpen(cfg: PlotmanConfig):
    print(f"api port {cfg.apis.port} is now listening")
    application = web.Application([(r"/report", MainHandler)])
    http_server = httpserver.HTTPServer(application)
    http_server.listen(cfg.apis.port)
    ioloop.IOLoop.current().start()
