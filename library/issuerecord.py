#!/usr/bin/python3

# Author: Nilesh Ghule <nilesh@sunbeaminfo.com>
# library -> issuerecord.py
# Date: 8/11/19

from datetime import datetime
from datetime import timedelta
import db
import config


def issue_record_new(id=0, copy_id=0, member_id=0, issued=datetime.now(), return_due=None, returned=None, fine=None):
    issue = {
        'id': id,
        'copy_id': copy_id,
        'member_id': member_id,
        'issued': issued,
        'return_due': return_due,
        'returned': returned,
        'fine': fine
    }
    return issue


def book_issue(book_id, member_id):
    book_copies = db.bookcopy_find_by_status(book_id, 'available')
    if len(book_copies) == 0:
        return -1
    copy = book_copies[0]
    copy['status'] = 'issued'
    if db.bookcopy_update(copy) == 0:
        copy['status'] = 'available'
        return 0
    issue = issue_record_new(copy_id=copy['id'], member_id=member_id, issued=datetime.now(), return_due=datetime.now()+timedelta(days=config.cfg['borrow_duration_days']))
    return db.issuerecord_insert_new(issue)


def book_return(issuerecord_id):
    record = issuerecord_find_by_id(issuerecord_id)
    record['returned'] = datetime.now()
    diff = record['returned'] - record['return_due']
    if diff.days > 0:
        record['fine'] = diff.days * config.cfg['fine_per_day']
    if db.issuerecord_update(record) == 0:
        return None
    copy = record['copy']
    copy['status'] = 'available'
    if db.bookcopy_update(copy) == 0:
        return 0
    return record


def get_issued_books(member_id):
    issued_list = db.issuerecord_find_by_member(member_id, 'issued')
    for record in issued_list:
        copy = db.bookcopy_find_by_id(record['copy_id'])
        record['copy'] = copy
        book = db.book_find_by_id(copy['bookid'])
        copy['book'] = book
    return issued_list


def issuerecord_find_by_id(issue_id):
    record = db.issuerecord_find_by_id(issue_id)
    if record is not None:
        copy = db.bookcopy_find_by_id(record['copy_id'])
        record['copy'] = copy
        book = db.book_find_by_id(copy['bookid'])
        copy['book'] = book
    return record

