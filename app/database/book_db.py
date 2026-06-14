import app.database.db_connection as db_c


class BookDB:
    def create_book(self, data: dict):
        values = (data.get("title"), data.get("author"), data.get("genre"))

        sql = "INSERT INTO books (title, author, genre) VALUES (%s, %s, %s)"

        with db_c.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql, values)
                conn.commit()

    def get_all_books(self) -> list:
        with db_c.get_connection() as conn:
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute("SELECT * FROM books")
                data = cursor.fetchall()
        return data

    def get_book_by_id(self, id) -> dict | None:
        with db_c.get_connection() as conn:
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute("SELECT * FROM books WHERE id = %s", (id,))
                data = cursor.fetchone()
        return data

    def update_book(self, id, data: dict):
        keys = [f"{k} = %s" for k in data.keys()]
        keys = ", ".join(keys)
        values = [v for v in data.values()] + [id]
        sql = f"UPDATE books SET {keys} WHERE id = %s"
        with db_c.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql, values)
                conn.commit()
                change = cursor.rowcount > 0
        return change

    def set_available(self, id: int, val: bool, member_id: int):
        if val:
            sql = (
                "UPDATE books SET is_available = TRUE, "
                "borrowed_by_member_id = NULL WHERE id = %s"
            )
            values = (id,)
        else:
            sql = (
                "UPDATE books SET is_available = FALSE, "
                "borrowed_by_member_id = %s WHERE id = %s"
            )
            values = (member_id, id)
        with db_c.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql, values)
                conn.commit()
                change = cursor.rowcount > 0
        return change

    def borrow_book(self, member_id, book_id):
        sum_borrowed = self.count_active_borrows_by_member(member_id)
        if sum_borrowed > 3:
            raise ValueError("Member already have 3 books")
        book = self.get_book_by_id(book_id)
        if not book.get("is_available"):
            raise ValueError("Book is taken")
        success = self.set_available(book_id, False, member_id)
        return success

    def return_book(self, member_id, book_id):
        book = self.get_book_by_id(book_id)
        if book.get("borrowed_by_member_id") != member_id:
            raise ValueError("Not your book")
        success = self.set_available(book_id, True, member_id)
        return success

    def count_total_book(self) -> int:
        sql = "SELECT COUNT(*) AS books_count FROM books"
        with db_c.get_connection() as conn:
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute(sql)
                data = cursor.fetchone()
        return data["books_count"]

    def count_available_books(self):
        sql = "SELECT COUNT(*) AS available_books_count FROM books WHERE is_available = TRUE"
        with db_c.get_connection() as conn:
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute(sql)
                data = cursor.fetchone()
        return data["available_books_count"]

    def count_borrowed_books(self):
        sql = "SELECT COUNT(*) AS borrowed_books_count FROM books WHERE is_available = FALSE"
        with db_c.get_connection() as conn:
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute(sql)
                data = cursor.fetchone()
        return data["borrowed_books_count"]

    def count_by_genre(self, genre) -> int:
        sql = "SELECT genre COUNT(*) AS count_genre FROM books WHERE genre = %s"
        with db_c.get_connection() as conn:
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute(sql, (genre,))
                data = cursor.fetchone()
        return data["count_genre"]

    def count_active_borrows_by_member(self, member_id):
        sql = "SELECT COUNT(*) AS borrows FROM books WHERE borrowed_by_member_id = %s"
        with db_c.get_connection() as conn:
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute(sql, (member_id,))
                result = cursor.fetchone()
        return result["borrows"]
