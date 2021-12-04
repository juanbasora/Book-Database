import sqlite3

class Database:

	def __init__(self):
		self.conn = sqlite3.connect("books.db")
		self.cur = self.conn.cursor()
		self.cur.execute("CREATE TABLE IF NOT EXISTS books (id INTEGER PRIMARY KEY, title text, author text, year integer, description text)")
		self.conn.commit()

	def add_entry(self, title, author, year, description):
		self.cur.execute("INSERT INTO books VALUES (NULL, ?, ?, ?, ?)", (title, author, year, description))
		self.conn.commit()

	def view_all(self):
		self.cur.execute("SELECT * FROM books")
		rows = self.cur.fetchall()
		return rows

	def search(self, id):
		self.cur.execute("SELECT * FROM books WHERE id=?", (id,))
		rows = self.cur.fetchall()
		return rows

	def update(self, id, title, author, year, description):
		self.cur.execute("UPDATE books set title=?, author=?, year=?, description=? WHERE id=?", (title, author, year, description, id))
		self.conn.commit()

	def delete(self, id):
		self.cur.execute("DELETE FROM books WHERE id=?", (id,))
		self.conn.commit()

	def __del__(self):
		self.conn.close()