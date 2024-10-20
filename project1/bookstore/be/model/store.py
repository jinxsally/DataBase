import logging
import os
import sqlite3 as sqlite
import threading

from pymongo import MongoClient
import pymongo


class Store:
    database: str

    def __init__(self):
        self.database = "mongodb://localhost:27017"  # 连接数据库
        self.init_tables()  # 初始化数据库

    def init_tables(self):
        try:
            db = self.get_db_conn()
            # 创建用户集合
            db.users.create_index([("user_id", pymongo.ASCENDING)], unique=True)

            # 创建用户商店集合
            db.user_store.create_index(
                [("user_id", pymongo.ASCENDING), ("store_id", pymongo.ASCENDING)],
                unique=True,
            )

            # 创建商店集合
            db.stores.create_index(
                [("store_id", pymongo.ASCENDING), ("book_id", pymongo.ASCENDING)],
                unique=True,
            )

            # 创建新订单集合
            db.new_orders.create_index([("order_id", pymongo.ASCENDING)], unique=True)

            # 创建新订单详情集合
            db.new_order_details.create_index(
                [("order_id", pymongo.ASCENDING), ("book_id", pymongo.ASCENDING)],
                unique=True,
            )
            print("connect to database")

        # 错误捕获
        except pymongo.errors.PyMongoError as e:
            logging.error(e)

    def get_db_conn(self):
        client = MongoClient(self.database)  # 替换为 MongoDB URI
        db = client["BookStore"]
        return db


database_instance: Store = None
# global variable for database sync
init_completed_event = threading.Event()


def init_database():
    global database_instance
    database_instance = Store()


def get_db_conn():
    global database_instance
    return database_instance.get_db_conn()
