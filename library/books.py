#!/usr/bin/python3

# Author: Nilesh Ghule <nilesh@sunbeaminfo.com>
# library -> books.py
# Date: 8/11/19

import db


def book_new(id=0, name='', author='', subject='', price=0.0, isbn=''):
    book = {
        'id': id,
        'name': name,
        'author': author,
        'subject': subject,
        'price': price,
        'isbn': isbn
    }
    return book


def book_copy_new(id=0, bookid=0, rack='', status='available'):
    copy = {
        'id': id,
        'bookid': bookid,
        'rack': rack,
        'status': status
    }
    return copy


def book_add_new(book):
    return db.book_insert_new(book)


def book_update(book):
    return db.book_update(book)


def book_find_by_name(name):
    return db.book_find_by_name(name)


def book_find_by_id(book_id):
    return db.book_find_by_id(book_id)


def book_get_available_copies(book_id):
    avail_copies = db.bookcopy_find_by_status(book_id, 'available')
    return avail_copies


def bookcopy_add_new(copy):
    return db.bookcopy_insert_new(copy)


def bookcopy_find_by_id(copy_id):
    return db.bookcopy_find_by_id(copy_id)


def bookcopy_change_rack(copy, new_rack):
    copy['rack'] = new_rack
    return db.bookcopy_update(copy)
