import pymssql


class MSSQL:
    def __init__(self, host, username, password, db, timeout):
        self.host = host
        self.user = username
        self.pwd = password
        self.db = db
        self.timeout = timeout

    def __GetConnect(self):
        if not self.db:
            raise ConnectionError("请设置数据库信息")
        self.conn = pymssql.connect(host=self.host, user=self.user, password=self.pwd, database=self.db, charset="utf8", timeout=self.timeout)
        cur = self.conn.cursor()
        if not cur:
            raise ConnectionError("连接数据库失败")
        else:
            return cur

    def ExecQuery(self, sql):
        cur = self.__GetConnect()
        cur.execute(sql)
        resList = cur.fetchall()

        # 查询完毕后必须关闭连接
        self.conn.close()
        return resList

    def ExecNonQuery(self, sql):
        cur = self.__GetConnect()
        cur.execute(sql)
        self.conn.commit()
        self.conn.close()
