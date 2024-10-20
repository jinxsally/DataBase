json = {
    "user_id": "jinx",
    "store_id": "1",
    "book_info": {
        "id": "1000067",
        "title": "美丽心灵",
        "author": "[美] 西尔维娅·娜萨",
        "publisher": "上海科技教育出版社",
        "original_title": "A Beautiful Mind : Genius, Schizophrenia and Recovery in the Life of a Nobel Laureate",
        "translator": "王尔山",
        "pub_year": "2002-1",
        "pages": 594,
        "price": 3879,
        "currency_unit": "元",
        "binding": "平装",
        "isbn": "9787542823823",
        "author_intro": "西尔维娅・娜萨，曾任《财富》杂志和《美国新闻与世界报道》记者，现任《纽约时报》经济记者，本书是她的处女作。\n娜萨写出了一部扣人心弦的报告，它牵涉到一个令人难以置信的人物、一个“美丽”的心灵以及可怕的精神错乱。她也写出了一则非常动人的爱情故事，一部在充满恶梦与天才的世界里人类的亲密关系居于中心地位的报告。\n――《新英格兰医学杂志》\n",
        "book_intro": "在这本感人至深的生动传记中，作者逼真地再现了一个数学天才——纳什的一生，他的生涯被精神分裂症所打断，但是在经受30年毁灭性的精神疾病困扰后，竟奇迹般地康复，并因年轻时在博弈论方面的奠基性工作，获得1994年诺贝尔经济学奖。本书第一版译作《普林斯顿的幽灵：纳什传》，亦使用同一ISBN。\n",
        "content": "",
        "tags": "传记\n纳什\n数学\n美丽心灵\n博弈论\n经济学\n人物\n大师\n",
        "picture": "com.intellij.database.extractors.ImageInfo@faec5a8f",
    },
    "stock_level": "10",
}
url = urljoin("http://127.0.0.1:5000/seller/", "add_book")
r = requests.post(url, json=json)
print(r)