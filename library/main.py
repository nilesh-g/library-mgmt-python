#!/usr/bin/python3

# Author: Nilesh Ghule <nilesh@sunbeaminfo.com>
# library -> main.py
# Date: 8/11/19

from datetime import date
import members
import books
import issuerecord
import payment
import reports
import os


def clrscr():
    input()
    os.system("clear")


def sign_in():
    cred = dict()
    cred['email'] = input("email: ")
    cred['passwd'] = input("passwd: ")
    user = members.user_sign_in(cred['email'], cred['passwd'])
    if user is not None:
        if user['role'] == 'owner':
            owner_area(user)
        elif user['role'] == 'librarian':
            librarian_area(user)
        else:
            members_area(user)
    else:
        print("invalid login.")
    return


def sign_up():
    new_member = members.user_new()
    print("enter member information:")
    new_member['name'] = input("name: ")
    new_member['email'] = input("email: ")
    new_member['phone'] = input("phone: ")
    new_member['passwd'] = input("passwd: ")
    new_member['role'] = 'member'
    cnt = members.user_sign_up(new_member)
    if cnt == 1:
        print("user registered successfully.")
    else:
        print("user register failed.")
    return


def edit_profile(user):
    new_email = input("new email: ")
    new_mobile = input("new mobile: ")
    cnt = members.user_edit_profile(user, new_email, new_mobile)
    if cnt == 1:
        print("profile updated successfully.")
    else:
        print("profile update failed.")


def change_password(user):
    new_passwd = input("new passwd: ")
    cnt = members.user_change_password(user, new_passwd)
    if cnt == 1:
        print("password updated successfully.")
    else:
        print("password update failed.")


def find_books():
    book_name = input("book name : ")
    book_list = books.book_find_by_name(book_name)
    for book in book_list:
        print(book)


def available_copies():
    book_id = int(input("enter book id: "))
    return books.book_get_available_copies(book_id)


def list_issued_books(user_id=0):
    if user_id == 0:
        user_id = input("enter user id: ")
    records = issuerecord.get_issued_books(user_id)
    for record in records:
        result = record['copy']['book'].copy()
        result['copy_id'] = record['copy_id']
        result['issue_id'] = record['id']
        result['issued'] = record['issued']
        result['return_due'] = record['return_due']
        print(result)


def list_payment_history(user_id=0):
    if user_id == 0:
        user_id = input("enter user id: ")
    records = payment.payment_find_by_member(user_id, type='all')
    for record in records:
        print(record)


def add_book():
    print("enter book info.")
    book = books.book_new()
    book['name'] = input("name: ")
    book['author'] = input("author: ")
    book['subject'] = input("subject: ")
    book['price'] = float(input("price: "))
    book['isbn'] = input("isbn: ")
    cnt = books.book_add_new(book)
    if cnt == 1:
        print("book added successfully.")
    else:
        print("book add failed.")


def edit_book():
    find_books()
    book_id = int(input("enter book id to edit: "))
    print("enter modified book info.")
    book = books.book_new()
    book['id'] = book_id
    book['name'] = input("name: ")
    book['author'] = input("author: ")
    book['subject'] = input("subject: ")
    book['price'] = float(input("price: "))
    book['isbn'] = input("isbn: ")
    cnt = books.book_update(book)
    if cnt == 1:
        print("book updated successfully.")
    else:
        print("book update failed.")


def add_book_copy():
    book_id = input("enter book id: ")
    book = books.book_find_by_id(book_id)
    if book is None:
        print("book is not found.")
        return
    copy = books.book_copy_new(bookid=book_id, status='available')
    copy['rack'] = input("enter rack: ")
    cnt = books.bookcopy_add_new(copy)
    if cnt == 1:
        print("book copy added successfully.")
    else:
        print("book copy add failed.")


def book_issue():
    member_id = int(input("member id: "))
    if members.user_is_paid(member_id):
        book_id = int(input("book id: "))
        result = issuerecord.book_issue(book_id, member_id)
        if result == -1:
            print("book not available.")
        elif result == 0:
            print("book issue failed.")
        else:
            print("book issued successfully.")
    else:
        print("user fee is not paid.")


