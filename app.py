import sqlite3
from sqlite3 import Error  

def openConnection(_dbFile):
    conn = None
    try:
        conn = sqlite3.connect(_dbFile)
    except Error as e:
        print(e)

    return conn

def closeConnection(_conn, _dbFile):
    try:
        _conn.close()
    except Error as e:
        print(e)

def login(_conn):
    print("Choose an Existing Profile")
    try:   
        sql = """SELECT userName FROM Users"""
        cur = _conn.cursor()
        cur.execute(sql)

        p = '{:>10}'.format("Users")
        print(p)
        print("-------------------------------")

        rows = cur.fetchall()
        for row in rows:
            p = '{:>10}'.format(row[0])
            print(p)
        print("-------------------------------")
        check = True
        while check:
            user = input("Enter User Name: ")
            sql = """SELECT userName, userID FROM Users WHERE userName = ?"""
            args = [user]
            cur = _conn.cursor()
            cur.execute(sql, args)
            rows = cur.fetchall()
            spell_check = 0
            for row in rows:
                if user == row[0]:
                    p = '{:>10} {:>10}'.format(row[0], row[1])
                    user_name = row[0]
                    user_id = row[1]
                    print(p)
                    spell_check = 1
                    check = False
            if spell_check == 0:
                print("Incorrect User OR User does not exist")

        loginInterface(user_name, user_id, _conn)
        

    except Error as e:
        print(e)

def loginInterface(name, id, _conn):
    while True:
        print("\nWELCOME %s to your Film Organizer" % (name))
        print("1. Watch Later")
        print("2. Owned Films")
        print("3. Streaming Platform")
        print("4. Log Out")

        num = input("Enter desired number here: ")

        if num == "1":
            print("hi")
        elif num == "2":
            print("hi")

        elif num == "3":
            print("hi")
        elif num == "4":
            print("bye")
        
        else:
            print("Invalid Input: Please select a desired action with the appropriate number")

def main():
    database = r"film.sqlite"

    # create a database connection
    conn = openConnection(database)
    
    while True:
        print("\nMOVIE ORGANIZER: ")
        print("1. Login Profile")
        print("2. Create Profile")
        print("3. End Session")

        num = input("Enter desired number here: ")

        if num == "1":
            print("hi")
            login(conn)
        elif num == "2":
            print("hi")

        elif num == "3":
            break
        
        else:
            print("Invalid Input: Please select a desired action with the appropriate number")

    closeConnection(conn, database)

if __name__ == "__main__":
    main()