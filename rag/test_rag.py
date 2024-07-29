
import unittest
from unittest.mock import patch, Mock
from sqlalchemy.orm import sessionmaker
from add_test_data import add_test_data
from rag.rag import insert_embeddings

class TestRag(unittest.TestCase):

    @patch("rag.rag.create_db_connection")
    @patch("rag.add_test_data.embedding", return_value=Mock(data=[
        {'embedding': [7.70271397e-02, 7.62866789e-02, -3.73198812e-02], 'sequence': 0},
        {'embedding': [1.70271397e-02, 5.6266789e-02, 2.73198812e-02], 'sequence': 1},
        {'embedding': [-8.77134927e-01, -4.07516444e-01, 3.52297473e-03], 'sequence': 2}
    ]))
    def test_insert_embeddings(self, mocked_embedding, mocked_create_connection):
        session = sessionmaker()
        embeddings = [[7.70271397e-02, 7.62866789e-02, -3.73198812e-02],
                      [1.70271397e-02, 5.6266789e-02, 2.73198812e-02],
                      [-8.77134927e-01, -4.07516444e-01, 3.52297473e-03]]
        
        # Test method
        insert_embeddings(session, embeddings)
        
        # Check if the session.add() method was called with the correct embeddings
        session.add.assert_called_with(insert_embeddings(embeddind=embeddings[0]))
        session.add.assert_called_with(insert_embeddings(embeddind=embeddings[1]))
        session.add.assert_called_with(insert_embeddings(embeddind=embeddings[2]))
        
        # Check if the commit() method was called
        session.commit.assert_called_once()

if __name__ == '__main__':
    unittest.main()