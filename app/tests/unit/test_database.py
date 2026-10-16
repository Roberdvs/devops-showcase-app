from app import database


def test_engine_does_not_echo_sql_statements():
    # SQLAlchemy's echo flag prints every statement as plain text to stdout,
    # bypassing the structured JSON logging the app configures. The attribute
    # is None when echo was never requested and True when it was.
    assert not database.engine.echo
