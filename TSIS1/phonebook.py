from connect import connect
import csv
import json


# ======================
# INSERT
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
# READ
# ======================
def show_contacts():
    conn = connect()
    cur = conn.cursor()

    cur.execute("SELECT * FROM contacts ORDER BY id")
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
# SEARCH SIMPLE
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
# ADVANCED SEARCH
# ======================
def advanced_search():
    group = input("Group (Family/Work/Friend/Other or empty): ")
    email = input("Email contains: ")
    sort = input("Sort by (name/birthday/date): ")

    limit = 3
    offset = 0

    conn = connect()
    cur = conn.cursor()

    while True:
        query = """
        SELECT c.username, c.email, c.birthday, g.name
        FROM contacts c
        LEFT JOIN groups g ON c.group_id = g.id
        WHERE (%s = '' OR g.name = %s)
          AND (%s = '' OR c.email ILIKE %s)
        """

        if sort == "name":
            query += " ORDER BY c.username"
        elif sort == "birthday":
            query += " ORDER BY c.birthday"
        elif sort == "date":
            query += " ORDER BY c.created_at"

        query += " LIMIT %s OFFSET %s"

        cur.execute(query, (group, group, email, f"%{email}%", limit, offset))
        rows = cur.fetchall()

        print("\n--- PAGE ---")
        for r in rows:
            print(r)

        cmd = input("next / prev / quit: ")

        if cmd == "next":
            offset += limit
        elif cmd == "prev":
            offset = max(0, offset - limit)
        else:
            break

    cur.close()
    conn.close()


# ======================
# EXPORT JSON (FIXED)
# ======================
def export_json():
    conn = connect()
    cur = conn.cursor()

    cur.execute("""
    SELECT c.username, c.email, c.birthday, g.name, p.phone, p.type
    FROM contacts c
    LEFT JOIN groups g ON c.group_id = g.id
    LEFT JOIN phones p ON c.id = p.contact_id
    """)

    rows = cur.fetchall()

    data = []
    for r in rows:
        data.append({
            "name": r[0],
            "email": r[1],
            "birthday": r[2].isoformat() if r[2] else None,
            "group": r[3],
            "phone": r[4],
            "type": r[5]
        })

    with open("contacts.json", "w") as f:
        json.dump(data, f, indent=4)

    print("✅ Exported to contacts.json")

    cur.close()
    conn.close()


# ======================
# IMPORT JSON (FIXED)
# ======================
def import_json():
    conn = connect()
    cur = conn.cursor()

    with open("contacts.json") as f:
        data = json.load(f)

    for item in data:
        name = item["name"]

        cur.execute("SELECT 1 FROM contacts WHERE username=%s", (name,))
        exists = cur.fetchone()

        if exists:
            choice = input(f"{name} exists. skip/overwrite: ")
            if choice == "skip":
                continue
            else:
                cur.execute("DELETE FROM contacts WHERE username=%s", (name,))

        #FIX
        birthday = item["birthday"]
        if birthday == "None" or birthday == "" or birthday is None:
            birthday = None

        email = item.get("email")
        if not email or email == "None":
            email = None

        cur.execute("""
        INSERT INTO contacts(username, email, birthday)
        VALUES (%s, %s, %s)
        RETURNING id
        """, (name, email, birthday))

        cid = cur.fetchone()[0]

        if item["group"]:
            cur.execute("CALL move_to_group(%s, %s)", (name, item["group"]))

        if item["phone"]:
            cur.execute("""
            INSERT INTO phones(contact_id, phone, type)
            VALUES (%s, %s, %s)
            """, (cid, item["phone"], item["type"]))

    conn.commit()
    print("✅ JSON imported")

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
7 - Advanced search
8 - Export JSON
9 - Import JSON
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
        elif choice == "7":
            advanced_search()
        elif choice == "8":
            export_json()
        elif choice == "9":
            import_json()
        elif choice == "0":
            print("Bye!")
            break
        else:
            print("Invalid option")


# ======================
# START
# ======================
if __name__ == "__main__":
    menu()