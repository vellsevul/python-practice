from connect import connect

# ==========================================
# 1. UPSERT (Используем процедуру из P8)
# ==========================================
def upsert_contact():
    name = input("Enter name: ")
    phone = input("Enter phone: ")

    conn = connect()
    cur = conn.cursor()
    
    # Вместо прямого INSERT/UPDATE вызываем процедуру
    cur.execute("CALL upsert_contact(%s, %s)", (name, phone))
    
    conn.commit()
    cur.close()
    conn.close()
    print(f"✅ Contact {name} processed (added or updated)!")

# ==========================================
# 2. DELETE (Используем процедуру из P8)
# ==========================================
def delete_contact():
    val = input("Enter username or phone to delete: ")

    conn = connect()
    cur = conn.cursor()
    
    # Процедура сама разберется, по какому полю удалять
    cur.execute("CALL delete_contact(%s)", (val,))
    
    conn.commit()
    cur.close()
    conn.close()
    print("✅ Contact removed!")

# ==========================================
# 3. PAGINATION (Используем функцию из P8)
# ==========================================
def show_paginated():
    limit = int(input("How many contacts per page? "))
    offset = int(input("How many to skip (offset)? "))

    conn = connect()
    cur = conn.cursor()
    
    # Функции, возвращающие таблицу, вызываются через SELECT
    cur.execute("SELECT * FROM get_contacts_page(%s, %s)", (limit, offset))
    rows = cur.fetchall()

    print(f"\n--- CONTACTS (Page: L={limit}, O={offset}) ---")
    for row in rows:
        print(f"ID:{row[0]} | Name:{row[1]} | Phone:{row[2]}")

    cur.close()
    conn.close()

# ==========================================
# 4. PATTERN SEARCH (Используем функцию из P8)
# ==========================================
def search_pattern():
    pattern = input("Enter search pattern (part of name or phone): ")

    conn = connect()
    cur = conn.cursor()
    
    cur.execute("SELECT * FROM get_contacts_by_pattern(%s)", (pattern,))
    rows = cur.fetchall()

    print("\n--- SEARCH RESULTS ---")
    for row in rows:
        print(row)

    cur.close()
    conn.close()

# ==========================================
# 5. BULK INSERT (Массовая вставка через процедуру)
# ==========================================
def bulk_insert():
    print("\nEnter contacts in format 'Name:Phone' separated by commas")
    print("Example: Alice:12345, Bob:67890")
    data_input = input("Contacts: ")
    
    names = []
    phones = []
    
    # Парсим ввод пользователя
    try:
        for item in data_input.split(','):
            n, p = item.split(':')
            names.append(n.strip())
            phones.append(p.strip())
            
        conn = connect()
        cur = conn.cursor()
        
        # Передаем списки в PostgreSQL массивами
        cur.execute("CALL insert_many_contacts(%s, %s)", (names, phones))
        
        conn.commit()
        print(f"✅ Bulk insert processed for {len(names)} contacts!")
        
    except ValueError:
        print("❌ Error: Invalid format. Use Name:Phone, Name:Phone")
    except Exception as e:
        print(f"❌ Database error: {e}")
    finally:
        if 'cur' in locals(): cur.close()
        if 'conn' in locals(): conn.close()