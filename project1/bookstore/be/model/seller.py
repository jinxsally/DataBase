from pymongo import errors
from be.model import error
from be.model import db_conn
import json


class Seller(db_conn.DBConn):
    def __init__(self):
        db_conn.DBConn.__init__(self)

    # 添加书籍
    def add_book(
        self,
        user_id: str,
        store_id: str,
        book_id: str,
        book_json_str: str,
        stock_level: int,
    ):
        try:
            if not self.user_id_exist(user_id):
                # debug
                print(1)
                return error.error_non_exist_user_id(user_id)
            if not self.store_id_exist(store_id):
                # debug
                print(2)
                return error.error_non_exist_store_id(store_id)
            if self.book_id_exist(store_id, book_id):
                # debug
                print(3)
                return error.error_exist_book_id(book_id)

            # 整合书籍信息成子文档
            stock_level = int(stock_level)
            book_info = json.loads(book_json_str)  # 需要解析一次
            book = {
                "book_id": book_id,
                "book_info": book_info,
                "stock_level": stock_level,
            }

            # 整合成需要插入的文档
            new = {
                "store_id": store_id,
                "books": book,
            }
            self.conn.stores.insert_one(new)
        except errors.PyMongoError as e:
            # debug
            print(e)
            return 528, "{}".format(str(e))
        except BaseException as e:
            # debug
            print(e)
            return 530, "{}".format(str(e))
        return 200, "ok"

    # 增加库存
    def add_stock_level(
        self, user_id: str, store_id: str, book_id: str, add_stock_level: int
    ):
        try:
            if not self.user_id_exist(user_id):
                return error.error_non_exist_user_id(user_id)
            if not self.store_id_exist(store_id):
                return error.error_non_exist_store_id(store_id)
            if not self.book_id_exist(store_id, book_id):
                return error.error_non_exist_book_id(book_id)

            query = {
                "store_id": store_id,
                "books.book_id": book_id,
            }
            update_stock = {
                "$inc": {"books.stock_level": add_stock_level},
            }
            self.conn.stores.update_one(query, update_stock)

        except errors.PyMongoError as e:
            # debug
            print(e)
            return 528, "{}".format(str(e))
        except BaseException as e:
            # debug
            print(e)
            return 530, "{}".format(str(e))
        return 200, "ok"

    # 创建店铺
    def create_store(self, user_id: str, store_id: str) -> (int, str):
        try:
            if not self.user_id_exist(user_id):
                return error.error_non_exist_user_id(user_id)
            if self.store_id_exist(store_id):
                return error.error_exist_store_id(store_id)

            # 建立店铺和用户的联系
            new = {
                "store_id": store_id,
                "user_id": user_id,
            }
            self.conn.user_store.insert_one(new)

        except errors.PyMongoError as e:
            # debug
            print(e)
            return 528, "{}".format(str(e))
        except BaseException as e:
            # debug
            print(e)
            return 530, "{}".format(str(e))
        return 200, "ok"
