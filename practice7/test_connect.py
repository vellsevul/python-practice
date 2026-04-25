from connect import connect

try:
    conn = connect()
    print("Connected successfully!")
    conn.close()
except Exception as e:
    print("Error:", e)