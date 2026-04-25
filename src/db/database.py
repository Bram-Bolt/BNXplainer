import sqlite3
import subprocess



# ADD ENTRY TO FEEDBACK DATABASE SQLITE

def insertEntry(website_rating, 
        voi_q1, voi_q2, voi_q3,
        mpe_q1, mpe_q2, mpe_q3,
        scenario_q1, scenario_q2, scenario_q3, 
        feedback_text):
    """
    Insert values (10 ints, 1 str) into the SQLite database.
    """
    
    # input validation
    if(inputValidationDB(website_rating, 
        voi_q1, voi_q2, voi_q3,
        mpe_q1, mpe_q2, mpe_q3,
        scenario_q1, scenario_q2, scenario_q3, 
        feedback_text)): 
        return print("Invalid input")

    # SET CONNECTOR AND CURSOR FOR SQLITE
    con = sqlite3.connect("src/db/feedback.db")
    cur = con.cursor()

    # CREATE TABLE IF NOT EXISTS
    create_table = """CREATE TABLE IF NOT EXISTS 
    feedback(website_rating, 
        voi_q1, voi_q2, voi_q3,
        mpe_q1, mpe_q2, mpe_q3,
        scenario_q1, scenario_q2, scenario_q3, 
        feedback_text)
    """
    cur.execute(create_table)

    
    cur.execute("""INSERT INTO feedback VALUES(?,?,?,?,?,?,?,?,?,?,?)""",
                [website_rating, 
                voi_q1, voi_q2, voi_q3,
                mpe_q1, mpe_q2, mpe_q3,
                scenario_q1, scenario_q2, scenario_q3, 
                feedback_text])
    
    con.commit()
    

# CONVERT SQLITE (.db) TO CSV FILE USING SHELL

def SqliteToCsv():
    subprocess.Popen('sqlite3 -header -csv feedback.db "select * from feedback;" > feedback.csv', shell=True)

# HELPER FUNCTION
def inputValidationDB(website_rating, 
        voi_q1, voi_q2, voi_q3,
        mpe_q1, mpe_q2, mpe_q3,
        scenario_q1, scenario_q2, scenario_q3, 
        feedback_text):
    # Check if all ints
    if not all(isinstance(x, int) for x in [website_rating, 
        voi_q1, voi_q2, voi_q3,
        mpe_q1, mpe_q2, mpe_q3,
        scenario_q1, scenario_q2, scenario_q3]):
        print("Invalid integer")
        return True  # Invalid input

    # Check if string
    if not isinstance(feedback_text,str):
        print("Invalid string")
        return True  # Invalid input

    return False 

