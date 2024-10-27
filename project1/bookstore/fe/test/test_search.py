import pytest
import uuid
import random
from fe.access.new_buyer import register_new_buyer
from fe.access import auth
from fe.test.gen_book_data import GenBook
from fe import conf


class TestSearch:
    @pytest.fixture(autouse=True)
    def pre_run_initialization(self):
        self.auth = auth.Auth(conf.URL)
        # 注册用户
        self.user_id = "test_search_{}".format(str(uuid.uuid1()))
        self.password = "password_" + self.user_id
        self.terminal = "terminal_" + self.user_id
        assert self.auth.register(self.user_id, self.password) == 200

        # 登录用户
        assert self.auth.login(self.user_id, self.password, self.terminal)

        # 注册店铺
        self.seller_id = "test_search_seller_id_{}".format(str(uuid.uuid1()))
        self.store_id = "test_search_store_id_{}".format(str(uuid.uuid1()))
        self.gen_book = GenBook(self.seller_id, self.store_id)

        # 生成图书数据
        self.gen_book.gen(non_exist_book_id=False, low_stock_level=False)
        self.seller = self.gen_book.seller

        # 设置标题数据
        self.valid_title = self.gen_book.buy_book_info_list[0][0].title
        self.invalid_title = "_x"
        # 设置标签数据
        self.valid_tag = self.gen_book.buy_book_info_list[0][0].tags[0]
        self.invalid_tag = "_x"
        # 设置介绍数据
        self.valid_intro = self.gen_book.buy_book_info_list[0][0].book_intro
        self.invalid_intro = "_x"
        # 设置内容数据
        self.valid_content = self.gen_book.buy_book_info_list[0][0].content
        self.invalid_content = "_x"

        yield

    # user_id错误
    def test_error_user_id(self):
        user_id = self.user_id + "_x"
        code = self.auth.search(
            user_id=user_id,
            store_id="",
            sort=1,
            key="",
            page=random.randint(1, 10),
            page_size=random.randint(1, 11),
        )
        assert code == 511

    """***************书名搜索******************"""

    # 参数化测试
    @pytest.mark.parametrize(
        "key, expected_code",
        [
            (0, 200),  # 书名存在
            (1, 521),  # 书名不存在
        ],
    )

    # 店铺
    def test_search_by_title_store(self, key, expected_code):
        # 占位符替换
        if key == 0:
            key = self.valid_title
        elif key == 1:
            key = self.invalid_title
        code = self.auth.search(
            user_id=self.user_id,
            store_id=self.store_id,
            sort=1,
            key=key,
            page=1,
            page_size=random.randint(1, 11),
        )
        assert code == expected_code

    # 参数化测试
    @pytest.mark.parametrize(
        "key, expected_code",
        [
            (0, 200),  # 书名存在
            (1, 521),  # 书名不存在
        ],
    )
    # 全局
    def test_search_by_title(self, key, expected_code):
        # 占位符替换
        if key == 0:
            key = self.valid_title
        elif key == 1:
            key = self.invalid_title
        code = self.auth.search(
            user_id=self.user_id,
            store_id="",
            sort=1,
            key=key,
            page=1,
            page_size=random.randint(1, 11),
        )
        assert code == expected_code

    # """***************标签搜索******************"""

    @pytest.mark.parametrize(
        "key, expected_code",
        [
            (0, 200),  # 标签存在
            (1, 521),  # 标签不存在
        ],
    )
    def test_search_by_tag_store(self, key, expected_code):
        # 占位符替换
        if key == 0:
            key = self.valid_tag
        elif key == 1:
            key = self.invalid_tag
        code = self.auth.search(
            user_id=self.user_id,
            store_id=self.store_id,
            sort=2,
            key=key,
            page=1,
            page_size=random.randint(1, 11),
        )
        assert code == expected_code

    @pytest.mark.parametrize(
        "key, expected_code",
        [
            (0, 200),  # 标签存在
            (1, 521),  # 标签不存在
        ],
    )
    def test_search_by_tag(self, key, expected_code):
        if key == 0:
            key = self.valid_tag
        elif key == 1:
            key = self.invalid_tag
        code = self.auth.search(
            user_id=self.user_id,
            store_id="",
            sort=2,
            key=key,
            page=1,
            page_size=random.randint(1, 11),
        )
        assert code == expected_code

    """***************书籍介绍搜索******************"""

    @pytest.mark.parametrize(
        "key, expected_code",
        [
            (0, 200),  # 介绍存在
            (1, 521),  # 介绍不存在
        ],
    )
    def test_search_by_intro_store(self, key, expected_code):
        # 占位符替换
        if key == 0:
            key = self.valid_intro
        elif key == 1:
            key = self.invalid_intro
        code = self.auth.search(
            user_id=self.user_id,
            store_id=self.store_id,
            sort=3,
            key=key,
            page=1,
            page_size=random.randint(1, 11),
        )
        assert code == expected_code

    @pytest.mark.parametrize(
        "key, expected_code",
        [
            (0, 200),  # 介绍存在
            (1, 521),  # 介绍不存在
        ],
    )
    def test_search_by_intro(self, key, expected_code):
        # 占位符替换
        if key == 0:
            key = self.valid_intro
        elif key == 1:
            key = self.invalid_intro
        code = self.auth.search(
            user_id=self.user_id,
            store_id="",
            sort=3,
            key=key,
            page=1,
            page_size=random.randint(1, 11),
        )
        assert code == expected_code

    """***************书籍内容搜索******************"""

    @pytest.mark.parametrize(
        "key, expected_code",
        [
            (0, 200),  # 介绍存在
            (1, 521),  # 介绍不存在
        ],
    )
    def test_search_by_content_store(self, key, expected_code):
        # 占位符替换
        if key == 0:
            key = self.valid_content
        elif key == 1:
            key = self.invalid_content
        code = self.auth.search(
            user_id=self.user_id,
            store_id=self.store_id,
            sort=4,
            key=key,
            page=1,
            page_size=random.randint(1, 11),
        )
        assert code == expected_code

    @pytest.mark.parametrize(
        "key, expected_code",
        [
            (0, 200),  # 介绍存在
            (1, 521),  # 介绍不存在
        ],
    )
    def test_search_by_content(self, key, expected_code):
        # 占位符替换
        if key == 0:
            key = self.valid_content
        elif key == 1:
            key = self.invalid_content
        code = self.auth.search(
            user_id=self.user_id,
            store_id="",
            sort=4,
            key=key,
            page=1,
            page_size=random.randint(1, 11),
        )
        assert code == expected_code

    """***************全站搜索******************"""

    @pytest.mark.parametrize(
        "key, expected_code",
        [
            (0, 200),
            (1, 521),
        ],
    )
    def test_search_by_all(self, key, expected_code):
        # 占位符替换
        if key == 0:
            key = self.valid_title
        elif key == 1:
            key = self.invalid_title
        code = self.auth.search(
            user_id=self.user_id,
            store_id="",
            sort=0,
            key=key,
            page=1,
            page_size=random.randint(1, 11),
        )
        assert code == expected_code
