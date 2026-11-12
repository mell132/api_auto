'''
此文件对数据库进行操作
'''
import pymysql

class Handle_db:
    def __init__(self,host, port, user, password, database, charset='utf8'):
        self.conn = pymysql.connect(
            host=host,
            port=int(port),
            user=user,
            password=password,
            database=database,
            charset=charset,
            autocommit=True,
            connect_timeout=5,
            cursorclass=pymysql.cursors.DictCursor,
        )

    def query_one(self, sql, args=None):
        with self.conn.cursor() as cur:
            cur.execute(sql, args or ())
            return cur.fetchone()

    def query_all(self, sql, args=None):
        with self.conn.cursor() as cur:
            cur.execute(sql, args or ())
            return cur.fetchall()

    def count(self, sql, args=None):
        """返回查询结果中的计数值。DictCursor 下 count(*) 是字典，不能直接当数字用。"""
        row = self.query_one(sql, args)
        if not row:
            return 0
        return int(next(iter(row.values())))

    def execute(self, sql, args=None):
        with self.conn.cursor() as cur:
            cur.execute(sql, args or ())
            return cur.rowcount

    def close(self):
        self.conn.close()


