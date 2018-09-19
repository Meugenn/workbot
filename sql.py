import sqlite3



def add_word(group_id, word):
    db = sqlite3.connect("db.db")
    cur = db.cursor()
    cur.execute(f"INSERT INTO condition (group_id, word) VALUES ('{group_id}','{word}');")
    db.commit()
    db.close()
