import sqlite3

conn = sqlite3.connect('test.db')
print("Opened database successfully")


def main():

    #create_table()
    #insert_records()
    execute_select()
    #execute_update()
    #delete_statement()


def delete_statement():
    conn.execute("DELETE from COMPANY where ID = 2;")
    conn.commit()
    print("Total number of rows deleted :" + str(conn.total_changes))

    cursor = conn.execute("SELECT id, name, address, salary from COMPANY")
    for row in cursor:
        print("ID = " + str(row[0]))
        print("NAME = " + str(row[1]))
        print("ADDRESS = " + str(row[2]))
        print("SALARY = " + str(row[3]) + "\n")

    print("Operation done successfully")


def execute_update():
    conn.execute("UPDATE COMPANY set SALARY = 25000.00 where ID = 1")
    conn.commit()
    print("Total number of rows updated :" + str(conn.total_changes))

    cursor = conn.execute("SELECT id, name, address, salary from COMPANY")
    for row in cursor:
        print("ID = " + str(row[0]))
        print("NAME = " + str(row[1]))
        print("ADDRESS = " + str(row[2]))
        print("SALARY = " + str(row[3]) + "\n")

    print("Operation done successfully")

    

def execute_select():

    cursor = conn.execute("SELECT id, name, address, salary from COMPANY")
    for row in cursor:
        print("ID = " + str(row[0]))
        print("NAME = " + str(row[1]))
        print("ADDRESS = " + str(row[2]))
        print("SALARY = " + str(row[3]) + "\n")

    print("Operation done successfully")


def insert_records():

    paul = "Paul"
    age = 32
    city = "California"
    salary = 20000.00

    conn.execute(f"INSERT INTO COMPANY (ID,NAME,AGE,ADDRESS,SALARY) \
          VALUES (9, '{paul}', {age}, '{city}', {salary} );")

    conn.execute("INSERT INTO COMPANY (ID,NAME,AGE,ADDRESS,SALARY) \
          VALUES (10, 'Allen', 25, 'Texas', 15000.00 );")

    conn.execute("INSERT INTO COMPANY (ID,NAME,AGE,ADDRESS,SALARY) \
          VALUES (11, 'Teddy', 23, 'Norway', 20000.00 );")

    conn.execute("INSERT INTO COMPANY (ID,NAME,AGE,ADDRESS,SALARY) \
          VALUES (12, 'Mark', 25, 'Rich-Mond ', 65000.00 );")

    conn.commit()
    print("Records created successfully")


def create_table():

    conn.execute('''CREATE TABLE COMPANY
             (ID INT PRIMARY KEY     NOT NULL,
             NAME           TEXT    NOT NULL,
             AGE            INT     NOT NULL,
             ADDRESS        CHAR(50),
             SALARY         REAL);''')
    print("Table created successfully")

if __name__ == '__main__':

    main()


conn.close()