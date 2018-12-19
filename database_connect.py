#coding=utf-8

import pymysql
from database_account import account 
from database_account import password
# import datbase_account

def insert_data(s, c, u, p, n, f, sol):
#connect to database

    db = pymysql.connect("localhost", account, password, "chatbot")
    cursor = db.cursor()
    sql = """INSERT INTO chatbot(subject,
        class, url, path, name, finish, solution)
        VALUES('%s', '%s', '%s', '%s', '%s','%s','%s')""" %(s,c,u,p,n,f,sol)



    try:
        #Execute the SQL command
        cursor.execute(sql)
        print('Yes, Insert Successful')
        # Commit the changes in the database
        db.commit()
    except:
        db.rollback()

    print(sql)
    db.close()



def read_question(text):

    db = pymysql.connect("localhost", account, password, "chatbot")
    cursor = db.cursor()
    sql = "SELECT * FROM chatbot \
    WHERE class = '%s'" %(text)
    print(sql)
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        print(results)
        question = []
        # i = 0
        for row in results:
            question.append(row[2])
            print("nono")
        db.commit()

    except:
        print("Error")
        db.rollback()    

    db.close()
    return question

def read_solution(text):

    db = pymysql.connect("localhost", account, password, "chatbot")
    cursor = db.cursor()
    sql = "SELECT * FROM chatbot \
    WHERE url = '%s'" %(text)
    print(sql)
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        print(results)
        # i = 0
        for row in results:
            sol = row[6]
            print("nono")
        db.commit()

    except:
        print("Error")
        db.rollback()    

    db.close()
    return sol

def update_solution(que,url):
    db = pymysql.connect("localhost", account, password, "chatbot")
    cursor = db.cursor()
    sql = """UPDATE chatbot set solution = '%s' where name = '%s'""" %(url, que)
    print(sql)
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        print(results)
        db.commit()

    except:
        print("Error")
        db.rollback()    

    db.close()

def update_finish(que,bit):
    db = pymysql.connect("localhost", account, password, "chatbot")
    cursor = db.cursor()
    sql = """UPDATE chatbot set finish = '%s' where name = '%s'""" %(bit, que)
    print(sql)
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        print(results)
        db.commit()

    except:
        print("Error")
        db.rollback()    

    db.close()
