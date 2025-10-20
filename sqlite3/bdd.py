import sqlite3

con = sqlite3.connect("data_form.db")
cur = con.cursor()

cur.execute('''CREATE TABLE IF NOT EXISTS data_form
             (user_id TEXT, use_case TEXT)''')
con.commit()