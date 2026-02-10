import sqlite3

# connect to database (it will be created automatically)
conn = sqlite3.connect("services.db")

cursor = conn.cursor()

# create services table
cursor.execute("""
CREATE TABLE IF NOT EXISTS services (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    price INTEGER NOT NULL
)
""")

# create bookings table
cursor.execute("""
CREATE TABLE IF NOT EXISTS bookings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_name TEXT NOT NULL,
    service_name TEXT NOT NULL,
    booking_date TEXT NOT NULL,
    status TEXT DEFAULT 'Pending'
)
""")

# insert default services
cursor.execute("INSERT INTO services (name, price) VALUES ('Plumber', 500)")
cursor.execute("INSERT INTO services (name, price) VALUES ('Electrician', 400)")
cursor.execute("INSERT INTO services (name, price) VALUES ('House Cleaning', 1000)")
cursor.execute("INSERT INTO services (name, price) VALUES ('AC Repair', 1200)")

conn.commit()
conn.close()

print("✅ Database created successfully!")
