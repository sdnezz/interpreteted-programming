import sqlite3

con = sqlite3.connect("../hotel.db")
curs = con.cursor()

curs.execute("""
    CREATE TABLE IF NOT EXISTS Guests(
    guest_id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    phone_number TEXT,
    email TEXT,
    passport_number TEXT UNIQUE
);
""")

curs.execute("""
CREATE TABLE IF NOT EXISTS Rooms (
    room_id INTEGER PRIMARY KEY AUTOINCREMENT,
    room_number INTEGER UNIQUE NOT NULL,
    room_type TEXT NOT NULL,
    price_per_night REAL NOT NULL,
    status TEXT NOT NULL CHECK(status IN ('свободен', 'занят', 'ремонт'))
);
""")

curs.execute("""
CREATE TABLE IF NOT EXISTS Bookings(
    booking_id INTEGER PRIMARY KEY AUTOINCREMENT,
    guest_id INTEGER NOT NULL,
    room_id INTEGER NOT NULL,
    check_in_date DATE NOT NULL,
    check_out_date DATE NOT NULL,
    total_price REAL NOT NULL,
    FOREIGN KEY (guest_id) REFERENCES Guests(guest_id),
    FOREIGN KEY (room_id) REFERENCES Rooms(room_id)
);
""")

curs.execute("""
CREATE TABLE IF NOT EXISTS Services (
    service_id INTEGER PRIMARY KEY AUTOINCREMENT,
    service_name TEXT NOT NULL,
    service_price REAL NOT NULL
);
""")

# Добавление гостей
curs.execute("""
INSERT INTO Guests (first_name, last_name, phone_number, email, passport_number)
VALUES ('Андрей', 'Андреев', '+73334567890', 'Andreev@example.com', '3334567890');
""")

# Добавление номеров
curs.execute("""
INSERT INTO Rooms (room_number, room_type, price_per_night, status)
VALUES (103, 'Одноместный', 2500.00, 'занят'),
       (104, 'Двухместный', 3500.00, 'занят'),
       (202, 'Люкс', 7000.00, 'ремонт');
""")

# Добавление бронирования
curs.execute("""
INSERT INTO Bookings (guest_id, room_id, check_in_date, check_out_date, total_price)
VALUES (2, 102, '2024-11-22', '2024-11-25', 12500.00);
""")

curs.execute("""
SELECT room_number, room_type, price_per_night
FROM Rooms
WHERE status = 'свободен';
""")
print(curs.fetchall())

curs.execute("""
SELECT SUM(total_price) AS total_revenue
FROM Bookings;
""")
print(curs.fetchone()[0])

curs.execute("""select * from guests;""")
print(curs.fetchall())

con.commit()
con.close()