import unittest
from unittest.mock import patch
from database import Database
from tests.helpers import FakeConnection, FakeCursor

class TestSindico(unittest.TestCase):
    @patch("mysql.connector.connect", return_value=FakeConnection(FakeCursor([(0,)])))
    def test_set_and_get_sindico(self, _conn):
        db = Database()
        db.set_sindico(5, 12)
        update_sql, update_params = db.cursor.statements[-1]
        self.assertIn("UPDATE condominios SET sindico_morador_id=%s", update_sql)
        self.assertEqual(update_params[0], 12)
        db.get_sindico(5)
        select_sql, select_params = db.cursor.statements[-1]
        self.assertIn("JOIN condominios c ON c.sindico_morador_id = m.id", select_sql)
        self.assertEqual(select_params[0], 5)

if __name__ == "__main__":
    unittest.main()
