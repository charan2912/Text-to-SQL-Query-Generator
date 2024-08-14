import sqlite3

connection=sqlite3.connect("student.db")



cursor=connection.cursor()

table_info="""
Create table STUDENT(NAME VARCHAR(25),CLASS VARCHAR(25),SECTION VARCHAR(25),
    MARKS INT);

"""
cursor.execute(table_info)

cursor.execute('''Insert into STUDENT values('charan','genai','A',60)''')
cursor.execute('''Insert into STUDENT values('Geetha','genai','A',70)''')
cursor.execute('''Insert into STUDENT values('Bicchi','DL','B',80)''')
cursor.execute('''Insert into STUDENT values('Vengala','genai','B',90)''')
cursor.execute('''Insert into STUDENT values('Kiran','DL','A',100)''')

print("The Inserted Redords are")
data=cursor.execute('''Select * from STUDENT''')
for row in data:
    print(row)
    
    
connection.commit()
connection.close()