from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
import json

class menu_handler:
    def __init__(self):
        self.menu_file = 'menu_data.json'
        self.datas = self.load_menu_data()

        self.choose_yes = KeyboardButton("да")
        self.choose_no = KeyboardButton("нет")

        self.choose = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2).add(self.choose_yes, self.choose_no)

        self.menu_b  = KeyboardButton("Меню")
        self.menu_b2 = KeyboardButton("Отправить запрос на оплату")
        self.menu_button = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1).add(self.menu_b, self.menu_b2)

        self.admin_m1 = KeyboardButton("Добавить видео")
        self.admin_m2 = KeyboardButton("Добавить фото")
        self.admin_m3 = KeyboardButton("Добавить голосовое сообщение")
        self.admin_m4 = KeyboardButton("Добавить текстовое сообщение")
        self.admin_m5 = KeyboardButton("Выйти")

        self.admin_menu = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1).add(self.admin_m1, self.admin_m2, self.admin_m3, self.admin_m4, self.admin_m5)


        self.menu = InlineKeyboardMarkup(row_width=1)
        self.update_menu()

    def load_menu_data(self):
        try:
            with open(self.menu_file, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return [('вопрос1', 'qq_1')]

    def save_menu_data(self):
        with open(self.menu_file, 'w') as file:
            json.dump(self.datas, file)

    def update_menu(self):
        self.menu = InlineKeyboardMarkup(row_width=1)

        for data in self.datas:
            button = InlineKeyboardButton(text=data[0], callback_data=data[1])
            self.menu.add(button)

    def add_button(self, text: str):
        new_data = (text, f"qq_{len(self.datas) + 1}")
        self.datas.append(new_data)

        self.update_menu()

        self.save_menu_data()

    def delete_button(self, button_number: int):
        if int(button_number) < 1 or int(button_number) > len(self.datas):
            raise ValueError("Invalid button number")

        print("delete")
        del self.datas[button_number - 1]
        self.update_menu()
        self.save_menu_data()

    def add_mesaage(self, text: str):
        pass
        