import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        port=3306,
        user="root",
        password="root",
        database="library_db"
    )

def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    books_sql = """
    CREATE TABLE IF NOT EXIST books (
        id INT PRIMARY KEY AUTO_INCREMENT,
        title VARCHAR(50) NOT NULL,
        author VARCHAR(50) NOT NULL,
        genre ENUM('Fiction' , 'Non-Fiction' , 'Science', 'History', 'Other') NOT NULL,
        is_available BOOLEAN DEFAULT TRUE NOT NULL,
        borrowed_by_member_id INT DEFAULT NULL
    )
"""
    members_sql = """
    CREATE TABLE IF NOT EXIST members (
        id INT PRIMARY KEY AUTO_INCREMENT,
        name VARCHAR(50) NOT NULL,
        email VARCHAR(255) UNIQUE NOT NULL,
        is_active BOOLEAN DEFAULT TRUE NOT NULL,
        total_borrowed INT DEFAULT 0 NOT NULL
    )
"""
    cursor.execute(books_sql)
    cursor.execute(members_sql)

    conn.commit()

    cursor.close()
    conn.close()