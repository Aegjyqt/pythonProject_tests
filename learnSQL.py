import sqlite3

db = sqlite3.connect('mydb')

cursor = db.cursor()

try:
    cursor.execute('''
    CREATE TABLE users(id INTEGER PRIMARY KEY, name TEXT,
    phone TEXT, email TEXT unique, password TEXT)
    ''')
    db.commit()
except sqlite3.OperationalError:
    pass

name1 = "Fyodor"
phone1 = "1234567"
email1 = "some_email@smth.com"
password1 = "der password"

name2 = "Senya"
phone2 = "2345678"
email2 = "another_email@smth.com"
password2 = "der parol"

more_users = [(name1, phone1, email1, password1), (name2, phone2, email2, password2)]

#cursor.executemany('''INSERT INTO users(name, phone, email,password) VALUES(?,?,?,?)''', more_users)

db.commit()

cursor.execute('''SELECT name, email, phone, password FROM users''')

all_rows = cursor.fetchall()
print(all_rows[0][1])

for row in all_rows:
    print('{0} : {1}, {2}'.format(row[0], row[1], row[2]))


newphone = '3113093164'
userid = 2
cursor.execute('''UPDATE users SET phone = ? WHERE id = ? ''',
(newphone, userid))


user_id = 2
cursor.execute('''SELECT name, phone, email, password FROM users WHERE id=?''', (user_id,))
user = cursor.fetchone()

print(user)


db.close()