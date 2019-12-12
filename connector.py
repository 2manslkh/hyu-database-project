import mysql.connector
import csv
import saved_queries as sqlq
from random import choice
from random import seed
import time

seed(time.time())


cnx = mysql.connector.connect(user='root', password='1234',
                              host='127.0.0.1',
                              port=3306,
                              database='telegrambot')

cursor = cnx.cursor(buffered=True)

def add_user(telegram_id):
    cursor.execute(sqlq.INSERT_NEW_USER.format(telegram_id=telegram_id))
    cnx.commit()

def get_last_hint_time(telegram_id):
    'get last time hint was given'
    cursor.execute(sqlq.QUERY_LAST_HINT_TIME.format(telegram_id=telegram_id))
    last_hint_time = cursor.fetchall()[0][0]
    return last_hint_time

def get_current_users():
    cursor.execute(sqlq.QUERY_CURRENT_USERS)
    current_users = [x[0] for x in cursor.fetchall()]
    return current_users

def get_current_users_student_id():
    cursor.execute(sqlq.QUERY_CURRENT_USERS_STUDENT_ID)
    current_users_student_id = [x[0] for x in cursor.fetchall()]
    return current_users_student_id

def insert_new_user(telegram_id):
    cursor.execute(sqlq.INSERT_NEW_USER.format(telegram_id=telegram_id))
    cnx.commit()

def update_student_id(telegram_id, student_id):
    cursor.execute(sqlq.UPDATE_STUDENT_ID.format(telegram_id=telegram_id,student_id=student_id))
    cnx.commit()

def update_last_hint_time(telegram_id,last_hint_time):
    cursor.execute(sqlq.UPDATE_LAST_HINT_TIME.format(telegram_id=telegram_id,last_hint_time=last_hint_time))
    cnx.commit()

def get_hint(telegram_id):
    '''Retrieves a hint from the hint table
    Returns with a hint description
    '''
    # Get hint_part, if hint_part = -1 or 4, 
    cursor.execute(sqlq.QUERY_HINT_PART.format(telegram_id=telegram_id))
    hint_part = cursor.fetchall()[0][0]
    print(hint_part)
    if hint_part == -1 or hint_part == 4:

        # Get list of unsolved hint and Assign random hint_id
        cursor.execute(sqlq.QUERY_UNSOLVED_HINT_ID)
        unsolved_hints = cursor.fetchall()
        selection = choice(unsolved_hints)[0]
        print(selection)
        cursor.execute(sqlq.ASSIGN_HINT_ID.format(telegram_id=telegram_id,hint_id=selection))
        
        # Set hint_part = 1
        cursor.execute(sqlq.SET_HINT_PART.format(telegram_id=telegram_id,hint_part=1))
        cnx.commit()

    # Get hint_part
    cursor.execute(sqlq.QUERY_HINT_PART.format(telegram_id=telegram_id))
    hint_part = cursor.fetchall()[0][0]
    print(hint_part)
    
    # Get hint_id
    cursor.execute(sqlq.QUERY_HINT_ID.format(telegram_id=telegram_id))
    hint_id = cursor.fetchall()[0][0]
    print(hint_id)

    # Get hint_description
    cursor.execute(sqlq.QUERY_HINT_DESCRIPTION.format(hint_id=hint_id,hint_part=hint_part))
    hint_description = cursor.fetchall()[0][0]

    # Increment hint_id by 1
    cursor.execute(sqlq.SET_HINT_PART.format(telegram_id=telegram_id,hint_part=hint_part+1))
    cnx.commit()

    return hint_description

def get_unclaimed_hints():
    'return list of unclaimed token_id'
    cursor.execute(sqlq.QUERY_UNSOLVED_TOKEN_ID)
    result = [x[0] for x in cursor.fetchall()]
    return result

def get_unclaimed_users():
    'return list of telegram_id of users that have not claimed a prize'
    cursor.execute(sqlq.QUERY_UNCLAIMED_USERS)
    result = [x[0] for x in cursor.fetchall()]
    return result

def get_all_tokenid():
    cursor.execute(sqlq.QUERY_ALL_HINTS)
    result = [x[0] for x in cursor.fetchall()]
    return result

def claim_token(telegram_id,token_id):
    "set claimed = 1 for token and user involved"
    cursor.execute(sqlq.SET_USER_CLAIMED.format(telegram_id=telegram_id))
    cursor.execute(sqlq.SET_HINT_CLAIMED.format(token_id=token_id))
    cnx.commit()

def add_hints(cursor):
    ''' add hints from csv file '''
    with open('testdata.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for i,line in enumerate(csv_reader):
            if i > 0: # Ignore headers
                hint1 = line[3]
                hint2 = line[4]
                hint3 = line[5]
                hints = [hint1,hint2,hint3]
                cursor.execute(f"INSERT INTO hints(description_1,description_2,description_3) VALUES(test1,test2,test3)")
                print("added")