import psycopg2
import csv

conn = psycopg2.connect(
    dbname="rake",
    user="postgres",
    password="2005",  
    host="localhost",
    port="5432"
)
cur = conn.cursor()

# Кесте құру
cur.execute("""
    CREATE TABLE IF NOT EXISTS phonebook (
        id SERIAL PRIMARY KEY,
        name VARCHAR(50),
        phone VARCHAR(20)
    );
""")
conn.commit()

# CSV-тен жүктеу
def load_from_csv():
    with open('psycopg2.csv', 'r') as f:
        reader = csv.reader(f)
        next(reader)
        count_added = 0
        count_skipped = 0
        for row in reader:
            if len(row) >= 2:
                name, phone = row[0], row[1]
                
                # Тексеру: осындай name және phone бар ма?
                cur.execute("SELECT * FROM phonebook WHERE name = %s AND phone = %s", (name, phone))
                if cur.fetchone():
                    print(f"⚠️  '{name}' нөмірі бар жазба бұрыннан бар. Өткізіліп кетті.")
                    count_skipped += 1
                else:
                    cur.execute("INSERT INTO phonebook (name, phone) VALUES (%s, %s)", (name, phone))
                    count_added += 1
        conn.commit()
        print(f"\n✅ CSV жүктелді: {count_added} жаңа дерек, {count_skipped} өткізіліп кетті.")

# Қолмен енгізу
def insert_manually():
    name = input("Атың: ")
    phone = input("Нөмірің: ")

    # Нөмірдің қайталануы тексеріледі
    cur.execute("SELECT * FROM phonebook WHERE phone = %s", (phone,))
    if cur.fetchone():
        print(f"⚠️  '{phone}' нөмірі бұрыннан бар. Қайтадан нөмір енгізіңіз.")
    else:
        cur.execute("INSERT INTO phonebook (name, phone) VALUES (%s, %s)", (name, phone))
        conn.commit()
        print("✅ Дерек қосылды!")

# Жаңарту
def update_entry():
    name = input("Қай есімді өзгертеміз (ағымдағы аты): ")
    
    cur.execute("SELECT * FROM phonebook WHERE name = %s", (name,))
    result = cur.fetchone()
    
    if result:
        print("\nҚандай деректі өзгертесіз?")
        print("1. Атын")
        print("2. Нөмірін")
        print("3. Екеуін де")
        choice = input("Таңдаңыз (1-3): ")

        if choice == "1":
            new_name = input("Жаңа аты: ")
            cur.execute("UPDATE phonebook SET name = %s WHERE name = %s", (new_name, name))
            conn.commit()
            print("✅ Аты жаңартылды!")

        elif choice == "2":
            new_phone = input("Жаңа нөмірі: ")
            cur.execute("UPDATE phonebook SET phone = %s WHERE name = %s", (new_phone, name))
            conn.commit()
            print("✅ Нөмірі жаңартылды!")

        elif choice == "3":
            new_name = input("Жаңа аты: ")
            new_phone = input("Жаңа нөмірі: ")
            cur.execute("UPDATE phonebook SET name = %s, phone = %s WHERE name = %s", (new_name, new_phone, name))
            conn.commit()
            print("✅ Аты мен нөмірі жаңартылды!")

        else:
            print("⚠️ Қате таңдау! Мәзірден тек 1, 2 немесе 3 таңдаңыз.")
    else:
        print("⚠️ Ондай есімді адам жоқ.")

# Іздеу
def query_data():
    filter_name = input("Аты бойынша іздеу: ")
    cur.execute("SELECT * FROM phonebook WHERE name ILIKE %s", ('%' + filter_name + '%',))
    results = cur.fetchall()
    
    if results:
        for row in results:
            print(row)
    else:
        print("Ондай есімді адам жоқ.")


