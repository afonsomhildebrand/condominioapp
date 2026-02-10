import unittest
from unittest.mock import patch
import tkinter as tk
import main

class TestDeploySmoke(unittest.TestCase):
    def setUp(self):
        self.root = tk.Tk()
        self.root.withdraw()
    def tearDown(self):
        try:
            self.root.destroy()
        except:
            pass
    @patch("tkinter.messagebox.showerror")
    @patch.object(main.Database, "verify_user", return_value=None)
    def test_login_shows_error_on_invalid(self, mock_verify, mock_err):
        app = main.LoginWindow(self.root)
        app.entry_user.insert(0, "x")
        app.entry_pass.insert(0, "y")
        app.login()
        mock_err.assert_called()
    @patch("mysql.connector.connect")
    def test_dashboard_lazy_db_init(self, mock_connect):
        user_data = (1, "admin", "admin", None)
        dash = main.Dashboard(self.root, user_data)
        self.assertIsNone(dash.db)
        dash.open_moradores()
        self.assertIsNotNone(dash.db)
        self.assertTrue(mock_connect.called)

if __name__ == "__main__":
    unittest.main()
