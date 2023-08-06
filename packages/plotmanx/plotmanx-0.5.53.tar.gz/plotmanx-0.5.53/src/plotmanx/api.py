#!/usr/bin/python
#

import sqlite3
from datetime import datetime

import pkg_resources
import requests
from tornado import web, ioloop, httpserver

from .configuration import PlotmanConfig, get_db_path

try:
    import simplejson as json
except ImportError:
    import json


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


class SQLX:
    def __init__(self):
        self.con = sqlite3.connect(get_db_path())
        self.cur = self.con.cursor()

    def end(self):
        self.con.commit()
        self.con.close()

    def schema_plan(self):
        self.cur.execute('''CREATE TABLE IF NOT EXISTS systemchia (
                           tid text PRIMARY KEY,
                           block text NOT NULL,
                           ip text NOT NULL
                   );''')

        self.cur.execute('''CREATE TABLE IF NOT EXISTS sysio (
                                   tid INTEGER PRIMARY KEY AUTOINCREMENT,
                                   ip text NOT NULL,
                                   plotc INTEGER NOT NULL,
                                   mvplotc INTEGER NOT NULL,
                                   cpu_count INTEGER NOT NULL,
                                   cpu_percent REAL NOT NULL,
                                   cache_percent REAL NOT NULL,
                                   slab_percent REAL NOT NULL,
                                   swap_percent REAL NOT NULL,
                                   disk_percent REAL NOT NULL,
                                   iowait_percent REAL NOT NULL,
                                   memory_percent REAL NOT NULL,
                                   net_read_mb_s INTEGER NOT NULL,
                                   net_write_mb_s INTEGER NOT NULL,
                                   disk_read_mb_s INTEGER NOT NULL,
                                   disk_write_mb_s INTEGER NOT NULL,

                                   net_fds INTEGER NOT NULL,
                                   version text NOT NULL,
                                   stamp INTEGER NOT NULL

                           );''')

        self.cur.execute('''CREATE TABLE IF NOT EXISTS plot (
                           pcid INTEGER PRIMARY KEY AUTOINCREMENT,
                           plotid text NOT NULL,
                           k INTEGER NOT NULL,
                           r INTEGER NOT NULL,
                           b INTEGER NOT NULL,
                           u INTEGER NOT NULL,
                           pid INTEGER NOT NULL,
                           ip text NOT NULL,
                           time text NOT NULL
                   );''')

    def datainput(self, j: dict, ipremo: str, ts: str) -> None:

        if len(j['jobls']) > 0:

            try:
                for h in j['jobls']:

                    plotid = h['plot_id']

                    #                        if len(plotid) > 8:
                    #                            plotid = h['plot_id'][:8]

                    content_find = f"""

                    SELECT COUNT(*) FROM plot WHERE plotid='{plotid}';
                    """

                    (n,) = self.cur.execute(content_find).fetchone()
                    if int(n) == 0:
                        content_insert = f"""
                            INSERT INTO plot (plotid, k, r, b, u, pid, ip, time)
                            VALUES (
                            '{plotid}', {int(h['k'])}, {int(h['r'])}, {int(h['b'])},
                            {int(h['u'])}, {int(h['pid'])}, '{ipremo}', '{ts}'
                            )
                           ;
                        """

                        self.cur.execute(content_insert)

                        print(f"ID - {plotid}")
                    else:
                        content_update = f"""
                        UPDATE plot 
                        SET time='{ts}'
                        WHERE plotid='{plotid}'
                        ;
                        """
                        self.cur.execute(content_update)

            except sqlite3.OperationalError as r:
                print(f"there is a things that doesnt work. {r}")
        else:
            print("body is not empty")

        content_insert = f"""
        INSERT INTO sysio (
        ip,plotc,mvplotc,
        cpu_count,cpu_percent,cache_percent,slab_percent,swap_percent,disk_percent,iowait_percent,memory_percent,
        net_read_mb_s,net_write_mb_s,disk_read_mb_s,disk_write_mb_s,net_fds,version,stamp
        ) VALUES(
        '{ipremo}',
        {int(j['plotcount'])},
        {int(j['movingcount'])},
        {int(j['cpucount'])},
        {float(j['cpu_percent'])},
        {float(j['cache_percent'])},
        {float(j['slab_percent'])},
        {float(j['swap_percent'])},
        {float(j['disk_percent'])},
        {float(j['iowait_percent'])},
        {float(j['memory_percent'])},
        {commaInt(j['net_read_mb_s'])},
        {commaInt(j['net_write_mb_s'])},
        {commaInt(j['disk_read_mb_s'])},
        {commaInt(j['disk_write_mb_s'])},
        {commaInt(j['net_fds'])},
        '{j['version']}',
        {int(j['stamp'])}
        )
        """

        self.cur.execute(content_insert)


class NodeHandle(web.RequestHandler):
    def initialize(self, *args, **kwargs):
        self.remote_ip = self.request.headers.get('X-Forwarded-For', self.request.headers.get('X-Real-Ip', self.request.remote_ip))
        self.using_ssl = (self.request.headers.get('X-Scheme', 'http') == 'https')

    def post(self):
        self.set_header("Content-Type", "text/plain")
        req_body = self.request.body
        sq = SQLX()
        sq.schema_plan()

        remote_ip = self.request.headers.get("X-Real-IP") or \
                    self.request.headers.get("X-Forwarded-For") or \
                    self.request.remote_ip

        jpayload = dict()

        try:
            jpayload = json.loads(req_body)
        except:
            print("error from decoding json file.")
            return

        try:
            ip_remo = jpayload['identity']
        except:
            ip_remo = remote_ip

        tstime = datetime.now().strftime('%m-%d %H:%M:%S')

        if req_body is not None:
            sq.datainput(jpayload, ip_remo, tstime)

        sq.end()

        print("Report data ------")
        print(f"remote ip: {ip_remo} and ver. {jpayload['version']}")


def commaInt(x: str) -> int:
    return int(x.replace(',', ''))


def start_master_api_node(cfg: PlotmanConfig):
    try:
        version = pkg_resources.get_distribution('plotmanx').version
        print(f"Now plotman API - v{version}")
        print(f"API running port {cfg.apis.port} is now listening.. ")
        application = web.Application([(r"/report", NodeHandle)])
        http_server = httpserver.HTTPServer(application)
        http_server.listen(cfg.apis.port)
        ioloop.IOLoop.current().start()
    except:
        print("Port is in use. Please close the daemon app and start again. ")
