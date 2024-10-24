from be.model import store


class DBConn:
    def __init__(self):
        self.client = store.get_db_conn()
        self.db = self.client

    def user_id_exist(self, user_id):
        doc = self.db["users"].find_one({"user_id": user_id})
        if doc is None:
            return False
        else:
            return True

    def book_id_exist(self, store_id, book_id):
        doc = self.db["stores"].find_one(
            {"store_id": store_id, "books.book_id": book_id}
        )
        if doc is None:
            return False
        else:
            return True

    def store_id_exist(self, store_id):
        doc = self.db["user_store"].find_one({"store_id": store_id})
        if doc is None:
            return False
        else:
            return True

    def order_id_exist(self, order_id):
        doc = self.db["new_orders"].find_one({"order_id": order_id})
        if doc is None:
            return False
        else:
            return True
