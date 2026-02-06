import unittest
from unittest.mock import patch
from database import Database


class FakeCursor:
    def __init__(self):
        self.statements = []

    def execute(self, sql, params=None):
        self.statements.append((sql, params))

    def fetchone(self):
        return (1, "admin", "admin", None)


class FakeConnection:
    def __init__(self):
        self.database = None
        self.cursor_obj = FakeCursor()

    def cursor(self):
        return self.cursor_obj

    def commit(self):
        pass

    def close(self):
        pass


class TestDatabaseQueries(unittest.TestCase):
    @patch("mysql.connector.connect", return_value=FakeConnection())
    def test_add_user_uses_mysql_placeholders(self, _conn):
        db = Database()
        db.add_user("u1", "p1", "admin", None)
        sql, params = db.cursor.statements[-1]
        self.assertIn("INSERT INTO usuarios", sql)
        self.assertIn("%s", sql)
        self.assertEqual(params[0], "u1")

    @patch("mysql.connector.connect", return_value=FakeConnection())
    def test_verify_user_query(self, _conn):
        db = Database()
        res = db.verify_user("admin", "admin123")
        self.assertIsNotNone(res)
        sql, params = db.cursor.statements[-1]
        self.assertIn("SELECT id, username, nivel, condominio_id FROM usuarios", sql)
        self.assertIn("%s", sql)
        self.assertEqual(params[0], "admin")

    def test_password_hash_static(self):
        h = Database.hash_password("x")
        self.assertEqual(len(h), 64)


if __name__ == "__main__":
    unittest.main()
