import json
import pytest
from fe.test.gen_book_data import GenBook
from fe.access.new_buyer import register_new_buyer
from fe.access.new_seller import register_new_seller
from fe.access import buyer,auth
from fe import conf
import uuid
import pytest

from fe.access import auth
from fe import conf


class TestSendBooks:
    @pytest.fixture(autouse=True)
    def pre_run_initialization(self):
        self.seller_id = "test_send_books_seller_id_{}".format(str(uuid.uuid1()))
        self.store_id = "test_send_books_store_id_{}".format(str(uuid.uuid1()))
        self.buyer_id = "test_send_books_buyer_id_{}".format(str(uuid.uuid1()))
        self.password = self.seller_id
        self.buyer = register_new_buyer(self.buyer_id, self.password)
        self.gen_book = GenBook(self.seller_id, self.store_id)
        self.temp_order = None

        yield


    def test_search_ok(self):
        code, result = self.buyer.search("章云", 0)
        assert code == 200

    def test_search_ok_page(self):
        code, result = self.buyer.search("章云", 1)
        assert code == 200

    def test_search_empty_content(self):
        code, result = self.buyer.search("章云1024", 1)
        assert result==[]

    def test_search_empty_page(self):
        code, result = self.buyer.search("章云1024", 1000)
        assert result==[]

    def test_search_empty(self):
        code, result = self.buyer.search("章云1024", 1000)
        assert result==[]

    def test_search_many_ok(self):
        list=["余秋雨","汪曾祺"]
        code, result = self.buyer.search_many(list)
        assert code == 200

    def test_search_many_u_ok(self): 
        list = ["余秋雨", "汪曾祺", "成长"]
        code, result = self.buyer.search_many(list)
        assert code == 200

    def test_search_many_ok_u(self):
        list=["余秋雨","汪曾祺1024"]
        code, result = self.buyer.search_many(list)
        assert code == 200

    def test_search_many_empty(self):#分页
        list=["余秋雨1024","汪曾祺2048"]
        code, result = self.buyer.search_many(list)
        assert result==[]

    def test_search_in_store_ok(self):
        search_key="撒哈拉"
        store_id="test_add_books_store_id_413e6f48-06c2-11ef-a85d-e69a436c88b7"
        page=0
        code, result = self.buyer.search_in_store(store_id,search_key,page)
        assert code == 200

    def test_search_in_store_page_ok(self):
        search_key="撒哈拉"
        store_id="test_add_books_store_id_413e6f48-06c2-11ef-a85d-e69a436c88b7"
        page=1
        code, result = self.buyer.search_in_store(store_id,search_key,page)
        assert code == 200


