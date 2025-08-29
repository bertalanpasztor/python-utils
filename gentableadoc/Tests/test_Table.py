from gentableadoc.Table import Table


def test_get_tables():
    # mock db object with connection
    class MockDB:
        def __init__(self):
            self.conn = 'connection'

        def execute_query(self, cmd):
            return [('schemaname', 'relname')]

    db = MockDB()
    tables = Table.get_tables(db,'schemaname')
    assert (tables['relname'].schema == 'schemaname' and
            tables['relname'].conn == 'connection' and
            tables['relname'].name == 'relname')
