from sqlalchemy import text

def test__db_connection_check(db_session):
    result = db_session.execute(text("SELECT name FROM sqlite_master WHERE type='table';")).fetchall()
    assert len(result) > 0  # テーブルが1つ以上存在すること