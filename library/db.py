#!/usr/bin/python3

# Author: Nilesh Ghule <nilesh@sunbeaminfo.com>
# library -> db.py
# Date: 8/11/19

from dbutil import exec_dql_query
from dbutil import exec_dml_query
from datetime import datetime
from datetime import timedelta
import members
import books
import issuerecord
import payment

# -------------------------------------------------------------------------------
# users functions
# -------------------------------------------------------------------------------


def user_insert_new(member):
    sql = "INSERT INTO members(name, email, phone, passwd, role) VALUES (%s, %s, %s, %s, %s)"
    cnt = exec_dml_query(sql, (member['name'], member['email'], member['phone'], member['passwd'], member['role']))
    return cnt


def user_find_by_email(email):
    sql = "SELECT id, name, email, phone, passwd, role FROM members WHERE email=%s"
    result = exec_dql_query(sql, (email,))
    if len(result) > 0:
        data = result[0]
        return members.user_new(id=data[0], name=data[1], email=data[2], phone=data[3], passwd=data[4], role=data[5])
    else:
        return None


def user_find_all():
    sql = "SELECT id, name, email, phone, passwd, role FROM members"
    result = exec_dql_query(sql)
    user_list = []
    for data in result:
        member = members.user_new(id=data[0], name=data[1], email=data[2], phone=data[3], passwd='*****', role=data[5])
        user_list.append(member)
    return user_list


def user_update(member):
    sql = "UPDATE members SET name=%s, email=%s, phone=%s, passwd=%s, role=%s WHERE id=%s"
    cnt = exec_dml_query(sql, (member['name'], member['email'], member['phone'], member['passwd'], member['role'], member['id']))
    return cnt


def user_delete(member_id):
    sql = "DELETE FROM members WHERE id=%s"
    cnt = exec_dml_query(sql, (member_id, ))
    return cnt


# -------------------------------------------------------------------------------
# books functions
# -------------------------------------------------------------------------------


def book_insert_new(book):
    sql = "INSERT INTO books(name, author, subject, price, isbn) VALUES (%s, %s, %s, %s, %s)"
    cnt = exec_dml_query(sql, (book['name'], book['author'], book['subject'], book['price'], book['isbn']))
    return cnt


def book_find_by_id(book_id):
    sql = "SELECT id, name, author, subject, price, isbn FROM books WHERE id=%s"
    result = exec_dql_query(sql, (book_id,))
    if len(result) > 0:
        data = result[0]
        return books.book_new(id=data[0], name=data[1], author=data[2], subject=data[3], price=data[4], isbn=data[5])
    else:
        return None


def book_find_by_name(name):
    name = '%' + name + '%'
    sql = "SELECT id, name, author, subject, price, isbn FROM books WHERE name LIKE %s"
    result = exec_dql_query(sql, (name,))
    book_list = []
    for data in result:
        b = books.book_new(id=data[0], name=data[1], author=data[2], subject=data[3], price=data[4], isbn=data[5])
        book_list.append(b)
    return book_list


def book_update(book):
    sql = "UPDATE books SET name=%s, author=%s, subject=%s, price=%s, isbn=%s WHERE id=%s"
    cnt = exec_dml_query(sql, (book['name'], book['author'], book['subject'], book['price'], book['isbn'], book['id']))
    return cnt


def book_delete(book_id):
    sql = "DELETE FROM books WHERE id=%s"
    cnt = exec_dml_query(sql, (book_id, ))
    return cnt


# -------------------------------------------------------------------------------
# book copies functions
# -------------------------------------------------------------------------------


def bookcopy_insert_new(copy):
    sql = "INSERT INTO copies(bookid, rack, status) VALUES (%s, %s, %s)"
    cnt = exec_dml_query(sql, (copy['bookid'], copy['rack'], copy['status']))
    return cnt


def bookcopy_find_by_id(copy_id):
    sql = "SELECT id, bookid, rack, status FROM copies WHERE id=%s"
    result = exec_dql_query(sql, (copy_id,))
    if len(result) > 0:
        data = result[0]
        return books.book_copy_new(id=data[0], bookid=data[1], rack=data[2], status=data[3])
    else:
        return None


