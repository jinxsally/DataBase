import jwt
import time
import logging
from be.model import error
from be.model import db_conn
import pymongo
import pymongo.errors

# encode a json string like:
#   {
#       "user_id": [user name],
#       "terminal": [terminal code],
#       "timestamp": [ts]} to a JWT
#   }


def jwt_encode(user_id: str, terminal: str) -> str:
    encoded = jwt.encode(
        {"user_id": user_id, "terminal": terminal, "timestamp": time.time()},
        key=user_id,
        algorithm="HS256",
    )
    return encoded


# decode a JWT to a json string like:
#   {
#       "user_id": [user name],
#       "terminal": [terminal code],
#       "timestamp": [ts]} to a JWT
#   }
def jwt_decode(encoded_token, user_id: str) -> str:
    decoded = jwt.decode(encoded_token, key=user_id, algorithms="HS256")
    return decoded


class User(db_conn.DBConn):
    token_lifetime: int = 3600  # 3600 second

    def __init__(self):
        db_conn.DBConn.__init__(self)

    # 检查给定的JWT是否有效
    def __check_token(self, user_id, db_token, token) -> bool:
        try:
            if db_token != token:
                return False
            jwt_text = jwt_decode(encoded_token=token, user_id=user_id)
            ts = jwt_text["timestamp"]
            if ts is not None:
                now = time.time()
                if self.token_lifetime > now - ts >= 0:
                    return True
        except jwt.exceptions.InvalidSignatureError as e:
            logging.error(str(e))
            return False

    # 注册
    def register(self, user_id: str, password: str):
        try:
            terminal = "terminal_{}".format(str(time.time()))
            token = jwt_encode(user_id, terminal)
            doc = {
                "_id": user_id,
                "user_id": user_id,
                "password": password,
                "balance": 0,
                "token": token,
                "terminal": terminal,
            }
            self.db["users"].insert_one(doc)
        except pymongo.errors.PyMongoError as e:
            return error.error_exist_user_id(user_id)
        return 200, "ok"

    # 检查权限
    def check_token(self, user_id: str, token: str) -> (int, str):
        doc = self.db["users"].find_one({"user_id": user_id}, {"token": 1, "_id": 0})
        if doc is None:
            return error.error_authorization_fail()
        db_token = doc["token"]
        if not self.__check_token(user_id, db_token, token):
            return error.error_authorization_fail()
        return 200, "ok"

    # 检查密码
    def check_password(self, user_id: str, password: str) -> (int, str):
        doc = self.db["users"].find_one(
            {"user_id": user_id}, {"password": 1, "_id": 0}
        )
        if doc is None:
            return error.error_authorization_fail()

        if password != doc["password"]:
            return error.error_authorization_fail()

        return 200, "ok"

    # 登录
    def login(self, user_id: str, password: str, terminal: str) -> (int, str, str):
        token = ""
        try:
            code, message = self.check_password(user_id, password)
            if code != 200:
                return code, message, ""

            token = jwt_encode(user_id, terminal)
            result = self.db["users"].update_one(
                {"user_id": user_id}, {"$set": {"token": token, "terminal": terminal}}
            )
            if result.modified_count == 0:
                return error.error_authorization_fail() + ("",)

        except pymongo.errors.PyMongoError as e:
            return 528, "{}".format(str(e)), ""
        except BaseException as e:
            print(e)
            return 530, "{}".format(str(e)), ""
        return 200, "ok", token

    # 登出
    def logout(self, user_id: str, token: str) -> bool:
        try:
            code, message = self.check_token(user_id, token)
            if code != 200:
                return code, message

            terminal = "terminal_{}".format(str(time.time()))
            dummy_token = jwt_encode(user_id, terminal)

            result = self.db["users"].update_one(
                {"user_id": user_id},
                {"$set": {"token": dummy_token, "terminal": terminal}},
            )
            if result.modified_count == 0:
                return error.error_authorization_fail()
        except pymongo.errors.PyMongoError as e:
            return 528, "{}".format(str(e))
        except BaseException as e:
            return 530, "{}".format(str(e))
        return 200, "ok"

    # 注销
    def unregister(self, user_id: str, password: str) -> (int, str):
        try:
            code, message = self.check_password(user_id, password)
            if code != 200:
                return code, message

            result = self.db["users"].delete_one({"user_id": user_id})
            if result.deleted_count == 0:
                return error.error_authorization_fail()

        except pymongo.errors.PyMongoError as e:
            return 528, "{}".format(str(e))
        except BaseException as e:
            return 530, "{}".format(str(e))
        return 200, "ok"

    # 修改密码
    def change_password(
        self, user_id: str, old_password: str, new_password: str
    ) -> bool:
        try:
            code, message = self.check_password(user_id, old_password)
            if code != 200:
                return code, message

            terminal = "terminal_{}".format(str(time.time()))
            token = jwt_encode(user_id, terminal)
            result = self.db["users"].update_one(
                {"user_id": user_id},
                {
                    "$set": {
                        "password": new_password,
                        "token": token,
                        "terminal": terminal,
                    }
                },
            )
            if result.modified_count == 0:
                return error.error_authorization_fail()
        except pymongo.errors.PyMongoError as e:
            return 528, "{}".format(str(e))
        except BaseException as e:
            return 530, "{}".format(str(e))
        return 200, "ok"

    # 搜索
    def search(self, user_id: str, store_id: str, key: str, page: int, page_size: int):
        try:
            if not self.user_id_exist(user_id):
                # debug
                return error.error_non_exist_user_id(user_id)
            if not self.store_id_exist(store_id):
                # debug
                return error.error_non_exist_store_id(store_id)

            # 执行查询操作，两种情况

            # 店铺搜索
            if store_id:
                query = {
                    "store_id": store_id,
                    "books.stock_level": {"$gt": 0},  # 库存量大于等于0
                    "books": {
                        "$elemMatch": {
                            "book_info": {
                                "$regex": key,  # 存在关键词的都需要
                                "$options": "i",  # 不区分大小写
                            }
                        }
                    },
                }
                books = (
                    self.db.stores.find(query)
                    .skip((page - 1) * page_size)  # 跳过已经浏览过的界面
                    .limit(page_size)  # 限制浏览数量
                )

            # 全局搜索
            else:
                query = {
                    "books.stock_level": {"$gt": 0},  # 库存量大于等于0
                    "books": {
                        "$elemMatch": {
                            "book_info": {
                                "$regex": key,
                                "$options": "i",
                            }
                        }
                    },
                }
                books = (
                    self.db.stores.find(query)
                    .skip((page - 1) * page_size)  # 跳过已经浏览过的界面
                    .limit(page_size)  # 限制浏览数量
                )

            # 筛选执行结果的信息
            ans = []

            for book in books:
                ans.append(book)

        except pymongo.errors.PyMongoError as e:
            return 528, "{}".format(str(e))
        except BaseException as e:
            return 530, "{}".format(str(e))
        return 200, "ok", ans
