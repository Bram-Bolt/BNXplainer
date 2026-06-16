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
        return False

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
    return True

    
    

# CONVERT SQLITE (.db) TO CSV FILE USING SHELL

def SqliteToCsv():
    subprocess.Popen('sqlite3 -header -csv feedback.db "select * from feedback;" > feedback.csv', shell=True)

# HELPER FUNCTION
def inputValidationDB(website_rating, 
        voi_q1, voi_q2, voi_q3,
        mpe_q1, mpe_q2, mpe_q3,
        scenario_q1, scenario_q2, scenario_q3, 
        feedback_text):
    """
    Check if all individuals and sets are either completely filled in
    or completely empty: 
    if voi_q1 has a value (int), voi_q2 and voi_q3 should also be an int
    if not filled it is np.nan (float) and thus all 3 should be float
    """
    is_invalid: bool = False
    voi_inputs = [voi_q1, voi_q2, voi_q3]
    mpe_inputs = [mpe_q1, mpe_q2, mpe_q3]
    scenario_inputs = [scenario_q1, scenario_q2, scenario_q3]

    if not isinstance(website_rating, int):
        print("Website rating not filled in")
        is_invalid =  True  # Invalid input
    
    if not all(isinstance(x, float) for x in voi_inputs):
        if not all(isinstance(x, int) for x in voi_inputs):
            is_invalid = True
            print("Not all VOI fields filled in")
            # not all fields are filled in
    if not all(isinstance(x, float) for x in mpe_inputs):
        if not all(isinstance(x, int) for x in mpe_inputs):
            is_invalid = True
            print("Not all MPE fields filled in")
            # not all fields are filled in
    if not all(isinstance(x, float) for x in scenario_inputs):
        if not all(isinstance(x, int) for x in scenario_inputs):
            is_invalid = True
            print("Not all Scenario fields filled in")
            # not all fields are filled in

    # Check if string
    if not isinstance(feedback_text,str):
        print("Invalid open comment string")
        is_invalid =  True  # Invalid input

    return is_invalid 