def bookcopy_find_by_status(book_id=0, status='available'):
    if id == 0:
        sql = "SELECT id, bookid, rack, status FROM copies WHERE status=%s"
        result = exec_dql_query(sql, (status,))
    else:
        sql = "SELECT id, bookid, rack, status FROM copies WHERE bookid=%s AND status=%s"
        result = exec_dql_query(sql, (book_id, status))

    copy_list = []
    for data in result:
        b = books.book_copy_new(id=data[0], bookid=data[1], rack=data[2], status=data[3])
        copy_list.append(b)
    return copy_list


def bookcopy_update(copy):
    sql = "UPDATE copies SET bookid=%s, rack=%s, status=%s WHERE id=%s"
    cnt = exec_dml_query(sql, (copy['bookid'], copy['rack'], copy['status'], copy['id']))
    return cnt


def bookcopy_delete(copy_id):
    sql = "DELETE FROM copies WHERE id=%s"
    cnt = exec_dml_query(sql, (copy_id, ))
    return cnt


# -------------------------------------------------------------------------------
# issue functions
# -------------------------------------------------------------------------------


def issuerecord_insert_new(issue):
    sql = "INSERT INTO issuerecord(copyid, memberid, issued, returndue, returned, fine) VALUES (%s, %s, %s, %s, %s, %s)"
    cnt = exec_dml_query(sql, (issue['copy_id'], issue['member_id'], issue['issued'], issue['return_due'], issue['returned'], issue['fine']))
    return cnt


def issuerecord_update(issue):
    sql = "UPDATE issuerecord SET copyid=%s, memberid=%s, issued=%s, returndue=%s, returned=%s, fine=%s WHERE id=%s"
    cnt = exec_dml_query(sql, (issue['copy_id'], issue['member_id'], issue['issued'], issue['return_due'], issue['returned'], issue['fine'], issue['id']))
    return cnt


def issuerecord_find_by_id(issue_id):
    sql = "SELECT id, copyid, memberid, issued, returndue, returned, fine FROM issuerecord WHERE id=%s"
    result = exec_dql_query(sql, (issue_id,))
    if len(result) > 0:
        data = result[0]
        return issuerecord.issue_record_new(id=data[0], copy_id=data[1], member_id=data[2], issued=data[3], return_due=data[4], returned=data[5], fine=data[6])
    else:
        return None


def issuerecord_find_by_member(user_id, status='issued'):
    if status == 'issued':
        sql = "SELECT id, copyid, memberid, issued, returndue, returned, fine FROM issuerecord WHERE memberid=%s AND returned IS NULL"
    elif status == 'returned':
        sql = "SELECT id, copyid, memberid, issued, returndue, returned, fine FROM issuerecord WHERE memberid=%s AND returned IS NOT NULL"
    else:
        sql = "SELECT id, copyid, memberid, issued, returndue, returned, fine FROM issuerecord WHERE memberid=%s"
    issue_records = []
    result = exec_dql_query(sql, (user_id,))
    for data in result:
        record = issuerecord.issue_record_new(id=data[0], copy_id=data[1], member_id=data[2], issued=data[3], return_due=data[4], returned=data[5], fine=data[6])
        issue_records.append(record)
    return issue_records


def issuerecord_delete(issue_id):
    sql = "DELETE FROM issuerecord WHERE id=%s"
    cnt = exec_dml_query(sql, (issue_id, ))
    return cnt


# -------------------------------------------------------------------------------
# payments functions
# -------------------------------------------------------------------------------


def payment_insert_new(payment):
    sql = "INSERT INTO payments(memberid, amount, type, txtime, duedate) VALUES (%s, %s, %s, %s, %s)"
    cnt = exec_dml_query(sql, (payment['member_id'], payment['amount'], payment['type'], payment['tx_time'], payment['due_date']))
    return cnt


def payment_update(payment):
    sql = "UPDATE payments SET memberid=%s, amount=%s, type=%s, txtime=%s, duedate=%s WHERE id=%s"
    cnt = exec_dml_query(sql, (payment['member_id'], payment['amount'], payment['type'], payment['tx_time'], payment['due_date'], payment['id']))
    return cnt


def payment_find_by_id(payment_id):
    sql = "SELECT id, memberid, amount, type, txtime, duedate FROM payments WHERE id=%s"
    result = exec_dql_query(sql, (payment_id,))
    if len(result) > 0:
        data = result[0]
        return payment.payment_new(id=data[0], member_id=data[1], amount=data[2], type=data[3], tx_time=data[4], due_date=data[5])
    else:
        return None


