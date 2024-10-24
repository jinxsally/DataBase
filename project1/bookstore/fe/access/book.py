import os
import sqlite3 as sqlite
import random
import base64
import pymongo
import numpy as np


class Book:
    id: str
    title: str
    author: str
    publisher: str
    original_title: str
    translator: str
    pub_year: str
    pages: int
    price: int
    currency_unit: str
    binding: str
    isbn: str
    author_intro: str
    book_intro: str
    content: str
    tags: [str]
    pictures: [bytes]

    def __init__(self):
        self.tags = []
        self.pictures = []


class BookDB:
    def __init__(self, large: bool = False):
        client = pymongo.MongoClient("mongodb://localhost:27017")
        self.db = client["BookStore"]
        try:
            self.db.books.create_index([("id", pymongo.ASCENDING)])
        except:
            pass

    def get_book_count(self):
        book_col = self.db["books"]
        count = book_col.count_documents({})
        return count

    def get_book_info(self, start, size) -> [Book]:
        books = []
        book_col = self.db["books"]
        content = book_col.find().skip(start).limit(size)

        for row in content:
            book = Book()
            book.id = row.get("id")
            book.title = row.get("title")
            book.author = row.get("author")
            book.publisher = row.get("publisher")
            book.original_title = row.get("original_title")
            book.translator = row.get("translator")
            book.pub_year = row.get("pub_year")
            book.pages = None if np.isnan(row.get("pages")) else int(row.get("pages"))
            book.price = row.get("price")
            book.currency_unit = row.get("currency_unit")
            book.binding = row.get("binding")
            book.isbn = row.get("isbn")
            book.author_intro = row.get("author_intro")
            book.book_intro = row.get("book_intro")
            book.content = row.get("content")

            tags = row.get("tags")
            picture = row.get("picture")

            for tag in tags.split("\n"):
                if tag.strip() != "":
                    book.tags.append(tag)

            for i in range(0, random.randint(0, 9)):
                if picture is not None:
                    # encode_str = base64.b64encode(picture).decode("utf-8")
                    encode_str = picture
                    book.pictures.append(encode_str)

            books.append(book)

        return books
