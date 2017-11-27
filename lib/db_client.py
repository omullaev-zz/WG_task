import sqlite3


class DbClient:
    
    def __init__(self, db):
        self.conn = sqlite3.connect(db)
        self.conn.text_factory = str
        self.c = self.conn.cursor()
    
    def create_db(self, script):
        self.c.executescript(script)

    def delete_all(self, table):
        self.c.execute("DELETE FROM %s" % table)

    def select_all(self, table):
        self.c.execute("SELECT * FROM %s" % table)
        return self.c.fetchall()

    def select(self, table, column):
        self.c.execute("SELECT [{0}] FROM {1}".format(column, table))
        return self.c.fetchall()

    def select_condition(self, table, condition):
        self.c.execute("SELECT * FROM {0} WHERE {1}".format(table, condition))
        return self.c.fetchall()

    def insert(self, table, values):
        self.c.executemany("INSERT INTO {0} VALUES ({1})".format(table, ",".join(len(values[0])*"?".split())), values)

    def update(self, table, param, value, condition):
        self.c.execute("UPDATE {0} SET [{1}] = '{2}' WHERE {3}".format(table, param, value, condition))

    def close_connection(self):
        self.conn.commit()
        self.conn.close()
