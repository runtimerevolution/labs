
import unittest
from unittest.mock import patch, Mock
from rag.rag import find_similar_embeddings

class TestRag(unittest.TestCase):

    @patch("rag.rag.cursor")
    @patch("rag.rag.connection")
    def test_find_similar_embeddings(self, mock_connection, mock_cursor):
        mock_execute = mock_cursor.return_value.execute
        mock_return_value = [("1", "file1.txt", "Text 1", 0.8), ("2", "file2.txt", "Text 2", 0.75)]
        mock_cursor.return_value.fetchall.return_value = mock_return_value
        
        result = find_similar_embeddings("Sample test query")
        
        mock_execute.assert_called_once()
        mock_cursor.assert_attribute('close').assert_called_once()
        mock_connection.close.assert_called_once()
        self.assertEqual(result, mock_return_value)