def take_payment(user_id=0, type='fee', amount=0.0):
    if amount == 0.0:
        amount = float(input("enter " + type + " amount: "))
    else:
        print(type, " amount: ", amount)
    if user_id == 0:
        user_id = int(input("enter member id: "))
    pay = payment.payment_new(member_id=user_id, amount=amount, type=type)
    cnt = payment.payment_add_new(pay)
    if cnt == 1:
        print("payment done successfully.")
    else:
        print("payment failed.")


def book_return():
    issue_id = int(input("book issue id: "))
    issue_record = issuerecord.book_return(issue_id)
    if issue_record is not None:
        print("book returned successfully.")
        if issue_record['fine'] is not None:
            take_payment(user_id=issue_record['member_id'], type='fine', amount=issue_record['fine'])
    else:
        print("book return failed.")


def members_area(user):
    while 1:
        clrscr()
        print("\n\n0. sign out\n1. edit profile\n2. change password\n3. find book by name\n4. check book availability\n5. list issued books\n6. payment history")
        choice = input("enter choice: ")
        if choice == '0':
            return
        elif choice == '1':
            edit_profile(user)
        elif choice == '2':
            change_password(user)
        elif choice == '3':
            find_books()
        elif choice == '4':
            copies_list = available_copies()
            print("available copies: ", len(copies_list))
        elif choice == '5':
            list_issued_books(user['id'])
        elif choice == '6':
            list_payment_history(user['id'])
        else:
            print("invalid option.")


def find_all_users():
    users = members.user_find_all()
    for user in users:
        print(user)


def change_rack():
    copy_id = int(print("enter book copy id: "))
    copy = books.bookcopy_find_by_id(copy_id)
    if copy is None:
        print("copy not found.")
    else:
        rack = int(print("enter new rack: "))
        books.bookcopy_change_rack(copy, rack)
    pass


def input_date(prompt):
    str = input(prompt + " (dd-mm-yyyy): ")
    day,month,year = map(int, str.split('-'))
    return date(year, month, day)


def librarian_area(user):
    while 1:
        clrscr()
        print("\n\n0. sign out\n1. edit profile\n2. change password\n3. find book by name\n4. check book availability\n5. add new book\n6. add new copy\n7. issue book copy\n8. return book copy\n9. list issued books\n10. edit book\n11. change rack\n12. add member\n13. take payment\n14. payment history\n15. list all users\n")
        choice = input("enter choice: ")
        if choice == '0':
            return
        elif choice == '1':
            edit_profile(user)
        elif choice == '2':
            change_password(user)
        elif choice == '3':
            find_books()
        elif choice == '4':
            copies_list = available_copies()
            for copy in copies_list:
                print(copy)
        elif choice == '5':
            add_book()
        elif choice == '6':
            add_book_copy()
        elif choice == '7':
            book_issue()
        elif choice == '8':
            book_return()
        elif choice == '9':
            list_issued_books()
        elif choice == '10':
            edit_book()
        elif choice == '11':
            change_rack()
        elif choice == '12':
            sign_up()
        elif choice == '13':
            take_payment()
        elif choice == '14':
            list_payment_history()
        elif choice == '15':
            find_all_users()
        else:
            print("invalid option.")


def owner_area(user):
    while 1:
        clrscr()
        print("\n\n0. sign out\n1. edit profile\n2. change password\n3. subjectwise copies report\n4. Bookwise copies report\n5. Fees/Fine report")
        choice = input("enter choice: ")
        if choice == '0':
            return
        elif choice == '1':
            edit_profile(user)
        elif choice == '2':
            change_password(user)
        elif choice == '3':
            reports.subjectwise_copies_chart()
        elif choice == '4':
            reports.bookwise_copies_chart()
        elif choice == '5':
            start = input_date("from date")
            end = input_date("to date")
            reports.daterange_fees_fine_chart(start, end)
        else:
            print("invalid option.")


def main():
    while 1:
        clrscr()
        print("\n\n0. exit\n1. sign in\n2. sign up")
        choice = input("enter choice: ")
        if choice == '0':
            return
        elif choice == '1':
            sign_in()
        elif choice == '2':
            sign_up()
        else:
            print("invalid option.")


main()


