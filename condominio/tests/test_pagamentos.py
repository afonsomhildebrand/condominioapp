import unittest
from unittest.mock import patch
from database import Database
from tests.helpers import FakeConnection, FakeCursor

class TestPagamentos(unittest.TestCase):
    @patch("mysql.connector.connect", return_value=FakeConnection(FakeCursor([(0,)])))
    def test_add_pagamento_and_filters(self, _conn):
        db = Database()
        db.add_pagamento(10, 3, "2026-02", 350.00, "pendente", None)
        insert_sql, insert_params = db.cursor.statements[-1]
        self.assertIn("INSERT INTO pagamentos", insert_sql)
        self.assertIn("%s", insert_sql)
        self.assertEqual(insert_params[0], 10)
        db.get_pagamentos(condominio_id=3)
        sel_sql, _ = db.cursor.statements[-1]
        self.assertIn("WHERE condominio_id=%s", sel_sql)
        db.get_pagamentos(morador_id=10, referencia="2026-02")
        sel_sql2, _ = db.cursor.statements[-1]
        self.assertIn("morador_id=%s", sel_sql2)
        self.assertIn("referencia=%s", sel_sql2)

if __name__ == "__main__":
    unittest.main()
