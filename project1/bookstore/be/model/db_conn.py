from be.model import store


class DBConn:
    def __init__(self):
        self.conn = store.get_db_conn()

    # 查找user_id是否存在
    def user_id_exist(self, user_id):
        info = {
            "user_id": user_id,
        }
        count = self.conn.users.count_documents(info)
        if count == 0:
            return False
        else:
            return True

    # 查找当前商店中有没有这本书
    def book_id_exist(self, store_id, book_id):
        info = {
            "store_id": store_id,
            "books.book_id": book_id,
        }
        count = self.conn.stores.count_documents(info)
        if count == 0:
            return False
        else:
            return True

    # 查找商店是否存在
    def store_id_exist(self, store_id):
        info = {
            "store_id": store_id,
        }
        count = self.conn.user_store.count_documents(info)
        if count == 0:
            return False
        else:
            return True
