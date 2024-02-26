from collections import UserDict
from datetime import datetime, timedelta

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    # реалізація класу
		pass

class Phone(Field):
    def __init__(self, value):
        # Перевірка, чи довжина номеру телефону дорівнює 10
        if len(value) == 10:
            super().__init__(value)
        else:
            raise Exception("Phone number must be equal to 10") # Викидаємо виняток, якщо номер не має 10 символів
        
class Birthday(Field):
    def __init__(self, value):
        try:
            # Додайте перевірку коректності даних
            # та перетворіть рядок на об'єкт datetime
            datatime_object = datetime.strptime(value, "%d.%m.%Y").date()
            if datetime.now().date() > datatime_object:
                super().__init__(datatime_object)
            else:
                raise Exception("Invalid date of birthday")  
        except ValueError:
            raise Exception("Invalid date format. Use DD.MM.YYYY")

    # Приводимо дату до стрінгу
    def __str__(self):
        return self.value.strftime("%d.%m.%Y")

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    # Додаємо день народження 
    def add_birthday(self, birthday: str):
        self.birthday = Birthday(birthday)

    # Додаємо телефон до списку
    def add_phone(self, phone: str):
        self.phones.append(Phone(phone))

    # Видаляємо телефон зі списку, якщо він співпадає з переданим значенням
    def remove_phone(self, rem_phone: str):
        self.phones = [phone for phone in self.phones if str(phone) != rem_phone]

    # Замінюємо старий номер на новий, якщо він співпадає з переданим значенням
    def edit_phone(self, old_phone, new_phone):
        self.phones = [phone if str(phone) != old_phone else Phone(new_phone) for phone in self.phones]
    
    # Пошук телефону у списку
    def find_phone(self, f_phone):
        for phone in self.phones:
            if str(phone) == f_phone:
                return phone

    def __str__(self):
        if not self.birthday: # Вивід контакту без дня народження
            return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"
        else: # Вивід контакту з днем народження
            return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}, birthday: {self.birthday}"

class AddressBook(UserDict):

    # Додаємо запис у телефонну книгу
    def add_record(self, record):
        self.data[record.name] = record
    
    # Пошук запису по імені
    def find(self, name) -> Record|None:
        for key in self.data.keys():
            if str(key) == name:
                return self.data[key]
        return None

    # Видаляємо запис з телефонної книги по імені
    def delete(self, name) -> Record|None:
        for key in self.data.keys():
            if str(key.value) == name:
                return self.data.pop(key)
        return None
            
    def get_upcoming_birthdays(self):
        # Отримуємо поточну дату
        today = datetime.today().date()

        # Створюємо порожній список для зберігання інформації про майбутні дні народження
        upcoming_birthdays = []

        for name, record in self.data.items():
            
            if  record.birthday:

                upcoming_birthday = dict()

                # Змінює рік на поточний
                birthday_this_year = record.birthday.value.replace(year = today.year)
                
                # Перевіряємо, чи минув день народження в цьому році
                if birthday_this_year < today:
                    # Якщо так, розглядаємо дату наступного року
                    birthday_this_year = birthday_this_year.replace(year = today.year + 1)
                
                # Визначаємо різницю в днях між сьогоднішньою датою і датою народження
                difference = birthday_this_year.toordinal() - today.toordinal()
                if difference < 7: # Перевіряємо чи день народження буде протягом наступних 7 днів
                    # Переносимо день народження, якщо випадає на вихідні
                    if birthday_this_year.weekday() == 5:
                        birthday_this_year += timedelta(days=2)
                    if birthday_this_year.weekday() == 6:
                        birthday_this_year += timedelta(days=1)

                    # Додаємо словник до списку
                    upcoming_birthday[str(name)] = birthday_this_year.strftime("%d.%m.%Y")
                    upcoming_birthdays.append(upcoming_birthday)
            
        return upcoming_birthdays
    
if __name__ == "__main__":
    # Створення нової адресної книги
    book = AddressBook()

    # Створення запису для John
    john_record = Record("John")
    john_record.add_phone("1234567890")
    john_record.add_phone("5555555555")
    john_record.add_birthday('24.02.1975')
    # Додавання запису John до адресної книги
    book.add_record(john_record)

    # Створення та додавання нового запису для Jane
    jane_record = Record("Jane")
    jane_record.add_phone("9876543210")
    jane_record.add_phone("1111111111")
    print(jane_record)
    # Видалення телефону
    jane_record.remove_phone("1111111111")
    print('-' * 20)
    print(jane_record)
    book.add_record(jane_record)

    # Виведення всіх записів у книзі
    print('-' * 20)
    for name, record in book.data.items():
        print(record)

    # Знаходження та редагування телефону для John
    john = book.find("John")
    john.edit_phone("1234567890", "1112223333")

    print('-' * 20)
    print(john)  # Виведення: Contact name: John, phones: 1112223333; 5555555555

    # Пошук конкретного телефону у записі John
    found_phone = john.find_phone("5555555555")
    print('-' * 20)
    print(f"{john.name}: {found_phone}")  # Виведення: 5555555555

    print('-' * 20)
    print(book.get_upcoming_birthdays())
    # Видалення запису Jane
    book.delete("Jane")
    print('-' * 20)
    for name, record in book.data.items():
        print(record)   