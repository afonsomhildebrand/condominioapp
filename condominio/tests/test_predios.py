import unittest
from unittest.mock import patch
from database import Database
from tests.helpers import FakeConnection, FakeCursor

class TestPredios(unittest.TestCase):
    @patch("mysql.connector.connect", return_value=FakeConnection(FakeCursor([(0,)])))
    def test_add_predio_and_get_predios(self, _conn):
        db = Database()
        db.add_predio("Bloco A", 1, "Rua X")
        insert_sql, insert_params = db.cursor.statements[-1]
        self.assertIn("INSERT INTO predios", insert_sql)
        self.assertIn("%s", insert_sql)
        self.assertEqual(insert_params[0], "Bloco A")
        db.get_predios()
        select_all_sql, _ = db.cursor.statements[-1]
        self.assertIn("SELECT * FROM predios", select_all_sql)
        db.get_predios(2)
        select_where_sql, select_where_params = db.cursor.statements[-1]
        self.assertIn("WHERE condominio_id=%s", select_where_sql)
        self.assertEqual(select_where_params[0], 2)

if __name__ == "__main__":
    unittest.main()
