from connect import connect
import csv


# ======================
# INSERT (console input)
# ======================
def insert_contact():
    name = input("Enter name: ")
    phone = input("Enter phone: ")

    conn = connect()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO contacts (username, phone) VALUES (%s, %s)",
        (name, phone)
    )

    conn.commit()
    cur.close()
    conn.close()

    print("✅ Contact added!")


# ======================
# READ (show all)
# ======================
def show_contacts():
    conn = connect()
    cur = conn.cursor()

    cur.execute("SELECT * FROM contacts")
    rows = cur.fetchall()

    print("\n--- CONTACTS ---")
    for row in rows:
        print(f"ID:{row[0]} | Name:{row[1]} | Phone:{row[2]}")

    cur.close()
    conn.close()


# ======================
# UPDATE
# ======================
def update_contact():
    name = input("Enter username to update: ")
    new_phone = input("Enter new phone: ")

    conn = connect()
    cur = conn.cursor()

    cur.execute(
        "UPDATE contacts SET phone=%s WHERE username=%s",
        (new_phone, name)
    )

    conn.commit()
    cur.close()
    conn.close()

    print("✅ Contact updated!")


# ======================
# DELETE
# ======================
def delete_contact():
    name = input("Enter username to delete: ")

    conn = connect()
    cur = conn.cursor()

    cur.execute(
        "DELETE FROM contacts WHERE username=%s",
        (name,)
    )

    conn.commit()
    cur.close()
    conn.close()

    print("✅ Contact deleted!")


# ======================
# IMPORT CSV
# ======================
def import_csv():
    conn = connect()
    cur = conn.cursor()

    try:
        with open("contacts.csv", encoding="utf-8") as file:
            reader = csv.reader(file)

            for row in reader:
                cur.execute(
                    "INSERT INTO contacts (username, phone) VALUES (%s, %s)",
                    (row[0], row[1])
                )

        conn.commit()
        print("✅ CSV imported!")

    except Exception as e:
        print("Error importing CSV:", e)

    finally:
        cur.close()
        conn.close()


# ======================
# FILTER SEARCH (extra for practice)
# ======================
def search_by_name():
    keyword = input("Enter name to search: ")

    conn = connect()
    cur = conn.cursor()

    cur.execute(
        "SELECT * FROM contacts WHERE username ILIKE %s",
        (f"%{keyword}%",)
    )

    rows = cur.fetchall()

    for row in rows:
        print(row)

    cur.close()
    conn.close()


# ======================
# MENU
# ======================
def menu():
    while True:
        print("""
========= PHONEBOOK =========
1 - Add contact
2 - Show contacts
3 - Update contact
4 - Delete contact
5 - Import from CSV
6 - Search by name
0 - Exit
=============================
""")

        choice = input("Choose option: ")

        if choice == "1":
            insert_contact()
        elif choice == "2":
            show_contacts()
        elif choice == "3":
            update_contact()
        elif choice == "4":
            delete_contact()
        elif choice == "5":
            import_csv()
        elif choice == "6":
            search_by_name()
        elif choice == "0":
            print("Bye!")
            break
        else:
            print("Invalid option")


# ======================
# START PROGRAM
# ======================
if __name__ == "__main__":
    menu()