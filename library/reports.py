#!/usr/bin/python3

# Author: Nilesh Ghule <nilesh@sunbeaminfo.com>
# library -> reports.py
# Date: 11/11/19

import db
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime

def subjectwise_copies_report():
    return db.subjectwise_copies()


def subjectwise_copies_chart():
    list = db.subjectwise_copies()
    subjects = []
    counts = []
    for data in list:
        print(data)
        subjects.append(data['subject'])
        counts.append(data['count'])
    plt.pie(counts, labels=subjects, startangle=0, autopct='%.1f%%')
    plt.title("Subjectwise BookCopies Count")
    plt.show()


def bookwise_copies_report():
    return db.bookwise_copies()


def bookwise_copies_chart():
    result = db.bookwise_copies()
    ids = []
    books = []
    counts = []
    available = []
    issued = []
    for data in result:
        print(data)
        ids.append(data['id'])
        books.append(data['name'])
        available.append(float(data['available']))
        issued.append(float(data['issued']))
        counts.append(float(data['count']))
    index = np.arange(len(books))
    ig = plt.bar(index, issued, 0.35)
    ag = plt.bar(index, available, 0.35, bottom=issued)
    plt.title("Bookwise Copies Count")
    plt.xticks(index, ids)
    plt.legend((ig[0], ag[0]), ('Issued', 'Available'))
    plt.xticks(rotation=75)
    plt.tight_layout()
    plt.show()


def daterange_fees_fine_collection_report(start=datetime.now(), end=datetime.now()):
    return db.daterange_fees_fine_collection(start, end)


def daterange_fees_fine_chart(start=datetime.now(), end=datetime.now()):
    list = db.daterange_fees_fine_collection(start, end)
    types = []
    amounts = []
    for data in list:
        print(data)
        types.append(data['type'])
        amounts.append(data['amount'])
    print(types)
    print(amounts)
    plt.pie(amounts, labels=types, startangle=0, autopct='%.1f%%')
    plt.title("Fees Fine Ratio in Date Range")
    plt.show()


def daily_collection_report(start=datetime.now(), end=datetime.now()):
    return db.daily_collection(start, end)


def monthly_collection_report(start=datetime.now(), end=datetime.now()):
    return db.monthly_collection(start, end)


