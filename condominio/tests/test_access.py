import unittest
from unittest.mock import patch
import tkinter as tk
from main import Dashboard


class DummyDB:
    pass


class TestAccessControl(unittest.TestCase):
    def setUp(self):
        self.root = tk.Tk()
        self.root.withdraw()

    def tearDown(self):
        try:
            self.root.destroy()
        except:
            pass

    @patch("tkinter.messagebox.showwarning")
    def test_open_condominios_denied_for_sindico(self, mock_warn):
        user_data = (2, "s1", "sindico", 1)
        dash = Dashboard(self.root, user_data)
        dash.open_condominios()
        mock_warn.assert_called()

    @patch("tkinter.messagebox.showwarning")
    def test_open_usuarios_denied_for_sindico(self, mock_warn):
        user_data = (2, "s1", "sindico", 1)
        dash = Dashboard(self.root, user_data)
        dash.open_usuarios()
        mock_warn.assert_called()


if __name__ == "__main__":
    unittest.main()