# Өшіру және ID қайта нөмірлеу 
def delete_entry():
    print("\n🔍 Қалай өшіресіз?")
    print("1. Аты арқылы")
    print("2. Нөмірі арқылы")
    choice = input("Таңдау (1-2): ")

    if choice == "1":
        identifier = input("Кімді өшіресіз (аты): ")
        cur.execute("SELECT * FROM phonebook WHERE name = %s", (identifier,))
    elif choice == "2":
        identifier = input("Қай нөмірді өшіресіз: ")
        cur.execute("SELECT * FROM phonebook WHERE phone = %s", (identifier,))
    else:
        print("⚠️ Қате таңдау!")
        return

    result = cur.fetchone()

    if result:
        if choice == "1":
            cur.execute("DELETE FROM phonebook WHERE name = %s", (identifier,))
        else:
            cur.execute("DELETE FROM phonebook WHERE phone = %s", (identifier,))
        conn.commit()
        print("🗑️ Өшірілді!")

        # ID қайта нөмірлеу
        try:
            cur.execute("""
                CREATE TABLE temp_phonebook (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(50),
                    phone VARCHAR(20)
                );
            """)
            cur.execute("INSERT INTO temp_phonebook (name, phone) SELECT name, phone FROM phonebook;")
            cur.execute("DROP TABLE phonebook;")
            cur.execute("ALTER TABLE temp_phonebook RENAME TO phonebook;")
            conn.commit()
        except Exception as e:
            conn.rollback()
            print("⚠️ Қайта нөмірлеу кезінде қате:", e)
    else:
        print("⚠️ Ондай дерек табылмады.")
        
def paginate_data(limit, offset):
    try:
        cur.execute("SELECT * FROM phonebook ORDER BY id ASC LIMIT %s OFFSET %s", (limit, offset))
        results = cur.fetchall()

        if results:
            print(f"\n📄 {offset + 1}-жазбадан бастап {offset + len(results)}-жазбаға дейін:")
            print("+-----+-----------------------+---------------------+")
            print("|  ID | Аты                   | Нөмірі              |")
            print("+-----+-----------------------+---------------------+")
            for row in results:
                print(f"| {row[0]:<3} | {row[1]:<21} | {row[2]:<19} |")
                print("+-----+-----------------------+---------------------+")
        else:
            print("📭 Бұл бетте дерек жоқ.")
    except Exception as e:
        print("⚠️ Қате:", e)        

# Кестені көрсету
def view_data():
    print("\n📋 Қалай көрсетеміз?")
    print("1. Барлық жазбалар")
    print("2. Шаблон арқылы іздеу")

    choice = input("Таңда (1-2): ")

    if choice == "1":
        cur.execute("SELECT * FROM phonebook ORDER BY id ASC")
        results = cur.fetchall()

        if results:
            print("\n📋 PHONEBOOK ЖАЗБАЛАРЫ:")
            print("+-----+-----------------------+---------------------+")
            print("|  ID | Аты                   | Нөмірі              |")
            print("+-----+-----------------------+---------------------+")
            for row in results:
                print(f"| {row[0]:<3} | {row[1]:<21} | {row[2]:<19} |")
                print("+-----+-----------------------+---------------------+")
        else:
            print("📁 Кестеде деректер жоқ.")
    
    elif choice == "2":
        print("\n🔎 Қай өріс бойынша іздейміз?")
        print("1. ID")
        print("2. Аты")
        print("3. Нөмірі")
        field_choice = input("Таңда (1-3): ")

        if field_choice == "1":
            pattern = input("ID мәнін енгіз: ")
            cur.execute("SELECT * FROM phonebook WHERE CAST(id AS TEXT) ILIKE %s", (f"%{pattern}%",))
        elif field_choice == "2":
            pattern = input("Атын енгіз (шаблон): ")
            cur.execute("SELECT * FROM phonebook WHERE name ILIKE %s", (f"%{pattern}%",))
        elif field_choice == "3":
            pattern = input("Нөмірін енгіз (шаблон): ")
            cur.execute("SELECT * FROM phonebook WHERE phone ILIKE %s", (f"%{pattern}%",))
        else:
            print("⚠️ Қате таңдау!")
            return
        
        results = cur.fetchall()

        if results:
            print("\n🔎 ІЗДЕУ НӘТИЖЕСІ:")
            print("+-----+-----------------------+---------------------+")
            print("|  ID | Аты                   | Нөмірі              |")
            print("+-----+-----------------------+---------------------+")
            for row in results:
                print(f"| {row[0]:<3} | {row[1]:<21} | {row[2]:<19} |")
                print("+-----+-----------------------+---------------------+")
        else:
            print("📭 Ештеңе табылмады.")
    
    else:
        print("⚠️ Қате таңдау! 1 немесе 2 енгізіңіз.")
        
        
        
