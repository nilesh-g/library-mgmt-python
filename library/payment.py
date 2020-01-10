#!/usr/bin/python3

# Author: Nilesh Ghule <nilesh@sunbeaminfo.com>
# library -> payment.py
# Date: 11/11/19

from datetime import datetime
from datetime import timedelta
import db

def payment_new(id=0, member_id=0, amount=0, type='fee', tx_time=datetime.now(), due_date=datetime.now()+timedelta(days=28)):
    if type != 'fee': # fine
        due_date = None
    payment = {
        'id': id,
        'member_id': member_id,
        'amount': amount,
        'type': type,
        'tx_time': tx_time,
        'due_date': due_date
    }
    return payment


def payment_add_new(payment):
    return db.payment_insert_new(payment)


def payment_update(payment):
    return db.payment_update(payment)


def payment_find_by_id(payment_id):
    return db.payment_find_by_id(payment_id)


def payment_find_by_member(user_id, type='fee'):
    return db.payment_find_by_member(user_id, type)


def payment_find_last_paid(user_id, type='fee'):
    return db.payment_find_last_paid(user_id, type)

