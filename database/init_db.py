import os, sys
import pymysql
import warnings
import copy
from . import config

DEFAULT_DB_DDL_PATH = os.path.realpath(os.path.join(os.path.dirname(__file__), "DB.sql")) # 默认CAREER的DDL语句文件路径

def init_DB(sql_path:str=DEFAULT_DB_DDL_PATH) -> bool:
    """
    初始化Career数据库. 默认的数据库DDL文件为career_platform/persistent/CAREER.sql.

    Params:
        sql_path: .sql文件路径, 内含用于初始化Career数据库的DDL语句.

    Returns:
        执行成功返回True,失败返回False.
    """

    # 获取数据库config
    db_config = copy.deepcopy(config.DB_config)
    if db_config.get("database", False):
        db_config.pop("database")

    # 获取DDL语句
    with open(sql_path, encoding='utf-8') as f:
        sqls = f.read().split(';')

    # 关闭pymysql的warning
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        
        try: 
            conn = pymysql.connect(**db_config)
            cursor = conn.cursor()
            for sql in sqls:
                sql = sql.strip()
                if sql!='':
                    cursor.execute(sql)
            conn.commit()
            conn.close()
        except Exception as E:
            print(E)
            print("execution failed!")
            return False
        else:
            print("execution success! NLQ database initialized!")
            return True