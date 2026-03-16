import sqlite3
import subprocess



# ADD ENTRY TO FEEDBACK DATABASE SQLITE

def insertEntry(method_pref: int, exp1_rating: int, exp2_rating: int, exp3_rating:int, open_comment: str):
    """
    Insert values (int,int,int,int,str) into the SQLite database.
    """
    
    # input validation
    if(inputValidationDB(method_pref,exp1_rating,exp2_rating,exp3_rating,open_comment)): 
        return print("Invalid input")

    # SET CONNECTOR AND CURSOR FOR SQLITE
    con = sqlite3.connect("feedback.db")
    cur = con.cursor()

    # CREATE TABLE IF NOT EXISTS
    create_table = """CREATE TABLE IF NOT EXISTS 
    feedback(method_pref, exp1_rating, exp2_rating, exp3_rating, open_comment)
    """
    cur.execute(create_table)

    
    cur.execute("""INSERT INTO feedback VALUES(?,?,?,?,?)""",
                [method_pref,exp1_rating,exp2_rating,exp3_rating,open_comment])
    
    con.commit()
    

# CONVERT SQLITE (.db) TO CSV FILE USING SHELL

def SqliteToCsv():
    subprocess.Popen('sqlite3 -header -csv feedback.db "select * from feedback;" > feedback.csv', shell=True)




# HELPER FUNCTION
def inputValidationDB(m,e1,e2,e3,o):
    if(isinstance([m,e1,e2,e3],int)): pass
    else: return True

    if(isinstance(o,str)): return False
    else: return True

