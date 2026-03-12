import sqlite3

con = sqlite3.connect("feedback.db")
cur = con.cursor()

# CREATE TABLE
create_table = """CREATE TABLE IF NOT EXISTS 
feedback(method_pref, exp1_rating, exp2_rating, exp3_rating, open_comment)
"""
cur.execute(create_table)