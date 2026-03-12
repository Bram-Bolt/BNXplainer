import sqlite3

con = sqlite3.connect("feedback.db")
cur = con.cursor()

# CREATE TABLE
create_table = """CREATE TABLE IF NOT EXISTS 
feedback(method_pref, exp1_rating, exp2_rating, exp3_rating, open_comment)
"""
cur.execute(create_table)


# ADD ENTRY TO FEEDBACK DATABASE SQLITE

def insertEntry(method_pref: int, exp1_rating: int, exp2_rating: int, exp3_rating:int, open_comment: str):
    """
    Insert values (int,int,int,int,str) into the SQLite database.
    """
    cur.execute("""INSERT INTO feedback VALUES(?,?,?,?,?)""",
                [method_pref,exp1_rating,exp2_rating,exp3_rating,open_comment])
    
    con.commit()
    

def insertEntryList(feedback_list):
    """
    Insert list of 5 values (int,int,int,int,str) into the SQLite database.
    """
    cur.execute("""INSERT INTO feedback VALUES(?,?,?,?,?)""",feedback_list)
    
    con.commit()



# EXAMPLE USE
#
# insertEntry(2,3,4,4,"This is great!")
# 


# TESTING

# res = cur.execute("SELECT open_comment FROM feedback")
# print(res.fetchall())