def payment_find_by_member(user_id, type='fee'):
    if type == 'fee':
        sql = "SELECT id, memberid, amount, type, txtime, duedate FROM payments WHERE memberid=%s AND type='fee' ORDER BY txtime DESC"
    elif type == 'fine':
        sql = "SELECT id, memberid, amount, type, txtime, duedate FROM payments WHERE memberid=%s AND type='fine' ORDER BY txtime DESC"
    else:
        sql = "SELECT id, memberid, amount, type, txtime, duedate FROM payments WHERE memberid=%s ORDER BY txtime DESC"
    payments = []
    result = exec_dql_query(sql, (user_id,))
    for data in result:
        record = payment.payment_new(id=data[0], member_id=data[1], amount=data[2], type=data[3], tx_time=data[4], due_date=data[5])
        payments.append(record)
    return payments


def payment_find_last_paid(user_id, type='fee'):
    if type == 'fee':
        sql = "SELECT id, memberid, amount, type, txtime, duedate FROM payments WHERE memberid=%s AND type='fee' ORDER BY txtime DESC LIMIT 1"
    elif type == 'fine':
        sql = "SELECT id, memberid, amount, type, txtime, duedate FROM payments WHERE memberid=%s AND type='fine' ORDER BY txtime DESC LIMIT 1"
    else:
        sql = "SELECT id, memberid, amount, type, txtime, duedate FROM payments WHERE memberid=%s ORDER BY txtime DESC LIMIT 1"
    result = exec_dql_query(sql, (user_id,))
    if len(result) > 0:
        data = result[0]
        return payment.payment_new(id=data[0], member_id=data[1], amount=data[2], type=data[3], tx_time=data[4], due_date=data[5])
    else:
        return None


# -------------------------------------------------------------------------------
# reports functions
# -------------------------------------------------------------------------------

def subjectwise_copies():
    sql = "SELECT b.subject, COUNT(c.id) FROM books b INNER JOIN copies c ON c.bookid = b.id GROUP BY b.subject"
    report = []
    list = exec_dql_query(sql)
    for data in list:
        report.append(dict(subject=data[0], count=data[1]))
    return report


def bookwise_copies():
    sql = "SELECT b.id, b.name, SUM(status='available') available, SUM(status='issued') issued, COUNT(c.id) count FROM books b INNER JOIN copies c ON c.bookid = b.id GROUP BY b.id, b.name"
    report = []
    list = exec_dql_query(sql)
    for data in list:
        report.append(dict(id=data[0], name=data[1], available=data[2], issued=data[3], count=data[4]))
    return report


def daterange_fees_fine_collection(start=datetime.now(), end=datetime.now()):
    sql = "SELECT type, SUM(amount) FROM payments WHERE DATE(txtime) BETWEEN DATE(%s) AND DATE(%s) GROUP BY type"
    report = []
    list = exec_dql_query(sql, (start, end))
    for data in list:
        report.append(dict(type=data[0], amount=data[1]))
    return report


def daily_collection(start=datetime.now(), end=datetime.now()):
    sql = "SELECT DATE(txtime) txdate, SUM(IF(type='fee', amount, 0.0)) fee, SUM(IF(type='fine', amount, 0.0)) fine FROM payments WHERE DATE(txtime) BETWEEN DATE(%s) AND DATE(%s) GROUP BY DATE(txtime), type"
    report = []
    list = exec_dql_query(sql, (start, end))
    for data in list:
        report.append(dict(tx_date=data[0], fee=data[1], fine=data[2]))
    return report


def monthly_collection(start=datetime.now(), end=datetime.now()):
    sql = "SELECT DATE_FORMAT(txtime, '%b-%y') txmonth, SUM(IF(type='fee', amount, 0.0)) fee, SUM(IF(type='fine', amount, 0.0)) fine FROM payments WHERE DATE(txtime) BETWEEN DATE(%s) AND DATE(%s) GROUP BY DATE_FORMAT(txtime, '%b-%y') txmonth, type"
    report = []
    list = exec_dql_query(sql, (start, end))
    for data in list:
        report.append(dict(tx_month=data[0], fee=data[1], fine=data[2]))
    return report


