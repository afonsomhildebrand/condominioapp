import unittest
from unittest.mock import patch
import tkinter as tk
from main import Dashboard
from tests.helpers import FakeConnection, FakeCursor

class TestGuiPredios(unittest.TestCase):
    def setUp(self):
        self.root = tk.Tk()
        self.root.withdraw()
    def tearDown(self):
        try:
            self.root.destroy()
        except:
            pass
    @patch("tkinter.messagebox.showwarning")
    def test_open_predios_denied_for_sindico(self, mock_warn):
        user_data = (2, "s1", "sindico", 1)
        dash = Dashboard(self.root, user_data)
        dash.open_predios()
        mock_warn.assert_called()
    @patch("mysql.connector.connect", return_value=FakeConnection(FakeCursor([(0,)])))
    def test_open_predios_admin_initializes_db(self, _conn):
        user_data = (1, "admin", "admin", None)
        dash = Dashboard(self.root, user_data)
        self.assertIsNone(dash.db)
        dash.open_predios()
        self.assertIsNotNone(dash.db)

if __name__ == "__main__":
    unittest.main()
