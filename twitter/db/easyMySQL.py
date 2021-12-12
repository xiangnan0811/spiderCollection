import pymysql


class EasyMySQL:
    # 初始化
    def __init__(self, host, port, user, passwd, database):
        self.host = host
        self.port = port
        self.user = user
        self.passwd = passwd
        self.database = database

    # 连接数据库，需要传数据库地址、用户名、密码、数据库名称，默认设置了编码信息
    def connect(self):
        try:
            self.conn = pymysql.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.passwd,
                database=self.database,
                use_unicode=True,
                charset='utf8mb4',
            )
            self.cursor = self.conn.cursor()
        except Exception as e:
            return e

    # 关闭数据库连接
    def close(self):
        try:
            self.cursor.close()
            self.conn.close()
        except Exception as e:
            return e

    # 查询操作，查询单条数据
    def get_one(self, sql):
        # res = None
        try:
            self.connet()
            self.cursor.execute(sql)
            res = self.cursor.fetchone()
            self.close()
        except Exception:
            res = None
        return res

    # 查询操作，查询多条数据
    def get_all(self, sql):
        # res = ()
        try:
            self.connet()
            self.cursor.execute(sql)
            res = self.cursor.fetchall()
            self.close()
        except Exception:
            res = ()
        return res

    # 查询数据库对象
    def get_all_obj(self, sql, table_name, *args):
        res_list = []
        fields_list = []
        try:
            if len(args) > 0:
                for item in args:
                    fields_list.append(item)
            else:
                fields_sql = (
                    "select COLUMN_NAME from information_schema.COLUMNS where table_name = '%s' and table_schema = '%s'"
                    % (table_name, self.conn)
                )
                fields = self.get_all(fields_sql)
                for item in fields:
                    fields_list.append(item[0])

            # 执行查询数据sql
            res = self.get_all(sql)
            for item in res:
                obj = {}
                count = 0
                for x in item:
                    obj[fields_list[count]] = x
                    count += 1
                res_list.append(obj)
            return res_list
        except Exception as e:
            return e

    # 数据库插入、更新、删除操作
    def insert(self, sql):
        return self.__edit(sql)

    def update(self, sql):
        return self.__edit(sql)

    def delete(self, sql):
        return self.__edit(sql)

    def __edit(self, sql):
        # count = 0
        try:
            self.connect()
            count = self.cursor.execute(sql)
            self.conn.commit()
        except Exception as e:
            print(e)
            print('=' * 50)
            print(sql)
            print('=' * 50)
            self.conn.rollback()
            count = 0
            self.close()
        return count