def view_sorted(order_by, ascending=True):
    order = "ASC" if ascending else "DESC"
    try:
        cur.execute(f"SELECT * FROM phonebook ORDER BY {order_by} {order}")
        results = cur.fetchall()
        if results:
            print("\n📋 СҰРЫПТАЛҒАН PHONEBOOK:")
            print("+-----+-----------------------+---------------------+")
            print("|  ID | Аты                   | Нөмірі              |")
            print("+-----+-----------------------+---------------------+")
            for row in results:
                print(f"| {row[0]:<3} | {row[1]:<21} | {row[2]:<19} |")
                print("+-----+-----------------------+---------------------+")
        else:
            print("📁 Кестеде деректер жоқ.")
    except Exception as e:
        print("⚠️ Сұрыптау кезінде қате:", e)
        
def sort_menu():
    while True:
        print("\n🔽 СҰРЫПТАУ МӘЗІРІ:")
        print("1. ID бойынша (өсу)")
        print("2. ID бойынша (кему)")
        print("3. Аты бойынша (A-Z)")
        print("4. Аты бойынша (Z-A)")
        print("5. Нөмірі бойынша (өсу)")
        print("6. Нөмірі бойынша (кему)")
        print("0. 🔙 Артқа қайту")

        choice = input("Таңда (0-6): ")

        if choice == "1":
            view_sorted("id", True)
        elif choice == "2":
            view_sorted("id", False)
        elif choice == "3":
            view_sorted("name", True)
        elif choice == "4":
            view_sorted("name", False)
        elif choice == "5":
            view_sorted("phone", True)
        elif choice == "6":
            view_sorted("phone", False)
        elif choice == "0":
            break
        else:
            print("⚠️ Қате таңдау! Қайтадан көріңіз.")
        
# Мәзір
def print_menu():
    menu_title = "📱  PHONEBOOK МӘЗІРІ"
    line = "=" * 42
    print("\n" + line.center(42))
    print(menu_title.center(42))
    print(line.center(42))

    print("┌──────────────────────────────┐".ljust(21) + "┌──────────────────────────────┐".rjust(21))
    print("│  1  📂 CSV-тен жүктеу        │".ljust(21) + "│  2  ✍️  Қолмен енгізу         │".rjust(21))
    print("└──────────────────────────────┘".ljust(21) + "└──────────────────────────────┘".rjust(21))

    print("┌──────────────────────────────┐".ljust(21) + "┌──────────────────────────────┐".rjust(21))
    print("│  3  🔄 Жаңарту               │".ljust(21) + "│  4  🔍 Іздеу                 │".rjust(21))
    print("└──────────────────────────────┘".ljust(21) + "└──────────────────────────────┘".rjust(21))

    print("┌──────────────────────────────┐".ljust(21) + "┌──────────────────────────────┐".rjust(21))
    print("│  5  ❌ Өшіру                 │".ljust(21) + "│  6  📜 Кестені көру          │".rjust(21))
    print("└──────────────────────────────┘".ljust(21) + "└──────────────────────────────┘".rjust(21))

    print("┌──────────────────────────────┐".ljust(21) + "┌──────────────────────────────┐".rjust(21))
    print("│  7  📑 Беттермен қарау       │".ljust(21) + "│  0  🚪 Шығу                  │".rjust(21))
    print("└──────────────────────────────┘".ljust(21) + "└──────────────────────────────┘".rjust(21))

    print(line.center(42))
    
while True:
    print_menu()
    choice = input("Таңда (0-7): ")

    if choice == "1":
        load_from_csv()
    elif choice == "2":
        insert_manually()
    elif choice == "3":
        update_entry()
    elif choice == "4":
        query_data()
    elif choice == "5":
        delete_entry()
    elif choice == "6":
        view_data() 
    elif choice == "7":
        try:
            limit = int(input("Бір бетте қанша жазба көрсетеміз? (мыс: 5): "))
            offset = 0
            while True:
                paginate_data(limit, offset)
                print("\n➡️ Келесі бетке өту үшін 'n', алдыңғы бет үшін 'p', шығу үшін 'q' басыңыз.")
                nav = input("Таңдау: ").lower()
                if nav == 'n':
                    offset += limit
                elif nav == 'p':
                    offset = max(0, offset - limit)
                elif nav == 'q':
                    break
                else:
                    print("⚠️ Белгісіз таңдау!")
        except ValueError:
            print("⚠️ Қате! Тек бүтін сан енгізіңіз.")
    elif choice == "0":
        print("📤 Шығу орындалды. Сау болыңыз!")
        break
    else:
        print("⚠️  Қате таңдау! Қайтадан көріңіз.")
cur.close()
conn.close()


