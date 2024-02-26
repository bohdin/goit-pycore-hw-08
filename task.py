from AddressBook import AddressBook, Record
import pickle

def save_data(book, filename="addressbook.pkl"):
    with open(filename, "wb") as f:
        pickle.dump(book, f)

def load_data(filename="addressbook.pkl"):
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook()  # Повернення нової адресної книги, якщо файл не знайдено

def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Give me name and phone please."
        except KeyError:
            return "Contact doesn't exists."
        except IndexError:
            return "Invalid contact."
        except Exception as e:
            return e
        
    return inner

def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args

@input_error
def add_contact(args, book: AddressBook) -> str:
    # Розбиваємо список
    name, phone = args
    # Робим щоб імена починалися з великої літери
    name = name.capitalize()
    # Якщо такою людини ще немає в словнику додаємо
    if name not in  book.data.keys():        
        record = Record(name)
        record.add_phone(phone)
        book.add_record(record)
        return "Contact added."
    else:
        return "Contact already exists." # В іншому випадку виводимо, що вже контакт існує

@input_error
def change_contact(args, book: AddressBook):
    
    #  Розбиваємо список
    name, phone = args
    # Робим щоб імена починалися з великої літери
    name = name.capitalize()
    # Видаляємо запис
    record = book.delete(name)
    # Міняємо номер телефону і заново додаємо запис
    if record:
        record.edit_phone(str(record.phones[0].value), phone)
        book.add_record(record)        
        return "Contact change."
    else:
        raise(KeyError)

@input_error
def show_phone(args, book: AddressBook):  
    # Приводимо ім'я до потрібної нам форми
    name = args[0].capitalize()
    # Знаходити запис про людину
    record = book.find(name)
    # Якщо така людина є, виводимо номер телефону
    if record:
        return str(record.phones[0])
    else:
        raise(KeyError)
    

@input_error
def show_all(book: AddressBook):
    # Якщо словник не пустий, виводимо контакти через enter
    if book.data:
        return "\n".join(str(record) for _, record in book.data.items())
    else:
        return "No contacts."
    
@input_error
def add_birthday(args, book: AddressBook):
    # Розбиваємо список
    name, birthday = args
    # Робим щоб імена починалися з великої літери
    name = name.capitalize()
    record = book.delete(name)
    # Якщо така людина є, додаємо день народження
    if record:        
        record.add_birthday(birthday)
        book.add_record(record)
        return "Birthday added."
    else:
        raise(KeyError)

@input_error
def show_birthday(args, book: AddressBook):
    # Приводимо ім'я до потрібної нам форми
    name = args[0].capitalize()
    # Шукаємо потрібний запис
    record = book.find(name)
    # Якщо запис знайшли
    if record:
        birthday = record.birthday 
        return str(birthday) if birthday else "Contact don't have birthday"
    else:
        raise(KeyError)

@input_error
def birthdays(args, book: AddressBook):
    birthdays_list = book.get_upcoming_birthdays()
    return "\n".join(str(record) for record in birthdays_list)

    
def main():
    book = load_data()
    print("Welcome to the assistant bot!")
    
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            save_data(book)
            print("Good bye!")
            break
        
        elif command == "hello":
            print("How can I help you?")

        elif command == "add":
            print(add_contact(args, book))

        elif command == "change":
            print(change_contact(args, book))

        elif command == "phone":
            print(show_phone(args, book))

        elif command == "all":
            print(show_all(book))

        elif command == "add-birthday":
            print(add_birthday(args, book))

        elif command == "show-birthday":
            print(show_birthday(args, book))

        elif command == "birthdays":
            print(birthdays(args, book))

        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()
