import  sqlite3


DB_NAME = 'shop.db'

def create_table():
    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS items (id INTEGER PRIMARY KEY AUTOINCREMENT,name TEXT,description TEXT)''')
    conn.commit()
    conn.close()

def add_item():
    name = input('Введите название: ')
    description = input('Введите описание: ')
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO items (name, description) VALUES (?, ?)", (name, description))
    conn.commit()
    conn.close()
    print("Элмент добавлен")

def get_item():

    try:
        item_id = int(input("Введите ID для поиска:"))
    except ValueError:
        print("ID должен быть числом")
        return

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM items WHERE id = ?", (item_id,))

    result = cursor.fetchone()
    conn.close()

    if result:
        print(f"ID: {result[0]}, Название: {result[1]}, Описание: {result[2]}")
    else:
        print("Элемент не найден.")

def update_item():
    try:
        item_id = int(input("Введите ID для изменения:"))
    except ValueError:
        print("ID должен быть числом")
        return

    name = input("Введите новое название:")
    description = input("Введите новое описание:")

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("UPDATE items SET name = ?, description = ? WHERE id = ?", (name, description ,item_id))

    conn.commit()
    conn.close()

    if cursor.rowcount > 0:
        print("Элемент обновлен.")
    else:
        print("Элемент не найден.")

def delete_item():
    try:
        item_id = int(input("Введите ID для удаления:"))
    except ValueError:
        print("ID должен быть числом")
        return
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("DELETE FROM items WHERE id = ?", (item_id,))

    conn.commit()
    conn.close()

    if cursor.rowcount > 0:
        print("Элемент удален.")
    else:
        print("Элемент не найден.")

def main():
    create_table()

    while True:
        print("\n1. Добавить")
        print("2. Найти")
        print("3. Изменить")
        print("4. Удалять")
        print("5. Выход")

        choice = input("Выберите команду:")

        if choice == "1":
            add_item()
        elif choice == "2":
            get_item()
        elif choice == "3":
            update_item()
        elif choice == "4":
            delete_item()
        elif choice == "5":
            break
        else:
            print("Неверная команда")


if __name__ == "__main__":
    main()