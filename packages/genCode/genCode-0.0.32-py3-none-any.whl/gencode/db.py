import os

from db_hammer.mysql import MySQLConnection
from db_hammer.oracle import OracleConnection

from gencode.sqls import SQL


def DbConnect():
    from gencode.config import DB_CONF
    if os.environ.get('ORACLE_HOME', None) is None:
        os.environ["ORACLE_HOME"] = "/Users/liuzhuo/var/instantclient_19_8"
    c = DB_CONF.copy()
    del c["table_name"]
    del c["db_type"]
    if DB_CONF["db_type"].upper() == "MYSQL":
        return MySQLConnection(**c)
    elif DB_CONF["db_type"].upper() == "ORACLE":
        c["caps"] = "a"
        return OracleConnection(**c)
    else:
        raise Exception("数据库类型暂不支持，请联系作者")


def get_all_tables():
    from gencode.config import DB_CONF
    with DbConnect() as db:
        return db.select_dict_list(sql=SQL["TABLES"][DB_CONF["db_type"].upper()], params={
            "db_name": DB_CONF["db_name"]
        })


# 取表备注
def get_table_comment(table_name: str):
    from gencode.config import DB_CONF
    sql = """
        Select TABLE_COMMENT AS comment from INFORMATION_SCHEMA.TABLES 
        Where table_schema = '{}' and  table_name='{}'
        """.format(DB_CONF["db_name"], table_name)

    with DbConnect() as db:
        obj = db.select_value(sql=sql)
        return obj.replace("主表", "").replace("从表", "").replace("明细表", "").replace("关联表", "")


def get_columns_by_table(table):
    from gencode.config import DB_CONF
    with DbConnect() as db:
        ls = db.select_dict_list(sql=SQL["COLUMNS"][DB_CONF["db_type"].upper()], params={
            "db_name": DB_CONF["db_name"],
            "table_name": table
        })
        for l in ls:
            if l["comment"] == "" or l["comment"] is None:
                l["comment"] = l["column_name"]
            else:
                l["comment"] = l["comment"].replace("\n\t", " ").replace("\n", " ").replace("\r", " ")

        return ls
