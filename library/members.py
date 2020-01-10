#!/usr/bin/python3

# Author: Nilesh Ghule <nilesh@sunbeaminfo.com>
# library -> members.py
# Date: 8/11/19

import db
from datetime import datetime


def user_new(id=0, name='', email='', phone='', passwd='', role='member'):
    user = {
        'id': id,
        'name': name,
        'email': email,
        'phone': phone,
        'passwd': passwd,
        'role': role
    }
    return user


def user_sign_up(member):
    return db.user_insert_new(member)


def user_sign_in(email, password):
    member = db.user_find_by_email(email)
    if member['passwd'] == password:
        return member
    else:
        return None


def user_change_password(member, new_password):
    member['passwd'] = new_password
    return db.user_update(member)


def user_edit_profile(member, new_email=None, new_mobile=None):
    if new_email is not None:
        member['email'] = new_email
    if new_mobile is not None:
        member['mobile'] = new_mobile
    return db.user_update(member)


def user_is_paid(member_id):
    payment = db.payment_find_last_paid(member_id)
    if payment is None:
        return False
    return payment['due_date'].date() > datetime.now().date()


def user_find_all():
    return db.user_find_all()

