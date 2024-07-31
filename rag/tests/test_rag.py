from psycopg import sql
from psycopg.rows import dict_row


def test_tables_count(database):
    with database.cursor(row_factory=dict_row) as cursor:
        cursor.execute(
            sql.SQL(
                "SELECT COUNT(*) FROM information_schema.tables "
                "WHERE table_type = 'BASE TABLE'"
                " AND table_schema NOT IN ('pg_catalog', 'information_schema')"
            )
        )
        result = cursor.fetchone()
    assert result["count"] == 0
