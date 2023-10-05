import sqlite3
import json

from datetime import date

class database_handler:
    def __init__(self):
        self.connection = sqlite3.connect('userdata.db')
        self.cursor = self.connection.cursor()

    def include_id(self, user_id):
        self.cursor.execute(
            "SELECT user_id FROM users WHERE user_id = ?;", (user_id,)
        )

        row = self.cursor.fetchone()

        if row is None:
            self.cursor.execute(
                "INSERT INTO users (user_id) VALUES (?);", (user_id,)
            )
            self.connection.commit()

    def include_name(self, user_id: int, name: str) -> bool:
        self.cursor.execute(
            "SELECT name FROM users WHERE user_id = ?", (user_id,)
        )

        row = self.cursor.fetchone()

        if row[0] is None:
            self.cursor.execute(
                "UPDATE users SET name = ? WHERE user_id = ?;", (name, user_id)
            )
            self.connection.commit()
            return False
        else:
            return True

    def include_email(self, user_id: int, email: str) -> bool:
        self.cursor.execute(
            "SELECT email FROM users WHERE user_id = ?", (user_id,)
        )

        row = self.cursor.fetchone()

        if row[0] is None:
            self.cursor.execute(
                "UPDATE users SET email = ? WHERE user_id = ?;", (email, user_id)
            )
            self.connection.commit()
            return False
        else:
            return True
        
    def add_pay(self, id: str):
        self.cursor.execute("UPDATE users SET pay = TRUE WHERE user_id = ?", (id,))
        self.connection.commit()
        
    def include_phone(self, user_id: int, phone: str) -> bool:
        self.cursor.execute(
            "SELECT phone FROM users WHERE user_id = ?", (user_id,)
        )

        row = self.cursor.fetchone()

        if row[0] is None:
            self.cursor.execute(
                "UPDATE users SET phone = ? WHERE user_id = ?;", (phone, user_id)
            )
            self.connection.commit()
            return False
        else:
            return True
        
    def add_answer(self, user_id, answer, theme) -> None:
        self.cursor.execute(
            "INSERT INTO questions (user_id, theme, question) VALUES (?, ?, ?)", (user_id, answer, theme)
        )
        self.connection.commit()
        
    def set_admin_photo(self, photo_id: str):
        self.delete_admin_by_type(1)
        cursor = self.connection.cursor()
        cursor.execute("INSERT INTO admin (type, id) VALUES (?, ?)", (1, photo_id))
        self.connection.commit()

    def set_admin_video(self, video_id: str):
        self.delete_admin_by_type(2)
        cursor = self.connection.cursor()
        cursor.execute("INSERT INTO admin (type, id) VALUES (?, ?)", (2, video_id))
        self.connection.commit()

    def set_admin_voice(self, voice_id: str):
        self.delete_admin_by_type(3)
        cursor = self.connection.cursor()
        cursor.execute("INSERT INTO admin (type, id) VALUES (?, ?)", (3, voice_id))
        self.connection.commit()

    def set_admin_message(self, message: str):
        self.delete_admin_by_type(4)
        cursor = self.connection.cursor()
        cursor.execute("INSERT INTO admin (type, id) VALUES (?, ?)", (4, message))
        self.connection.commit()

    def delete_admin_by_type(self, type_id: int):
        cursor = self.connection.cursor()
        cursor.execute("DELETE FROM admin WHERE type = ?", (type_id,))
        self.connection.commit()

    def get_admin_content(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM admin")
        result = cursor.fetchall()
        content = []
        for row in result:
            content.append({
                'type': row[0],
                'id': row[1]
            })
        return content
    
    def get_all_id(self) -> list:
        cursor = self.connection.cursor()
        cursor.execute("SELECT user_id FROM users")
        res = cursor.fetchall()
        if res is None:
            return 0
        else:
            return res

    def get_all_photo(self) -> list:
        cursor = self.connection.cursor()
        cursor.execute("SELECT id FROM admin WHERE type = 1")
        res = cursor.fetchall()
        if res is None:
            return 0
        else:
            return res
        
    def get_all_video(self) -> list:
        cursor = self.connection.cursor()
        cursor.execute("SELECT id FROM admin WHERE type = 2")
        res = cursor.fetchall()
        if res is None:
            return 0
        else:
            return res
        
    def get_all_voice(self) -> list:
        cursor = self.connection.cursor()
        cursor.execute("SELECT id FROM admin WHERE type = 3")
        res = cursor.fetchall()
        if res is None:
            return 0
        else:
            return res
    
    def get_all_clients(self) -> int:
        cursor = self.connection.cursor()
        cursor.execute("SELECT COUNT(*) FROM users")
        res = cursor.fetchone()[0]
        if res is None:
            return 0
        else:
            return res

    def get_all_payers(self) -> int:
        cursor = self.connection.cursor()
        cursor.execute("SELECT COUNT(*) FROM users WHERE pay = 1")
        res = cursor.fetchone()[0]
        if res is None:
            return 0
        else:
            return res
        
    def get_all_users(self) -> list:
        cursor = self.connection.cursor()
        cursor.execute("SELECT user_id, name, phone, email FROM users")
        users = []

        for user in cursor.fetchall():
            users.append([user[0], user[1], user[2], user[3]])
            
        if users is None:
            return []
        else:
            return users
        
    def get_all_questions(self) -> list:
        cursor = self.connection.cursor()
        cursor.execute("SELECT questions.*, users.pay FROM users JOIN questions ON users.user_id = questions.user_id")
        result = cursor.fetchall()
        cursor.close()

        questions_with_pay = []
        for row in result:
            user_id = row[0]
            question = row[1]
            theme = row[2]
            pay = row[3]
            questions_with_pay.append([user_id, theme, question, pay])

        return questions_with_pay
    
    def add_current_date(self) -> int:
        try:
            with open('dates.json', 'r') as file:
                dates = json.load(file)
        except FileNotFoundError:
            dates = []

        current_date = date.today().isoformat()
        if current_date not in dates:
            dates.append(current_date)

        with open('dates.json', 'w') as file:
            json.dump(dates, file)

        return len(dates)

#Создание таблицы "users", если она не существует
# conn = sqlite3.connect('userdata.db')
# conn.execute('''CREATE TABLE IF NOT EXISTS admin(
#                 type INTEGER NOT NULL,
#                 id  TEXT NOT NULL)''')
# conn.execute('''CREATE TABLE IF NOT EXISTS users
#                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
#                 user_id TEXT UNIQUE,
#                 name TEXT,
#                 phone TEXT,
#                 email TEXT,
#                 theme TEXT,
#                 pay BOOLEAN DEFAULT FALSE)''')

# conn.execute('''CREATE TABLE IF NOT EXISTS questions
#                 (user_id TEXT,
#                 theme TEXT NOT NULL,
#                 question TEXT NOT NULL,
#                 FOREIGN KEY (user_id) REFERENCES users (user_id),
#                 FOREIGN KEY (theme) REFERENCES users (theme))''')

# conn.commit()