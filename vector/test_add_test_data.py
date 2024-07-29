import unittest
from unittest.mock import patch
from add_test_data import add_test_data

class TestAddTestData(unittest.TestCase):

    @patch("add_test_data.embedding", return_value=Mock(data=[
        {'embedding': [7.70271397e-02, -3.73198812e-02], 'sequence': 0},
        {'embedding': [1.70271397e-02, 5.6266789e-02, 2.73198812e-02], 'sequence': 1},
        {'embedding': [-8.77134927e-01, -4.07516444e-01, 3.52297473e-03], 'sequence': 2}
    ]))
    @patch("add_test_data.create_db_connection")
    @patch("add_test_data.psycopg2.connect")
    @patch("add_test_data.psycopg2.Error")
    def test_add_test_data(self, mocked_psycopg2_error, mocked_psycopg2_connect, mocked_create_db_connection, mocked_embedding):
        connection = Mock()
        cursor = Mock()
        
        mocked_create_db_connection.return_value = connection
        connection.cursor.return_value = cursor

        add_test_data()
        
        cursor.execute.assert_called()
        connection.commit.assert_called()
        
        if cursor:
            cursor.close.assert_called()
        if connection:
            connection.close.assert_called()

if __name__ == '__main__':
    unittest.main()