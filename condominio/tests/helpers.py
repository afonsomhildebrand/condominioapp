class FakeCursor:
    def __init__(self, fetchone_values=None, fetchall_value=None):
        self.statements = []
        self.fetchone_values = list(fetchone_values) if fetchone_values else [(0,)]
        self.fetchall_value = [] if fetchall_value is None else fetchall_value
    def execute(self, sql, params=None):
        self.statements.append((sql, params))
    def fetchone(self):
        if self.fetchone_values:
            return self.fetchone_values.pop(0)
        return (0,)
    def fetchall(self):
        return self.fetchall_value

class FakeConnection:
    def __init__(self, cursor=None):
        self.database = None
        self.cursor_obj = cursor or FakeCursor()
    def cursor(self):
        return self.cursor_obj
    def commit(self):
        pass
    def close(self):
        pass
