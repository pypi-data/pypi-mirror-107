import sqlite3

from ..configuration import get_db_path


def commaInt(x: str) -> int:
    return int(x.replace(',', ''))


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
            ip,plotc,mvplotc,cpu_count,cpu_percent,cache_percent,slab_percent,
            swap_percent,disk_percent,iowait_percent,memory_percent,
            net_read_mb_s,net_write_mb_s,disk_read_mb_s,disk_write_mb_s,
            net_fds,version,stamp
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

    def getNodes(self) -> list:
        block = """
        SELECT * FROM sysio GROUP BY ip ORDER BY stamp DESC
        """

        list = self.cur.execute(block).fetchall()

        return list
