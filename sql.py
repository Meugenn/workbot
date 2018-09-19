import sqlite3



def add_user(chat_id):
    db = sqlite3.connect("db.db")
    cur = db.cursor()
    if get_cond(chat_id) != None:
        change_cond(chat_id, 'start')
    else:
        cur.execute(f"INSERT INTO cond (user_id, condition) VALUES ({chat_id},'start');")
    db.commit()
    db.close()

def change_cond(chat_id, condition):
    db = sqlite3.connect("db.db")
    cur = db.cursor()
    cur.execute(f'''UPDATE cond
    SET condition= '{condition}'
    WHERE user_id = {chat_id};''')
    db.commit()
    db.close()

def get_cond(user_id):
    db = sqlite3.connect("db.db")
    cur = db.cursor()
    a = cur.execute(f'''
    SELECT condition 
    FROM cond
    WHERE user_id = {user_id}
    ;''').fetchone()
    db.commit()
    db.close()
    if a is not None:
        a = a[0]
    return a

if __name__ == '__main__':
    add_user(123)
    print(get_cond(123))
    change_cond(123, 3)
    print(get_cond(123))
