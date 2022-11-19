from typing import Tuple, List, Dict
import abc
import pymysql
from . import config
import time
import warnings

__all__ = ["MysqlDB"]


class MysqlDB():
    """
    对mysql驱动的普通封装.
    """
    def __init__(self, config:Dict=config.DB_config):
        self.config = config

    def __get_connection(self):
        while(True):
            try:
                conn = pymysql.connect(autocommit=False, **self.config)
            except Exception as E:
                print('Error connecting to database:{0}'.format(E))
                print('Reconnect in 3 sec...')
                time.sleep(3)
            else:
                break
        return conn
            
    def connect(self):
        return self.__get_connection()

    def query(self, sql:str, args:Tuple=None):
        conn = self.__get_connection()
        cursor = conn.cursor()

        aff_rows = cursor.execute(sql, args)
        res = cursor.fetchall()

        conn.commit()
        conn.close()

        return res

    def query_many(self, sql:str, args_list:List[Tuple]):
        conn = self.__get_connection()
        cursor = conn.cursor()

        aff_rows = cursor.executemany(sql, args_list)
        res = cursor

        conn.commit()
        conn.close()

        return res

    def execute(self, sql:str, args:Tuple=None):
        conn = self.__get_connection()
        cursor = conn.cursor()

        conn.begin()
        try:
            aff_rows = cursor.execute(sql, args)
        except Exception as e:
            conn.rollback()
            print("Database Error: {}".format(str(e)))
            print("Database execution canceled, database rollback completed.")
            aff_rows = None
        else:
            conn.commit()
        conn.close()
        return aff_rows

    def execute_many(self, sql:str, args_list:List[Tuple]):
        conn = self.__get_connection()
        cursor = conn.cursor()

        conn.begin()
        try:
            aff_rows = cursor.executemany(sql, args_list)
        except Exception as e:
            conn.rollback()
            print("Database Error: {}".format(str(e)))
            print("Database execution canceled, database rollback completed.")
            aff_rows = None
        else:
            conn.commit()
        conn.close()
        return aff_rows