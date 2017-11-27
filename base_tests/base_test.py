import random

from lib.db_client import DbClient


def _rvalue():
    return random.randint(1, 100)


class WgBaseTest():
    def setup(self):
        self.wg_db_client = DbClient("wg.db")
        fd = open("create_db.sql", "r")
        script = fd.read()
        fd.close()
        self.wg_db_client.create_db(script)
        self._fill_db()

        self.memory_db = DbClient(":memory:")
        query = "".join(line for line in self.wg_db_client.conn.iterdump())
        self.memory_db.create_db(query)

    def teardown(self):
        self.memory_db.close_connection()
        self.wg_db_client.close_connection()

    def _fill_db(self):
        self.wg_db_client.delete_all("ships")
        self.wg_db_client.delete_all("weapons")
        self.wg_db_client.delete_all("hulls")
        self.wg_db_client.delete_all("engines")

        engines = [("engine-%s" % i, _rvalue(), _rvalue(), ) for i in xrange(1, 7)]
        weapons = [("weapon-%s" % i, _rvalue(), _rvalue(), _rvalue(), _rvalue(), _rvalue(), ) for i in xrange(1, 21)]
        hulls = [("hull-%s" % i, _rvalue(), _rvalue(), _rvalue(), ) for i in xrange(1, 6)]
        ships = [("ship-%s" % i, random.choice(weapons)[0], random.choice(hulls)[0],
                  random.choice(engines)[0], ) for i in xrange(1, 201)]

        self.wg_db_client.insert("engines", engines)
        self.wg_db_client.insert("weapons", weapons)
        self.wg_db_client.insert("hulls", hulls)
        self.wg_db_client.insert("ships", ships)
