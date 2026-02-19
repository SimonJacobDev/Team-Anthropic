import sqlite3

conn = sqlite3.connect('entitleai.db')
cursor = conn.cursor()

print("📋 HOUSEHOLDS IN DATABASE:")
print("-" * 50)

cursor.execute('SELECT id, name, age, gender, village FROM households LIMIT 10')
for row in cursor.fetchall():
    print(f"ID: {row[0]} | {row[1]} | Age: {row[2]} | {row[3]} | {row[4]}")

print("\n📊 TOTAL COUNT:", cursor.execute('SELECT COUNT(*) FROM households').fetchone()[0])

conn.close()